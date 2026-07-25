# The Daily — reading the front page

Open **http://127.0.0.1:5050/digest** in a browser (the backend re-renders it on
each request; `python3 src/digest.py` also writes a static `data/digest.html`).

Phone access (OFF by default, Joe's explicit choice only): the backend binds
`127.0.0.1` so The Daily is local-only. To reach it from a phone on the same
network you would change the last line of `src/backend.py` from
`host="127.0.0.1"` to `host="0.0.0.0"` — this exposes it on your LAN with no auth.
Do not do this unless you mean to; it is not done here.
