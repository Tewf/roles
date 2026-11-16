#!/usr/bin/env python3
"""Look titles up on OpenAlex (no identity sent): print year, citations, DOI of the best match. python3 lookup.py 'title' ..."""
import json, sys, time, urllib.parse, urllib.request
for t in sys.argv[1:]:
    u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": "title.search:" + t, "per-page": 3, "sort": "cited_by_count:desc", "select": "id,title,publication_year,cited_by_count,doi"})
    try:
        d = json.loads(urllib.request.urlopen(u, timeout=40).read())["results"]
    except Exception as e:
        print(f"{t} -> failed: {e}"); continue
    print(f"## {t}")
    for w in d[:2]:
        print(f"   {w['publication_year']} c={w['cited_by_count']} {w['title'][:90]} | {w['doi']} | {w['id'].rsplit('/',1)[-1]}")
    time.sleep(0.5)
