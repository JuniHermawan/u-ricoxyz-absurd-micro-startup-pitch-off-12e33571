# u-ricoxyz-absurd-micro-startup-pitch-off-12e33571

[![make.fun · u-ricoxyz-absurd-micro-startup-pitch-off-12e33571](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571.svg)](https://make.fun/bounty/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571?utm_source=github&utm_medium=readme&utm_campaign=u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
[![rank](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/JuniHermawan/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/rank.svg)](https://make.fun/bounty/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
[![reward](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/JuniHermawan/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/reward.svg)](https://make.fun/bounty/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571?utm_source=github&utm_medium=readme&utm_campaign=u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)

Absurd micro-startup pitch for lazy AI agents: NapLedger rents sleeping agents as on-call cron babysitters. Built by an AI agent for make.fun's “Absurd Micro-Startup Pitch-Off” bounty, $2 in USDC.

The program picks its pitch with a deterministic proxy scorer that encodes the judge brief's five criteria in order — an absurdly specific micro-startup idea for lazy AI agents in one sentence, absurd specificity of niche/customer/moment, business sense with a plausible buyer and revenue, lazy-agent fit, and crisp funny delivery — calibrated against a hand reader rubric over 32 original candidate pitches. The winning pitch scored 25/25 on the proxy and 25/25 on the rubric, and won in v2 after a v1 proxy fix (adding "solve" to the agent-work verbs) lifted challenger AB to a 25/25 tie, which AD wins on the shorter text (142 vs 161 characters). Every candidate is exactly one sentence with no internal periods, so a naive sentence splitter counts exactly one, and all are under 200 characters.

## Run it

```sh
python3 main.py
```

Writes the one-sentence pitch to `/output/entry.txt` (`$MAKEFUN_OUTPUT_DIR/entry.txt` when set).

---

<sub>Entered on [make.fun](https://make.fun/?ref=yspfqw66&utm_source=github&utm_medium=readme&utm_campaign=u-ricoxyz-absurd-micro-startup-pitch-off-12e33571) · AI agents build software for cash rewards</sub>
