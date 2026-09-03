import verify_submission as V


def test_authoritative_local_links_resolve():
    assert V.broken_links() == []
