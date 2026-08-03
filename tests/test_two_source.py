"""
test_two_source.py -- the two-source backfill verifier (V-Q7) cannot admit a fake or non-independent
source. The deterministic rule is the guardrail: a proposed second source is accepted ONLY if it is a
well-formed URL from a DIFFERENT publisher than the primary. Everything else must be rejected (-> Joe's
queue), so no fabricated or same-source URL can silently make the corpus "two-source".

Run:  python3 -m pytest -q tests/test_two_source.py
"""

import two_source_backfill as TS


def test_ts1_accepts_independent_source():
    ok, reason = TS.verify("https://digitallibrary.un.org/record/94220",
                            "https://www.history.com/this-day-in-history/august-2/iraq-invades-kuwait")
    assert ok is True and "independent" in reason


def test_ts2_rejects_same_publisher():
    # same registrable domain (rferl.org) as the primary -> NOT independent
    ok, reason = TS.verify("https://www.rferl.org/a/1090869.html",
                           "https://www.rferl.org/a/other-story.html")
    assert ok is False and "same publisher" in reason


def test_ts3_rejects_subdomain_of_same_publisher():
    # two different whitehouse archives are both archives.gov -> same publisher, not independent
    ok, _ = TS.verify("https://clintonwhitehouse6.archives.gov/x",
                      "https://georgewbush-whitehouse.archives.gov/y")
    assert ok is False


def test_ts4_rejects_malformed_and_empty():
    assert TS.verify("https://un.org/x", "not-a-url")[0] is False
    assert TS.verify("https://un.org/x", "")[0] is False
    assert TS.verify("https://un.org/x", "ftp://un.org/x")[0] is False   # wrong scheme


def test_ts5_registrable_domain():
    assert TS.registrable_domain("https://www.nytimes.com/2020/x") == "nytimes.com"
    assert TS.registrable_domain("https://en.wikipedia.org/wiki/x") == "wikipedia.org"
