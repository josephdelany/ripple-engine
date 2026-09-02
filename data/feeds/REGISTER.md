# Feed register — every source the watcher reads (Brief A-10, 2026-09-02)

Keyless only. "Verified" = fetched by session A on the date shown and parsed to ≥1 item (or, for an API, a documented
reply). A feed that fails the probe is listed with its failure, never silently kept or silently dropped.
Dedupe: the watcher keys every item on **URL + normalised title** (`watcher.is_new`), so a story syndicated under
one URL with two titles, or two URLs with one title, is surfaced once. The materiality gate is unchanged.

| feed | URL | format | domain | verified | status |
|---|---|---|---|---|---|
| bbc_world | https://feeds.bbci.co.uk/news/world/rss.xml | RSS | war & conflict | 2026-08-03 (TASK_BRIEF_12) | live, in `data/watch_feeds.txt` |
| aljazeera | https://www.aljazeera.com/xml/rss/all.xml | RSS | war & conflict | 2026-08-03 | live |
| un_news | https://news.un.org/feed/subscribe/en/news/all/rss.xml | RSS | geopolitics | 2026-09-02: 200, 30 items | live |
| eia_energy (EIA Today in Energy) | https://www.eia.gov/rss/todayinenergy.xml | RSS | energy | 2026-09-02: 200, 11 items | live |
| fed_press | https://www.federalreserve.gov/feeds/press_all.xml | RSS | macro | 2026-08-03 | live |
| oilprice | https://oilprice.com/rss/main | RSS | energy | 2026-08-03 | live |
| mining_tech | https://www.mining-technology.com/feed/ | RSS | metals | 2026-08-03 | live |
| gcaptain | https://gcaptain.com/feed/ | RSS | shipping | 2026-08-03 | live |
| freightwaves | https://www.freightwaves.com/feed | RSS | shipping | 2026-08-03 | live |
| timesofisrael | https://www.timesofisrael.com/feed/ | RSS | Middle East | 2026-08-03 | live |
| gdelt_events (GDELT 2.0 event export, 15-min) | http://data.gdeltproject.org/gdeltv2/lastupdate.txt | TSV zip | all | since TASK_BRIEF_12 | live (`watcher.run_gdelt`) |
| **gdelt_doc (GDELT DOC 2.0 API)** | https://api.gdeltproject.org/api/v2/doc/doc?query=…&mode=artlist&format=json&timespan=… | JSON | all (news articles, 15-min) | 2026-09-02: endpoint answers; **rate limit: one request per 5 s** (HTTP 429 text: "Please limit requests to one every 5 seconds"); keywords shorter than 3 chars rejected | added: `watcher.run_gdelt_doc`, one query per registered term, 5 s apart; terms of use per gdeltproject.org (free, attribution) |
| OPEC press releases RSS | https://www.opec.org/opec_web/en/press_room/rss.xml (and two variants) | — | energy | 2026-09-02: HTTP 403 Cloudflare "Just a moment" to scripts | **not added** (also dead at TASK_BRIEF_12) |
| IEA news RSS | https://www.iea.org/news.rss, https://www.iea.org/rss/news.xml | — | energy | 2026-09-02: HTTP 403 Cloudflare | **not added** |
