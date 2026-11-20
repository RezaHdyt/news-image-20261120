# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/RezaHdyt/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/RezaHdyt/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up Friday 20 November 2026's world news: a clean newspaper
front page with 36 real stories and 12 hand-drawn panels — from the first-ever
Trump–Xi–Putin trilateral summit in Shenzhen and the missile attack on Ukraine
that followed hours later, to Anthropic's Nasdaq debut, the ICJ's genocide
ruling on Myanmar, and markets tumbling on AI-bubble fears.

`render.py` draws the front page with PIL; `main.ts` validates `entry.png`
against the bounty gate (PNG, at most 1 MiB, at most 1024×1024) and copies it
to the output directory. Deterministic, no network, standard library only.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes the validated `entry.png` to `out/entry.png`. Without
`MAKEFUN_OUTPUT_DIR` the output goes to `/output/entry.png`.

<sub>Entered on [make.fun](https://make.fun/?ref=1c6x9h9j&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
