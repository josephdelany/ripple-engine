"""panel.py -- the state panel: schema, writer, vintage-aware reader (WORLD_STATE_FRAMEWORK §2, §4; PATH Step 2).

    state_panel(entity_id, field, obs_date, value, value_text, unit, source, vintage, release, retrospective, retrieved_at)

One table in data/oil.db (the one canonical database), named by PATH.md/BUILD_V3.md. Every row carries
a non-null `vintage` (when the value was knowable) and a non-null `release` (the dataset release parsed)
-- WORLD_STATE_CODEBOOK.md WS-R1 + Amendment 1 -- and the engine at date t reads a field only through
`value_at(..., t)`, which sees rows with vintage <= t (framework §4.3).
Loaders in src/state/<source>.py call `write()`; nothing here fetches anything.
"""
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
DB = DATA / "oil.db"
RAW = DATA / "state" / "raw"          # free downloads, gitignored (rebuilt by the loaders)
LOCAL = DATA / "state" / "local"      # licence-restricted files, gitignored, README stubs committed
CODEBOOK = ROOT / "docs" / "reference" / "WORLD_STATE_CODEBOOK.md"   # moved by the 74->6 root
                                                                     # restructure; path only
sys.path.insert(0, str(ROOT / "src"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS state_panel (
    entity_id    TEXT NOT NULL,          -- world | opec | region.<x> | country.<corpus id or iso3> | dyad.<a>__<b>
    field        TEXT NOT NULL,          -- WORLD_STATE_CODEBOOK.md field id
    obs_date     TEXT NOT NULL,          -- ISO date the value refers to (annual: YYYY-01-01, WS-R2)
    value        REAL,
    value_text   TEXT,
    unit         TEXT,
    source       TEXT NOT NULL,          -- dataset + version
    vintage      TEXT NOT NULL,          -- when the value was knowable (WS-R1 as amended); never null
    release      TEXT NOT NULL,          -- the dataset release parsed (Last-Modified / version date); never null
    retrospective INTEGER NOT NULL DEFAULT 0,   -- 1 = a later construction, not a contemporaneous record
    retrieved_at TEXT NOT NULL,
    PRIMARY KEY (entity_id, field, obs_date, vintage)
);
CREATE INDEX IF NOT EXISTS idx_state_panel_field ON state_panel(field, entity_id, obs_date);
"""


def connect(db=DB):
    conn = sqlite3.connect(db, timeout=30)
    ensure_schema(conn)
    return conn


def ensure_schema(conn):
    conn.executescript(SCHEMA)
    conn.commit()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ----------------------------------------------------------------------------- codebook

def codebook():
    """{field: {block, unit, resolution, source, coverage, licence, rule_id}} parsed from the codebook."""
    out = {}
    cols = ["block", "field", "unit", "resolution", "source", "coverage", "licence", "rule_id"]
    for line in CODEBOOK.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| block") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 8:
            r = dict(zip(cols, cells))
            out[r["field"]] = r
    return out


# ----------------------------------------------------------------------------- write

def write(conn, rows, replace=True):
    """Insert rows (dicts with entity_id, field, obs_date, value|value_text, unit, source, vintage).
    Refuses a null vintage or an unregistered field. Returns the number of rows written."""
    cb = codebook()
    ts = now()
    out = []
    for r in rows:
        if not r.get("vintage") or not r.get("release"):
            raise ValueError(f"vintage/release is null for {r.get('field')}/{r.get('entity_id')}/{r.get('obs_date')} (WS-R1)")
        if r["field"] not in cb:
            raise ValueError(f"field '{r['field']}' is not in WORLD_STATE_CODEBOOK.md (WS-R1: register before loading)")
        v = r.get("value")
        if v is not None and pd.isna(v):
            v = None
        vt = r.get("value_text")
        if v is None and vt is None:
            continue                                            # WS-R3: missing = absent row
        out.append((r["entity_id"], r["field"], str(r["obs_date"])[:10], None if v is None else float(v), vt,
                    r.get("unit") or cb[r["field"]]["unit"], r["source"], str(r["vintage"])[:10], str(r["release"])[:10],
                    1 if r.get("retrospective") else 0, ts))
    verb = "INSERT OR REPLACE" if replace else "INSERT OR IGNORE"
    conn.executemany(f"{verb} INTO state_panel VALUES (?,?,?,?,?,?,?,?,?,?,?)", out)
    conn.commit()
    return len(out)


# ----------------------------------------------------------------------------- read (vintage-aware)

def value_at(conn, entity_id, field, t):
    """The value of `field` for `entity_id` as known at date t: the latest obs_date <= t among rows
    whose vintage <= t; for that obs_date, the latest such vintage. None if nothing was knowable."""
    t = str(t)[:10]
    row = conn.execute(
        "SELECT obs_date, value, value_text, vintage, source, unit, release, retrospective FROM state_panel "
        "WHERE entity_id=? AND field=? AND obs_date<=? AND vintage<=? "
        "ORDER BY obs_date DESC, vintage DESC LIMIT 1", (entity_id, field, t, t)).fetchone()
    if not row:
        return None
    return {"obs_date": row[0], "value": row[1], "value_text": row[2], "vintage": row[3], "source": row[4], "unit": row[5],
            "release": row[6], "retrospective": bool(row[7])}


def state_at(conn, t, entities=None, fields=None):
    """Every (entity, field) knowable at t -> value_at(). Restricted to `entities`/`fields` if given."""
    t = str(t)[:10]
    q = "SELECT DISTINCT entity_id, field FROM state_panel WHERE obs_date<=? AND vintage<=?"
    args = [t, t]
    if entities:
        q += f" AND entity_id IN ({','.join('?' * len(entities))})"; args += list(entities)
    if fields:
        q += f" AND field IN ({','.join('?' * len(fields))})"; args += list(fields)
    out = {}
    for e, f in conn.execute(q, args):
        v = value_at(conn, e, f, t)
        if v is not None:
            out.setdefault(e, {})[f] = v
    return out


# ----------------------------------------------------------------------------- coverage

def coverage(conn):
    """Rows per block per decade + per field summary. Published as computed by src/state/status.py."""
    cb = codebook()
    df = pd.read_sql("SELECT field, entity_id, obs_date, vintage, source FROM state_panel", conn)
    if df.empty:
        return {"blocks": {}, "fields": {}, "n_rows": 0}
    df["block"] = df["field"].map(lambda f: cb.get(f, {}).get("block", "?"))
    df["decade"] = (df["obs_date"].str[:4].astype(int) // 10 * 10).astype(str) + "s"
    blocks = df.groupby(["block", "decade"]).size().unstack(fill_value=0)
    fields = df.groupby("field").agg(n=("obs_date", "size"), entities=("entity_id", "nunique"),
                                     first_obs=("obs_date", "min"), last_obs=("obs_date", "max"),
                                     vintages=("vintage", "nunique"), source=("source", "first"))
    return {"blocks": {b: {d: int(v) for d, v in row.items()} for b, row in blocks.iterrows()},
            "fields": {f: {"n": int(r["n"]), "entities": int(r["entities"]), "first": r["first_obs"], "last": r["last_obs"],
                           "vintages": int(r["vintages"]), "source": r["source"]} for f, r in fields.iterrows()},
            "n_rows": int(len(df))}


# ----------------------------------------------------------------------------- loader helpers

def raw_path(source, filename):
    p = RAW / source / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def local_path(source, filename):
    return LOCAL / source / filename


def fetch_file(url, dest, timeout=180, force=False):
    """Download `url` to `dest` once (cached), recording the HTTP Last-Modified beside it as the file's
    vintage evidence. Returns (path, meta). Raises on HTTP error; never substitutes."""
    import requests
    dest = Path(dest)
    meta_p = Path(str(dest) + ".meta.json")
    if dest.exists() and meta_p.exists() and not force:
        return dest, json.loads(meta_p.read_text())
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 (ripple-engine research)"}, stream=True)
    r.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(1 << 16):
            f.write(chunk)
    meta = {"url": url, "last_modified": r.headers.get("Last-Modified"), "date": r.headers.get("Date"),
            "content_type": r.headers.get("Content-Type"), "bytes": dest.stat().st_size, "retrieved_at": now()}
    meta_p.write_text(json.dumps(meta, indent=1))
    return dest, meta


def knowable_annual(year):
    """An annual value for year Y is knowable on 1 January of Y+1 (Amendment 1)."""
    return f"{int(year) + 1}-01-01"


def knowable_month(d):
    """A monthly value for month m is knowable on the first day of the following month."""
    d = pd.Timestamp(d)
    return (d + pd.offsets.MonthBegin(1)).date().isoformat() if d.day == 1 else (d + pd.offsets.MonthBegin(1)).date().isoformat()


def vintage_from(meta, fallback):
    """The dataset RELEASE date (Amendment 1): the file's HTTP Last-Modified (a real date the server asserts
    for the file parsed), else the documented release date of the version. Never null."""
    for key in ("last_modified", "date"):                     # Last-Modified first; else the server's Date for the file served
        lm = (meta or {}).get(key)
        if lm:
            try:
                return datetime.strptime(lm, "%a, %d %b %Y %H:%M:%S %Z").date().isoformat()
            except ValueError:
                pass
    if not fallback:
        raise ValueError("no vintage available (WS-R1)")
    return fallback


class MissingInput(Exception):
    """A licence-restricted file or an API key is absent: the loader stubs with instructions (never a fake)."""


def require_local(source, filename, instructions):
    p = local_path(source, filename)
    if not p.exists():
        raise MissingInput(f"{p.relative_to(ROOT)} is absent. {instructions}")
    return p


def require_env(name, instructions):
    import os
    v = os.environ.get(name)
    if not v:
        raise MissingInput(f"environment variable {name} is not set. {instructions}")
    return v


def report(source, n, fields, note=""):
    print(f"{source}: {n} rows -> state_panel ({', '.join(sorted(set(fields)))}){(' -- ' + note) if note else ''}")
