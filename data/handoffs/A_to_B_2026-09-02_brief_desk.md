# Handoff A -> B, 2026-09-02 (Brief: desk surfaces on the Amendment-2 record)

Done in A's files (commits "Brief A-1..A-4"): /api/walk/summary passes summary.json through whole; the story
trust block and app section 5 show run walk_20260902T182828Z's tiers.daily numbers and the two §7 statuses
verbatim; the retired sr_outcome_90 rates carry the retired label with the live IES-90 frequencies beside them;
tests/test_demo_911.py (PATH Step 10) verifies the three demos from the sealed reads.

For B (not fixed by A, per the brief):
- PATH §3 D4 still reads PARTIAL for one reason: `tiers.daily.G.engine_vs` carries three references
  (climatology, frozen, random_analogs). The sealed reads already hold a `baselines.persistence` block, so the
  fourth G baseline the protocol lists is computed per read but not scored into the summary. Scoring it into
  `tiers.*.G.engine_vs.persistence` (and P likewise if the protocol says so) flips D4.
- The `M` tier block is keyed engine / frozen / M01..M12; the desk passes it through as-is now.
