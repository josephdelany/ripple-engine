"""Registered schedule-imputed finalized-data sensitivity analysis.

The design stage consumes the frozen input bundle and frozen read ledger, but not
the realized target outcomes.  Publication scoring is a separate explicit call.
Nothing runs on import.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from structural_component_ablation import (
    TOL,
    calibrate_ess,
    canonical,
    effective_n,
    file_hash,
    holm_adjust,
    load_jsonl,
    minimum_attainable_ess,
    weights_at_temperature,
)
from structural_surface_experiment import (
    MIN_FIELDS,
    MIN_SCALE_N,
    ROOT,
    SEED,
    codebook_blocks,
    connect_bundle,
    paired_block,
    reduce_panel,
    weighted_crps,
)

BUNDLE = ROOT / "data" / "structural_surface" / "input"
READS = ROOT / "data" / "structural_surface" / "reads.jsonl"
SCORES = ROOT / "data" / "structural_surface" / "scores.jsonl"
OUT = ROOT / "data" / "structural_surface" / "availability"
REGISTRATION = ROOT / "registrations" / "CONTEMPORANEOUS_AVAILABILITY_ARM.md"
REGISTRATION_COMMIT = "3d57f36"
FROZEN_RELEASE_COMMIT = "1705713b801d7ffc48d7cc39adb5a802b613157c"
IMPLEMENTATION_COMMIT = "TO_BE_RECORDED_AFTER_IMPLEMENTATION_COMMIT"

FIELD_BLOCKS = {
    # physical
    "spare_capacity_opec": "physical",
    "us_crude_stocks_xspr": "physical",
    "us_spr_stock": "physical",
    "us_refinery_utilization": "physical",
    # actors
    "cinc": "actors", "milex_cow": "actors", "milper_cow": "actors",
    "milex_sipri": "actors", "milex_gdp_share_sipri": "actors",
    "polity2": "actors", "polity_durable": "actors",
    "leader_tenure_days": "actors", "leader_change_last_365d": "actors",
    "oil_rents_gdp": "actors", "coup_last_5y": "actors",
    # dyads
    "atop_defense_pact": "dyads", "atop_any_obligation": "dyads",
    "mid_count_10y": "dyads", "mid_max_hostlev_10y": "dyads",
    "mid_last_date": "dyads", "icb_crisis_count": "dyads",
    "icb_last_outcome_form": "dyads", "icb_last_violence": "dyads",
    "icb_last_tension": "dyads", "unga_ideal_point_distance": "dyads",
    # system
    "ucdp_active_conflicts": "system", "ucdp_intensity_max": "system",
    "ucdp_battle_deaths": "system", "mepv_regional_war": "system",
}

ALLOWED_SOURCES = frozenset({
    "EIA STEO Table 3d, surplus crude oil production capacity (STEO_m.xlsx)",
    "EIA https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCESTUS1&f=W (series eia.crude_stocks_xspr; bridge)",
    "EIA https://www.eia.gov/petroleum/ (series eia.spr_stocks; bridge)",
    "EIA https://www.eia.gov/petroleum/ (series eia.refinery_util; bridge)",
    "COW National Material Capabilities v7.0 (NMC-70-abridged.csv)",
    "Archigos v4.1 (Archigos_4.1_stata14.dta)",
    "Polity5 (p5v2018.xls, local file)",
    "SIPRI Military Expenditure Database (local file)",
    "World Bank WDI NY.GDP.PETR.RT.ZS (api.worldbank.org/v2)",
    "CSP Coups d'Etat 1946-2021 (CSPCoupsAnnualv2021.xls, local file)",
    "CSP Major Episodes of Political Violence 1946-2018 (MEPVv2018.xls, local file)",
    "UCDP/PRIO Armed Conflict v26.1 + UCDP Battle-Related Deaths v26.1",
    "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)",
    "COW dyadic MID 4.03: no dispute listed (absent = none)",
    "ICB v16 system level + dyads (Duke)",
    "ICB v16: no crisis listed for the dyad (absent = none)",
    "ATOP 5.1 directed dyad-year (atop5_1ddyr.csv)",
    "ATOP 5.1: no obligation listed (absent = none)",
    "UNGA ideal points, Bailey-Strezhnev-Voeten (IdealpointestimatesAll_Jun2024.csv)",
})


def admission_reason(row, event_date):
    """Return the first closed-world exclusion reason, or ``admitted``.

    This function intentionally has no access to prices, outcomes, losses, or
    candidate membership.
    """
    if row[5] == "situation":
        return "entity_is_situation"
    if int(row[8]):
        return "retrospective"
    if row[2] > event_date:
        return "obs_date_after_event"
    if row[6] > event_date:
        return "vintage_after_event"
    if row[1] not in FIELD_BLOCKS:
        return "field_not_allowlisted"
    if row[9] not in ALLOWED_SOURCES:
        return "source_not_allowlisted"
    return "admitted"


def admitted_panel(conn):
    """Build event vectors and a complete, deterministic admission receipt."""
    event_dates = dict(conn.execute("SELECT event_id,event_date FROM events"))
    raw = conn.execute(
        "SELECT event_id,field,obs_date,value,value_text,entity_id,vintage,release,"
        "retrospective,source FROM situation_state ORDER BY event_id,field,entity_id"
    ).fetchall()
    kept, first_reasons, overlap = [], Counter(), Counter()
    admitted_fields, admitted_blocks = Counter(), Counter()
    for row in raw:
        event_date = event_dates.get(row[0])
        if event_date is None:
            reason = "event_not_in_bundle"
        else:
            reason = admission_reason(row, event_date)
            checks = {
                "entity_is_situation": row[5] == "situation",
                "retrospective": bool(int(row[8])),
                "obs_date_after_event": row[2] > event_date,
                "vintage_after_event": row[6] > event_date,
                "field_not_allowlisted": row[1] not in FIELD_BLOCKS,
                "source_not_allowlisted": row[9] not in ALLOWED_SOURCES,
            }
            overlap.update(k for k, failed in checks.items() if failed)
        first_reasons[reason] += 1
        if reason == "admitted":
            kept.append((row[0], row[1], row[3], row[4], row[5]))
            admitted_fields[row[1]] += 1
            admitted_blocks[FIELD_BLOCKS[row[1]]] += 1
    vectors, metadata = reduce_panel(kept, FIELD_BLOCKS)
    receipt = {
        "field_allowlist": dict(sorted(FIELD_BLOCKS.items())),
        "source_allowlist": sorted(ALLOWED_SOURCES),
        "n_rows": len(raw),
        "n_admitted": len(kept),
        "first_exclusion_reason_counts": dict(sorted(first_reasons.items())),
        "overlapping_exclusion_rule_counts": dict(sorted(overlap.items())),
        "admitted_row_counts_by_field": dict(sorted(admitted_fields.items())),
        "admitted_row_counts_by_block": dict(sorted(admitted_blocks.items())),
    }
    return vectors, metadata, receipt


def nonmarket_distance(target, candidate, history, target_date, target_meta, candidate_meta):
    """Apply the frozen field scaling and block aggregation to non-market fields.

    A single usable non-market field can augment the four-field market block in
    the combined arm.  The standalone diagnostic separately enforces the frozen
    ``MIN_FIELDS`` threshold.
    """
    per_block, fields = defaultdict(list), []
    for field in sorted(set(target) & set(candidate)):
        kind = target_meta.get(field, {}).get("kind") or candidate_meta.get(field, {}).get("kind")
        block = target_meta.get(field, {}).get("block") or candidate_meta.get(field, {}).get("block")
        if block not in {"physical", "actors", "dyads", "system"}:
            raise AssertionError(f"unregistered non-market block for {field}: {block}")
        a, b = target[field], candidate[field]
        if kind == "cat":
            distance = 0.0 if str(a) == str(b) else 1.0
        else:
            prior = [float(vector[field]) for date, vector in history
                     if date < target_date and field in vector
                     and isinstance(vector[field], (int, float, np.number))]
            if len(prior) < MIN_SCALE_N:
                continue
            scale = float(np.std(prior, ddof=0))
            if not np.isfinite(scale) or scale <= 0:
                continue
            distance = min(abs(float(a) - float(b)) / scale / 3.0, 1.0)
        per_block[block].append(float(distance))
        fields.append(field)
    if not fields:
        return None
    blocks = {block: float(np.mean(values)) for block, values in per_block.items()}
    return {"distance": float(np.mean(list(blocks.values()))), "n_fields": len(fields),
            "fields": fields, "blocks": blocks}


def prepare_designs(bundle=BUNDLE, reads_path=READS):
    """Prepare all forecast weights without opening the target-score ledger."""
    reads = load_jsonl(reads_path)
    if len(reads) != 264:
        raise ValueError(f"registered support has {len(reads)} reads, expected 264")
    conn = connect_bundle(Path(bundle))
    try:
        events = list(conn.execute("SELECT event_id,event_date FROM events ORDER BY event_date,event_id"))
        vectors, metadata, admission = admitted_panel(conn)
    finally:
        conn.close()
    dates = dict(events)
    history = [(date, vectors.get(eid, {})) for eid, date in events]
    designs = []
    pair_blocks, pair_fields = Counter(), Counter()
    nonmarket_defined_dates = 0
    for read in reads:
        target_id, target_date = read["event_id"], read["date"]
        ids = list(read["candidate_ids"])
        details = read["structural"]["detail"]
        if len(ids) != len(details) or len(ids) != len(read["surface"]["distances"]):
            raise ValueError(f"frozen support arrays disagree for {target_id}")
        market = np.asarray([d["blocks"]["market"] for d in details], dtype=float)
        combined, nonmarket = [], []
        nonmarket_date_defined = True
        for cid, market_distance in zip(ids, market):
            panel_detail = nonmarket_distance(
                vectors.get(target_id, {}), vectors.get(cid, {}), history, target_date,
                metadata.get(target_id, {}), metadata.get(cid, {}),
            )
            if panel_detail is None:
                combined.append(float(market_distance))
                nonmarket.append(None)
                nonmarket_date_defined = False
                pair_blocks["market"] += 1
                continue
            blocks = dict(panel_detail["blocks"])
            if "market" in blocks:
                raise AssertionError("allowlisted panel unexpectedly contains the frozen market block")
            combined.append(float(np.mean([market_distance, *blocks.values()])))
            if panel_detail["n_fields"] >= MIN_FIELDS:
                nonmarket.append(float(panel_detail["distance"]))
            else:
                nonmarket.append(None)
                nonmarket_date_defined = False
            pair_blocks["market|" + "|".join(sorted(blocks))] += 1
            pair_fields.update(panel_detail["fields"])
        nonmarket_defined_dates += int(nonmarket_date_defined)
        surface = np.asarray(read["surface"]["distances"], dtype=float)
        availability = np.asarray(combined, dtype=float)
        vectors_to_match = {
            "market_matched": market,
            "availability_state_matched": availability,
            "event_class_matched": surface,
        }
        minima = {name: minimum_attainable_ess(d) for name, d in vectors_to_match.items()}
        common_target = min(
            float(len(ids)), max(float(read["structural_n_eff"]), *minima.values())
        )
        matched, calibration = {}, {}
        for name, distance in vectors_to_match.items():
            weights, temperature, achieved, boundary = calibrate_ess(distance, common_target)
            matched[name] = weights.tolist()
            calibration[name] = {
                "temperature": temperature, "effective_n": achieved,
                "minimum_attainable_n": minima[name], "boundary": boundary,
            }
        diagnostic = None
        if nonmarket_date_defined:
            nonmarket_distances = np.asarray(nonmarket, dtype=float)
            diagnostic = {
                "distances": nonmarket_distances.tolist(),
                "weights_tau_0_25": weights_at_temperature(nonmarket_distances, 0.25).tolist(),
            }
        designs.append({
            "event_id": target_id, "date": target_date, "read_hash": read["hash"],
            "candidate_ids": ids,
            "atoms_sha256": hashlib.sha256(canonical(
                read["forecasts"]["20"]["abnormal_atoms"]
            ).encode()).hexdigest(),
            "common_target_effective_n": common_target,
            "distances": {
                "market": market.tolist(), "availability_state": availability.tolist(),
                "event_class": surface.tolist(), "nonmarket": nonmarket,
            },
            "weights": {
                **matched,
                "uniform": (np.ones(len(ids)) / len(ids)).tolist(),
                "market_tau_0_25": weights_at_temperature(market, 0.25).tolist(),
                "availability_state_tau_0_25": weights_at_temperature(availability, 0.25).tolist(),
                "event_class_tau_0_25": weights_at_temperature(surface, 0.25).tolist(),
            },
            "calibration": calibration,
            "nonmarket_only_diagnostic": diagnostic,
        })
    admission["pairwise_field_counts"] = dict(sorted(pair_fields.items()))
    admission["pairwise_block_combination_counts"] = dict(sorted(pair_blocks.items()))
    admission["nonmarket_only_defined_on_all_candidates_dates"] = nonmarket_defined_dates
    return designs, admission


def _contrast(losses, arm_a, arm_b, dates, n_boot):
    result = paired_block(losses[arm_a], losses[arm_b], dates, n_boot)
    result["arm_a"], result["arm_b"] = arm_a, arm_b
    return result


def score_designs(designs, reads_path=READS, scores_path=SCORES, n_boot=2000):
    """Attach frozen outcomes only after every forecast weight has been prepared."""
    reads = load_jsonl(reads_path)
    scores = load_jsonl(scores_path)
    read_by_key = {(r["event_id"], r["date"]): r for r in reads}
    score_by_key = {(r["event_id"], r["date"]): r for r in scores}
    rows = []
    for design in designs:
        key = (design["event_id"], design["date"])
        read, score = read_by_key[key], score_by_key[key]
        if design["candidate_ids"] != read["candidate_ids"] or design["read_hash"] != score["read_hash"]:
            raise ValueError(f"frozen support or read hash changed for {key}")
        atoms = np.asarray(read["forecasts"]["20"]["abnormal_atoms"], dtype=float)
        if hashlib.sha256(canonical(atoms.tolist()).encode()).hexdigest() != design["atoms_sha256"]:
            raise ValueError(f"frozen atoms changed for {key}")
        outcome = float(score["outcome"])
        losses = {name: weighted_crps(atoms, np.asarray(weights), outcome)
                  for name, weights in design["weights"].items()}
        diagnostic = design.get("nonmarket_only_diagnostic")
        diagnostic_loss = None
        if diagnostic is not None:
            diagnostic_loss = weighted_crps(
                atoms, np.asarray(diagnostic["weights_tau_0_25"]), outcome
            )
        rows.append({**design, "outcome": outcome, "losses": losses,
                     "nonmarket_only_diagnostic_loss": diagnostic_loss})
    dates = [r["date"] for r in rows]
    loss_vectors = {name: np.asarray([r["losses"][name] for r in rows]) for name in rows[0]["losses"]}
    primary = {
        "availability_state_minus_market_matched": _contrast(
            loss_vectors, "availability_state_matched", "market_matched", dates, n_boot),
        "availability_state_minus_event_class_matched": _contrast(
            loss_vectors, "availability_state_matched", "event_class_matched", dates, n_boot),
    }
    adjusted = holm_adjust([x["dm"].get("p_value") for x in primary.values()])
    for result, p_adj in zip(primary.values(), adjusted):
        result["dm_p_holm"] = p_adj
        result["holm_reject_0_05"] = bool(p_adj < 0.05)
    diagnostic_rows = [r for r in rows if r["nonmarket_only_diagnostic_loss"] is not None]
    summary = {
        "registration": str(REGISTRATION.relative_to(ROOT)),
        "estimand": "schedule-imputed finalized-data sensitivity",
        "n_dates": len(rows), "n_boot": n_boot, "seed": SEED,
        "mean_loss": {name: float(np.mean(values)) for name, values in loss_vectors.items()},
        "median_effective_n": {
            name: float(np.median([effective_n(r["weights"][name]) for r in rows]))
            for name in rows[0]["weights"]
        },
        "primary": primary,
        "nonmarket_only_diagnostic": {
            "restricted_support": True,
            "n_dates": len(diagnostic_rows),
            "mean_loss": (float(np.mean([r["nonmarket_only_diagnostic_loss"] for r in diagnostic_rows]))
                          if diagnostic_rows else None),
            "median_effective_n": (float(np.median([
                effective_n(r["nonmarket_only_diagnostic"]["weights_tau_0_25"])
                for r in diagnostic_rows
            ])) if diagnostic_rows else None),
            "inference": None,
        },
    }
    return rows, summary


def publish(bundle=BUNDLE, reads_path=READS, scores_path=SCORES, out_dir=OUT, n_boot=2000):
    """Execute the registered publication run. Call explicitly exactly once."""
    if IMPLEMENTATION_COMMIT.startswith("TO_BE_"):
        raise RuntimeError("record the implementation commit before the publication run")
    designs, admission = prepare_designs(bundle, reads_path)
    rows, summary = score_designs(designs, reads_path, scores_path, n_boot)
    summary["field_admission"] = admission
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    scores_out, summary_out, admission_out = (
        out_dir / "scores.jsonl", out_dir / "summary.json", out_dir / "field_admission.json"
    )
    scores_out.write_text("".join(canonical(row) + "\n" for row in rows), encoding="utf-8")
    summary_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    admission_out.write_text(json.dumps(admission, indent=2) + "\n", encoding="utf-8")
    execution_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    inputs = [*(Path(bundle) / name for name in ("bundle_manifest.json", "events.csv", "market_observations.csv", "situation_state.csv")), reads_path, scores_path]
    manifest = {
        "frozen_release_commit": FROZEN_RELEASE_COMMIT,
        "registration_commit": REGISTRATION_COMMIT,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "execution_commit": execution_commit,
        "inputs": {str(Path(p).relative_to(ROOT)): file_hash(p) for p in inputs},
        "registration": {"path": str(REGISTRATION.relative_to(ROOT)), "sha256": file_hash(REGISTRATION)},
        "outputs": {p.name: file_hash(p) for p in (scores_out, summary_out, admission_out)},
        "note": "manifest.json cannot contain its own hash",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--fast", action="store_true", help="200 bootstrap draws; never publication output")
    args = parser.parse_args()
    print(json.dumps(publish(out_dir=args.out, n_boot=200 if args.fast else 2000), indent=2))


if __name__ == "__main__":
    main()
