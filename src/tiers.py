"""
tiers.py -- the ONE tiering vocabulary, imported by every surface so a null can never read as an edge.

The whole product rests on honest labels. Today each surface (digest, cockpit, MCP, research) decides
"validated vs null" in its own prose; that risks the same claim being labelled two ways. This module
is the single source of truth: five tiers, one classifier, one renderer. Every number a surface shows
should go through render_number() so it always carries its tier and (if known) its receipt id.

The tiers, from strongest to weakest:
  validated    -- passed the full gate: CI excludes 0 AND survives multiple-testing correction
                  (and, where checked, robustness). A CLAIM you can stand behind.
  suggestive   -- leans the predicted way but small-N, or direction defined in-sample, or not
                  family-wise corrected. NOT a claim -- a lead.
  null         -- tested and did not survive. Reported, never hidden. NOT a claim.
  insufficient -- too few usable events (n < MIN_N) to test at all. NOT a claim.
  descriptive  -- a readout / context only (a percentile, an analogue distribution). NEVER an
                  amplifier or a forecast.
"""

MIN_N = 12                              # matches research.run_test's floor

TIERS = {
    "validated":    "CI excludes 0 AND survives multiple-testing correction (a claim).",
    "suggestive":   "leans the right way but small-N / in-sample / uncorrected (a lead, not a claim).",
    "null":         "tested and did not survive (reported, not hidden).",
    "insufficient": f"too few usable events (n < {MIN_N}) to test.",
    "descriptive":  "a readout / context only; never an amplifier or forecast.",
}
ORDER = ["validated", "suggestive", "null", "insufficient", "descriptive"]
BADGE = {"validated": "[VALIDATED]", "suggestive": "[suggestive]", "null": "[null]",
         "insufficient": "[insufficient]", "descriptive": "[descriptive]"}


def tier_of(claim):
    """Derive the tier from a claim dict using the SAME fields everywhere, so H2-at-n=20 and
    H2-at-N=88 can never be labelled inconsistently. Recognized fields (any subset):
      statistically_validated / validated (bool), ci_excludes_zero (bool), survives_fdr (bool),
      n (int), suggestive (bool), kind == 'descriptive'."""
    if not isinstance(claim, dict):
        return "descriptive"
    if claim.get("kind") == "descriptive" or claim.get("descriptive"):
        return "descriptive"
    n = claim.get("n")
    if n is not None and n < MIN_N and not claim.get("validated") and not claim.get("statistically_validated"):
        return "insufficient"
    if claim.get("statistically_validated") or claim.get("validated"):
        return "validated"
    if claim.get("suggestive"):
        return "suggestive"
    # a corrected, CI-excludes-zero survivor is validated; a bare in-sample lean is suggestive
    if claim.get("ci_excludes_zero") and claim.get("survives_fdr"):
        return "validated"
    if claim.get("ci_excludes_zero"):
        return "suggestive"
    return "null"


def render_number(value, unit="", tier="descriptive", claim_id=None):
    """The canonical way to show a number: value + unit + tier badge + (optional) receipt id.
    No surface should print a bare number -- always route it through here."""
    if value is None:
        v = "n/a"
    elif isinstance(value, float):
        v = f"{value:+.2f}" if abs(value) < 1000 else f"{value:+.0f}"
    else:
        v = str(value)
    out = f"{v}{unit} {BADGE.get(tier, '')}".rstrip()
    if claim_id:
        out += f" ({claim_id})"
    return out
