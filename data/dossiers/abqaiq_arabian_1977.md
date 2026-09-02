# Fire at Saudi Abqaiq processing facility disrupts output     abqaiq_arabian_1977 · 1977-05-11 · day · infrastructure_attack

## Sources

**No source was retrieved and verified in this session.** Per the no-fabrication rule, no citation, quote, or number is offered for this event. What follows is a record of every retrieval route attempted, so the gap is documented rather than silently left blank.

| Route tried | Result |
|---|---|
| `history.state.gov` FRUS 1969–76 Vol. XXXVII (*Energy Crisis, 1974–1980*), Chapter 4 ("Strategies To Cope With High Oil Prices, February 1977–January 1979", Docs. 117–180) | Fetched the chapter's document list. No document dated May 1977 exists in this chapter — it jumps from April 25, 1977 (Doc. 122) to June 7, 1977 (Doc. 123). No FRUS document covers this event. |
| `washingtonpost.com` archive, "Fire in Pipeline Still Restricting Saudi Oil Output" (dated by the URL May 13, 1977) and "Oil Fire Continues" (dated by the URL May 14, 1977) | Both returned HTTP 403 to WebFetch. Never opened; not cited. |
| `nytimes.com` archive, a candidate May 12, 1977 article | WebFetch tool refuses `nytimes.com` outright (host-level block). Never opened; not cited. |
| `digital.bentley.umich.edu` (Michigan Daily student-newspaper digitization, a possible wire-service reprint) | Returned HTTP 403 on two different sub-paths. Never opened; not cited. |
| CIA FOIA Electronic Reading Room search | Per `SPINE_REGISTRATION.md` §4, already known to return the site homepage with no results; confirmed again this session with a search for a specific 1977 Abqaiq document — no working document link surfaced. |
| `govinfo.gov`, Senate Foreign Relations Committee print *The future of Saudi Arabian oil production* (96th Cong., 1979) | PDF located but exceeds the fetch tool's 10 MB size limit; an HTML rendering does not exist (`.../html/....htm` returns "Page Not Found"). Content not read; not cited. |
| `govinfo.gov`, `CHRG-95shrg36145.pdf` (a 95th-Congress Senate hearing, title unconfirmed) | Also exceeds the fetch tool's size limit. Content not read; not cited. |
| CSIS, "The Impact of the Abqaiq Attack on Saudi Energy Security" (Al-Rodhan, Feb. 2006) | Retrieved in full (8 pages). Confirmed on inspection to be entirely about the February 24, 2006 attempted al-Qaeda attack on Abqaiq — it does not mention 1977 anywhere in its text or footnotes. Not usable for this event. |
| `archive.org` full-text search, EIA petroleum chronology, Aramco World magazine archive, Trove (National Library of Australia) | Searched; no working document link surfaced for any of them. |

`WebSearch` (not a citable retrieval tool under this project's rules, since it returns an AI-generated summary of pages this session never itself opened) surfaced consistent claims across several outlets — a pipeline/pumping-station fire on approximately May 13, 1977 killing one Aramco employee, injuring thirteen, and the Aramco president attributing it to pipeline failure rather than sabotage — but none of this is fetched, verbatim text, and per this project's rule that a WebSearch summary is never a substitute for an actual retrieval, **none of it is repeated here as fact.** It is noted only so that a future session knows what specific claims to go verify.

## Narrative

Not written. SPINE_REGISTRATION.md §1(b) requires every factual claim in the narrative to carry a `[Sn]` marker resolving to a retrieved source. With zero sources retrieved this session, no claim can be made. The existing database description ("Fire at Saudi Abqaiq processing facility disrupts output") is asserted by the record itself, not by anything fetched in this session, and is not repeated here as if sourced.

## Knowable at

Cannot be established. No source retrieved this session confirms the fire occurred on 1977-05-11 specifically, at what time, or when it became public knowledge. The `event_date` field's current value cannot be confirmed or refuted from this session's work.

## Entities

- `country.saudi_arabia` — actor and target (per the current `event_entities` rows) — **not confirmed by any source retrieved this session.** If the underlying event was an accidental pipeline failure (an unverified claim above), coding Saudi Arabia as `actor` is itself questionable — an accident has no actor in the codebook's sense of "who did it." This cannot be resolved without a retrieved source.

## Class

Proposed class under review: `infrastructure_attack`. Codebook clause: "`infrastructure_attack` | Direct strike on production, refining, or export infrastructure." The word "strike" here means an attack, not an accident. **This dossier cannot answer the class question the task poses** — whether an accidental fire belongs in a class defined as a direct strike — because no retrieved source in this session establishes whether the fire was accidental, sabotage, or something else. The unverified WebSearch claims noted above (Aramco's president attributing it to "pipeline failure," an accident) point toward the class being wrong, but a claim this consequential — reclassifying or removing an event from the corpus — must not rest on an unfetched search summary. This is the single most important gap in this dossier and should be the first thing resolved before Joe applies any patch to this record.

## Not known at the time

Cannot be established without a source. In particular: whether the fire was accidental or deliberate was reportedly disputed even at the time (per the same unverified claims above — American diplomats said sabotage was "being investigated" while Aramco's president denied it) — if that turns out to be correct once sourced, it means severity and surprise could not have been coded with confidence on the day itself either, which bears on both fields once a source exists.

## Proposed field changes

None proposed. Per SPINE_REGISTRATION.md §3, "a field that no source supports is never proposed." Every field on this record — description, severity, surprise, source_url, class — currently rests on no source retrieved in this session, and the codebook's sourced-or-unknown rule means the honest state of every one of them is `unknown`, not a specific alternative value.

## Status

**partial — fails (a), (b), (c), (e) and (f).** Zero independent sources were retrieved and verified this session (fails a). No sourced narrative exists (fails b). `knowable_at` cannot be set (fails c). The class question posed for this event — attack vs. accident — is explicitly unresolved (fails e). "Not known at the time" cannot be written without a source (fails f). Entities (d) are unchanged from the existing record and not independently confirmed. This is a genuine dead end for this session's retrieval routes, not a low-effort search: eleven distinct routes were attempted (table above) and all either returned no usable content, were blocked, or exceeded size limits. The next session should try a route with authenticated newspaper-archive access (ProQuest, NYT TimesMachine, or Joe manually retrieving the two Washington Post URLs above, which a logged-in browser session could likely open) rather than repeating the free-web routes tried here.
