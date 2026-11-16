#!/usr/bin/env python3
"""Forward citations on OpenAlex: works that cite W-ID and match a title-and-abstract string. python3 forward.py W4385963839 'verification OR reliability' [n]"""
import json, sys, urllib.parse, urllib.request
wid, q = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": f"cites:{wid},title_and_abstract.search:{q}", "per-page": n, "sort": "cited_by_count:desc", "select": "title,publication_year,cited_by_count,doi"})
d = json.loads(urllib.request.urlopen(u, timeout=40).read())
print("count", d["meta"]["count"])
for w in d["results"]:
    print(f"  {w['publication_year']} c={w['cited_by_count']} {w['title'][:100]} | {w['doi']}")
