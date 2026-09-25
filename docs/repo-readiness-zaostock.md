<!-- NOT-ANNOUNCEMENT-COPY: internal readiness assessment of another repository. Names no deadline anyone submits to. -->
# ZAOstock repo readiness - what an outside contributor actually finds

Measured 2026-09-25 against `ZAODEVZ/ZAOstock`, before casting a bounty that sends agents there.
**A bounty that points people at a repository is responsible for what they find when they
arrive.**

## The verdict: it is in good shape, with two things that will cost entrants time

`ZAODEVZ/ZAOstock` is **public, MIT licensed, not archived**, TypeScript on Next.js, issues
enabled, pushed to the day this was written. It has a real `CONTRIBUTING.md`, a
`docs/ARCHITECTURE.md`, an `AGENTS.md`, and CI that runs typecheck, lint, test, build,
`check:facts` and `check:review` on every pull request.

**The single most useful fact, and it was written down nowhere a contributor would look:**
`.github/workflows/ci.yml` runs all of those with **no secrets at all**. So anyone can clone,
`npm ci`, and verify their own work before pushing. `CONTRIBUTING.md` leads with the
`.env.local` Supabase setup, which reads like a hard requirement and is not one for most
changes.

## Blocker 1 - AGENTS.md sent agents to files that do not exist. FIXED, pending merge.

The file opened with:

> *"Before agentic work in this repo, read `~/zao-vault/GENESIS.md` (the constitution),
> `~/zao-vault/BLACKBOARD.md` (live state) and `~/zao-vault/AGENTS.md`."*

Those are on maintainers' own machines. **A `--depth=1` clone has no `zao-vault/` directory at
all** - verified against a clean clone, not assumed. So the first instruction in the file
written to orient agents was a dead end, in the week we are asking agents to contribute.

**PR #308** fixes it without deleting anything: the internal section is labelled INTERNAL and
kept, because it is still correct for the people it was written for, and a section that works
for anyone goes above it. Every claim in the new text was checked against the clone.

## Blocker 2 - 202 branches, 174 of them already merged

Measured by joining the branch list against 286 closed pull requests:

| | |
|---|---|
| Branches on the remote | **202** |
| Whose PR is already **merged** | **174** |
| Remainder - unmerged or never PR'd | 28 |

A contributor opening the branch list cannot tell what is live, what was abandoned and what
shipped in May. It also makes `git branch -r` useless as a way to see what anyone is working
on.

**This is a repo action, not something a bounty entrant can do**, and it is not mine to fire.
The safe form deletes only branches whose PR is recorded as merged:

```bash
# DRY RUN FIRST. Lists what would go, deletes nothing.
gh api 'repos/ZAODEVZ/ZAOstock/pulls?state=closed&per_page=100&base=main' --paginate \
  --jq '.[] | select(.merged_at != null) | .head.ref' | sort -u > /tmp/merged-heads.txt
gh api 'repos/ZAODEVZ/ZAOstock/branches?per_page=100' --paginate --jq '.[].name' \
  | sort -u > /tmp/live-branches.txt
comm -12 /tmp/merged-heads.txt /tmp/live-branches.txt | tee /tmp/deletable.txt | wc -l
```

Then, and only after reading `/tmp/deletable.txt`:

```bash
while read -r b; do
  [ "$b" = "main" ] && continue
  gh api -X DELETE "repos/ZAODEVZ/ZAOstock/git/refs/heads/$b"
done < /tmp/deletable.txt
```

**Two guards worth keeping in that loop.** `main` is skipped explicitly rather than trusted not
to appear. And every branch in the list is there because GitHub says its pull request was
merged, so nothing unique is lost - the commits are in `main`'s history either way.

**Not done here.** Deleting 174 remote branches is outward-facing and irreversible from this
seat. It wants a human tap.

## What this does NOT assess

- **Whether the site is any good.** This is about whether a stranger can contribute, not about
  the product.
- **Test coverage, performance, security.** Not measured. A clean CI run is not an audit.
- **Whether the 2 open issues are good first issues.** Only one is open as of this read,
  `#230 Uptime: /api/events is down`, and an uptime alert is not a task for an outside
  contributor.
- **`npm run dev` against live data.** Not attempted - it wants Supabase credentials this seat
  does not have and should not have.

## What this means for round five

The round can cast. The repo is genuinely contributable-to once #308 merges, the licence is
permissive, and CI gives every entrant a way to check their own work without asking anyone for
anything.

The branch mess is worth naming in the bounty rather than hiding - it is an honest picture of
the codebase, and a contributor who reads it learns something true about what they are walking
into.
