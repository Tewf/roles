#!/usr/bin/env bash
# For each repository and term: the number of files GitHub code search finds that hold the term. 7 s apart (limit 10 per minute).
echo -e "repo\tterm\tfiles" > absence.tsv
for r in FoundationAgents/MetaGPT OpenBMB/ChatDev camel-ai/camel crewAIInc/crewAI microsoft/autogen OpenHands/OpenHands; do
  for t in 'lean4' 'wilson' '"confidence interval"' '"formal verification"' '"autonomy level"' '"standard operating procedure"'; do
    c=$(gh api -X GET search/code -f q="repo:$r $t" --jq '.total_count' 2>/dev/null || echo "failed")
    echo -e "$r\t$t\t$c" >> absence.tsv; sleep 7
  done
done
