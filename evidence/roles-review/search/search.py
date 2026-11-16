#!/usr/bin/env python3
"""Run one search string on one engine; print the count and the top results. No identity is sent.

    python3 search.py arxiv 'ti:"multi-agent" AND abs:"language model" AND ti:survey' [n]
    python3 search.py openalex 'title_and_abstract.search' '"multi-agent" "language model" survey' [n]
arXiv: the string is the raw search_query, sorted by relevance. OpenAlex: filter field and string, sorted by citations.
"""
import json, sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET

import time
def get(url):
    for wait in (4, 15, 40):          # arXiv asks for one request per 3 s; retry on 429
        time.sleep(wait if "arxiv" in url else 1)
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    raise SystemExit("rate limited (429) after three tries: not run")

engine = sys.argv[1]
if engine == "arxiv":
    q = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    u = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": n, "sortBy": "relevance"})
    root = ET.fromstring(get(u)); ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
    print("count", root.find("o:totalResults", ns).text)
    for e in root.findall("a:entry", ns):
        t = " ".join(e.find("a:title", ns).text.split()); i = e.find("a:id", ns).text.rsplit("/", 1)[-1]; y = e.find("a:published", ns).text[:4]
        print(f"  {i} {y} {t[:120]}")
else:
    field, q = sys.argv[2], sys.argv[3]; n = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": f"{field}:{q}", "per-page": n, "sort": "cited_by_count:desc"})
    d = json.loads(get(u)); print("count", d["meta"]["count"])
    for w in d["results"]:
        print(f"  {w.get('publication_year')} c={w['cited_by_count']} {(w['title'] or '')[:100]} {w.get('doi') or ''}")
