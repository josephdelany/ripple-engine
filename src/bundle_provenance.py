"""Where reproducibility stops: the committed bundle versus the database it came from.

The central experiment reproduces byte-for-byte from three committed CSVs, and
`src/reproduce_structural_surface.py` proves that.  This module checks the step *before* it —
whether those CSVs can still be traced to the database that produced them — because that is the
boundary the paper has to state and the one a reader cannot check for themselves.

Two different questions, and the difference is the whole point:

  1. Do the committed CSVs still match the hashes recorded in `bundle_manifest.json`?
     This must always be yes.  A no means the committed inputs were edited after freezing, which
     would silently invalidate every frozen number.  That is a defect and this script exits 1.

  2. Does the database recorded in that manifest still exist here, with the same hash?
     The honest answer today is no, and that is NOT a defect — `data/oil.db` is gitignored,
     parts of its source chain are keyed or licence-gated, and it is still being written to by
     other work in this repository.  It is a documented limit on what a reader can verify.  This
     script reports it as `diverged` or `absent` rather than staying quiet about it.

Reporting (2) as a status rather than a sentence in a document is deliberate: a sentence goes
stale silently, a checked status cannot.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "data" / "structural_surface" / "input"
MANIFEST = BUNDLE / "bundle_manifest.json"
SOURCE_DB = ROOT / "data" / "oil.db"

# Statuses for the upstream database.  Only `reproduced` means a reader could rebuild the CSVs
# and check them; the other two are boundaries the paper must disclose.
REPRODUCED = "reproduced"   # the recorded database is present and hashes identically
DIVERGED = "diverged"       # a database is present but is not the one the bundle came from
ABSENT = "absent"           # no database here at all (the state of any clean clone)


def file_hash(path):
    """SHA-256 of a file, read in chunks so a 240 MB database does not land in memory."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bundle_files():
    """Each committed CSV checked against the hash and row count frozen in the manifest."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = {}
    for name, want in manifest["files"].items():
        path = BUNDLE / name
        if not path.exists():
            out[name] = {"present": False, "ok": False}
            continue
        got = file_hash(path)
        # The manifest stores the data row count, so the header line is not counted.
        rows = sum(1 for _ in path.open(encoding="utf-8")) - 1
        out[name] = {"present": True, "expected_sha256": want["sha256"], "actual_sha256": got,
                     "expected_rows": want["rows"], "actual_rows": rows,
                     "ok": got == want["sha256"] and rows == want["rows"]}
    return out


def upstream():
    """The database the bundle was exported from: present and identical, present and different, or gone."""
    recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))["source_database_sha256"]
    if not SOURCE_DB.exists():
        return {"status": ABSENT, "recorded_sha256": recorded, "local_sha256": None,
                "note": "data/oil.db is gitignored; a clean clone reaches this state and cannot "
                        "rebuild the bundle from source."}
    local = file_hash(SOURCE_DB)
    if local == recorded:
        return {"status": REPRODUCED, "recorded_sha256": recorded, "local_sha256": local,
                "note": "the exporting database is present and unchanged."}
    return {"status": DIVERGED, "recorded_sha256": recorded, "local_sha256": local,
            "note": "a database is present but is not the one the bundle was exported from; it has "
                    "been written to since. The frozen CSVs remain the authoritative inputs."}


def report():
    files = bundle_files()
    return {"bundle_files": files, "upstream_database": upstream(),
            "bundle_intact": all(x["ok"] for x in files.values())}


def main():
    r = report()
    print(json.dumps(r, indent=2))
    up = r["upstream_database"]["status"]
    if not r["bundle_intact"]:
        # This is the only failure mode. The committed inputs are the experiment's ground truth.
        raise SystemExit("committed input bundle does not match bundle_manifest.json")
    print(f"committed input bundle: INTACT · upstream database: {up.upper()}")
    if up != REPRODUCED:
        print("Reproducibility boundary: the frozen experiment reproduces from the committed CSVs; "
              "those CSVs cannot be re-derived and checked from a verifiable upstream source here. "
              "See docs/audit/PROVENANCE_BOUNDARY.md.")


if __name__ == "__main__":
    main()
