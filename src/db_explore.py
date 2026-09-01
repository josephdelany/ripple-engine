"""
db_explore.py -- a HARD read-only explorer for the engine database (data/oil.db).

Lets Joe browse and query the actual engine DB from the Desk, without any risk of a
write. Read-only is enforced FOUR ways, belt-and-suspenders, because the canonical DB
is append-only and sacred (INV-2):
  1. a `mode=ro` URI connection (the OS/file handle is opened read-only);
  2. `PRAGMA query_only = 1` (the engine refuses writes on this connection);
  3. a statement AUTHORIZER that permits only SELECT / READ / FUNCTION and DENIES
     everything else (INSERT/UPDATE/DELETE/ATTACH/PRAGMA/CREATE/DROP...);
  4. only single SELECT/WITH statements are accepted; a row cap and a wall-clock
     interrupt bound cost.
A query that tries to write, attach, or run multiple statements is rejected, not run.
Table names are validated against the live schema (no string interpolation of user input
into a name without a whitelist check).
"""

import sqlite3
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ROW_CAP = 500                # max rows returned from a free query
PAGE_CAP = 200               # max rows per table-browse page
TIMEOUT_S = 4.0              # wall-clock interrupt for a runaway query


def _ro_conn():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=5)
    conn.execute("PRAGMA query_only = 1")
    return conn


def _table_names(conn):
    return {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}


def tables():
    """Every table with its row count and column names -- the map of the engine DB."""
    conn = _ro_conn()
    out = []
    for name in sorted(_table_names(conn)):
        try:
            n = conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        except sqlite3.Error:
            n = None
        cols = [r[1] for r in conn.execute(f'PRAGMA table_info("{name}")')]
        out.append({"name": name, "rows": n, "columns": cols})
    conn.close()
    return out


def rows(table, limit=50, offset=0):
    """A page of rows from one table (validated name, capped, read-only)."""
    conn = _ro_conn()
    if table not in _table_names(conn):
        conn.close()
        return {"error": f"no table {table!r}"}
    cols = [r[1] for r in conn.execute(f'PRAGMA table_info("{table}")')]
    lim = min(max(int(limit), 1), PAGE_CAP)
    off = max(int(offset), 0)
    rs = conn.execute(f'SELECT * FROM "{table}" LIMIT ? OFFSET ?', (lim, off)).fetchall()
    total = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    conn.close()
    return {"table": table, "columns": cols, "rows": [list(r) for r in rs],
            "total": total, "limit": lim, "offset": off}


def _authorizer(action, *_a):
    # Permit only reads; deny writes/DDL/attach/pragma/etc.
    if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def query(sql):
    """Run ONE read-only SELECT/WITH query. Guarded by an authorizer + row cap + timeout.
    Anything that isn't a single read is rejected with a plain reason."""
    sql = (sql or "").strip().rstrip(";")
    if not sql:
        return {"error": "empty query"}
    if not sql.lower().startswith(("select", "with")):
        return {"error": "only SELECT / WITH queries are allowed (read-only explorer)"}
    if ";" in sql:
        return {"error": "one statement only"}
    conn = _ro_conn()
    conn.set_authorizer(_authorizer)
    timer = threading.Timer(TIMEOUT_S, conn.interrupt)
    timer.start()
    try:
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rs = cur.fetchmany(ROW_CAP)
        return {"columns": cols, "rows": [list(r) for r in rs], "n": len(rs),
                "capped": len(rs) >= ROW_CAP}
    except sqlite3.Error as e:
        return {"error": str(e)[:200]}
    finally:
        timer.cancel()
        conn.set_authorizer(None)
        conn.close()
