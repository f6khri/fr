# B2B SaaS YouTube Content Strategy: Research Repository

## Topic
**YouTube Content Strategy for B2B SaaS**

How do the best B2B SaaS practitioners actually use YouTube as a growth and marketing channel? This research collects primary source material, including video transcripts and LinkedIn posts, from 10 experts who practice what they teach.

---

## Why This Topic
YouTube is increasingly central to B2B SaaS go-to-market strategy, but most advice on the topic is generic. This research focuses on practitioners with real SaaS track records, to surface patterns and frameworks that are grounded in actual results.

---

## Expert Selection
10 experts were selected based on one core criterion: they must actively practice what they teach. That means founders who have used content to grow real SaaS companies, CMOs who have executed YouTube strategies at scale, or specialists whose work is directly tied to measurable outcomes.

See [`research/sources.md`](research/sources.md) for the full list with annotations.

**Experts covered:**
1. Rob Walling (MicroConf)
2. Jason Lemkin (SaaStr)
3. Ross Simmonds (Foundation Marketing)
4. Rand Fishkin (SparkToro)
5. Wes Bush (ProductLed)
6. Nathan Barry (Kit / ConvertKit)
7. Denis Shatalin
8. Dave Gerhardt (Exit Five)
9. Chima Mmeje (Moz)
10. Noah Kagan (AppSumo)

---

## Repository Structure

```
research/
  sources.md                    # All 10 experts with links, dates, and annotations
  youtube-transcripts/          # Transcripts organized by expert
    rob-walling/
    jason-lemkin/
    ross-simmonds/
    rand-fishkin/
    wes-bush/
    nathan-barry/
    denis-shatalin/
    dave-gerhardt/
    chima-mmeje/
    noah-kagan/
  linkedin-posts/               # LinkedIn posts organized by author
  other/                        # Any additional reference materials
fetch_transcripts.py            # Script used to collect YouTube transcripts via API
```

---

## Data Collection Method

**YouTube Transcripts**
Collected using the `youtube-transcript-api` Python library, which fetches publicly available captions directly from YouTube without requiring an API key. Videos were selected based on relevance to B2B SaaS content strategy.

```bash
pip install youtube-transcript-api
python fetch_transcripts.py
```

**LinkedIn Posts**
Collected manually by visiting each expert's LinkedIn profile and saving recent posts relevant to content strategy, YouTube, and B2B SaaS marketing.

---

## Commit Log
Commits are made incrementally as material is collected, not in one batch at the end.

---

*Research started: April 2026*
