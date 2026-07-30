"""
_fetch.py -- HTTP GET with retry/backoff, so a transient network blip self-heals instead of logging
a FAILED step.

The network fetchers (FRED, EIA, GDELT, RSS, conflict-intensity) all hit free public endpoints that
occasionally time out, 429, or 5xx under load. Wrapping them in bounded exponential backoff turns a
transient hiccup into a silent recovery -- and keeps the "a dead source never blocks the rest"
guarantee, because after the last retry we raise and the caller's step is isolated as before.

stdlib-only fallback: if `requests` isn't importable, use urllib so this never adds a hard dependency.
"""

import time
import urllib.request

try:
    import requests
    _HAS_REQUESTS = True
except Exception:                       # pragma: no cover
    _HAS_REQUESTS = False

RETRYABLE = {429, 500, 502, 503, 504}


def get_with_retry(url, *, tries=3, base=2.0, timeout=30, headers=None):
    """GET `url`, retrying on connection/timeout errors and retryable status codes with jitter-free
    exponential backoff (base, base*2, base*4, ...). Raises the last error after `tries` attempts."""
    last = None
    for attempt in range(tries):
        try:
            if _HAS_REQUESTS:
                r = requests.get(url, timeout=timeout, headers=headers or {})
                if r.status_code in RETRYABLE:
                    raise IOError(f"HTTP {r.status_code}")
                r.raise_for_status()
                return r.text
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as e:               # noqa: BLE001 -- deliberately broad; we retry then re-raise
            last = e
            if attempt < tries - 1:
                time.sleep(base * (2 ** attempt))
    raise last
