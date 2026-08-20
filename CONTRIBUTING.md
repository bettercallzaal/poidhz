# Contributing to poidhz

Small repo, no build step, python standard library only. Things that help most:

1. **Deadline phrasings the parser misses.** Find an open bounty on poidh.xyz whose description states a deadline but does not show on the calendar. Add the phrase as a case in `scripts/deadline_parser.py` `selftest()`, make it pass, open a PR. Run `python3 scripts/deadline_parser.py --selftest` before pushing.
2. **New chains or tokens.** `CHAIN_TOKENS` in `scripts/build-bounty-dashboard.py` and the `CHAINS` map in `index.html`.
3. **Task-type classification misses.** `score_bounty()` in `scripts/build-bounty-dashboard.py` is keyword-based and documented inline; improve the keywords, keep it auditable.
4. **Running it for your own org.** Copy `org.config.json`, point it at your issuer wallets and bounty ids, run the scripts in the README.

Rules: no emojis and no em dashes in copy or commits; credit any source you build on (author + license) in the PR body; never commit keys or wallets that are not already public on-chain.

Every script must run under `/usr/bin/python3` on macOS (3.9). If you use `X | None` annotations, keep `from __future__ import annotations` at the top.
