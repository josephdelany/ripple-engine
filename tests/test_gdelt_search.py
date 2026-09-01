"""
test_gdelt_search.py -- the GDELT news-search PARSING is honest and robust (no network here;
the live call is exercised on the running server). The critical property: GDELT's 200 +
plain-text throttle body is detected as an error, never silently read as "no articles".

Run: python3 -m pytest -q tests/test_gdelt_search.py
"""

import gdelt_search as G


def test_gd1_rate_limit_body_is_detected_not_swallowed():
    body = "Your query volume is too high. Please limit your requests to one every 5 seconds."
    arts, err = G.parse_articles(body)
    assert arts is None and err == "rate_limited"


def test_gd2_valid_json_parses_articles():
    body = ('{"articles":[{"url":"http://a.com/x","title":"US strikes Iran",'
            '"domain":"a.com","seendate":"20260101T000000Z","language":"English",'
            '"sourcecountry":"US"}]}')
    arts, err = G.parse_articles(body)
    assert err is None and len(arts) == 1 and arts[0]["domain"] == "a.com"


def test_gd3_bad_json_is_an_error():
    arts, err = G.parse_articles("{not json")
    assert arts is None and err == "bad_response"


def test_gd4_norm_title_dedups_equivalent_titles():
    assert G._norm_title("US Strikes Iran!!") == G._norm_title("  us   strikes iran ")


def test_gd5_coverage_counts_diversity():
    arts = [{"domain": "a.com", "country": "US", "language": "English", "seendate": "20260101T00Z"},
            {"domain": "b.co.uk", "country": "UK", "language": "English", "seendate": "20260101T01Z"},
            {"domain": "a.com", "country": "US", "language": "English", "seendate": "20260102T00Z"}]
    c = G._coverage(arts)
    assert c["n_articles"] == 3 and c["n_domains"] == 2 and c["n_countries"] == 2
    assert c["top_domains"][0] == ("a.com", 2)
