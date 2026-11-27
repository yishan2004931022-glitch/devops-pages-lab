# Hi, I'm Yi-Shan Chen

A GitHub Pages site that publishes itself. The section below is not written by
hand: a scheduled workflow fetches my recent GitHub activity, rewrites this
file, and the commit it pushes triggers a new deployment of the site you are
reading.

- **Live site:** <https://yishan2004931022-glitch.github.io/devops-pages-lab/>
- **Build version:** [version.txt](version.txt) — the commit SHA this build was made from
- **How it works:** [Release safety](#release-safety)

## Recent activity
<!--START_SECTION:activity-->
1. 📝 Committed to devA/role-tests in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/commit/34ad1fb16ce894a8a3d7c3b29869884e763609da)
2. 📝 Committed to main in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/commit/8c0896269597938c29c760a273393b9851244d5a)
3. 🗣 Commented on a review of PR #23 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/23#pullrequestreviewcomment-4697297046)
4. 🗣 Commented on a review of PR #23 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/23#pullrequestreviewcomment-4697300891)
5. 🗣 Commented on PR #25 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/issues/25#issuecomment-7168089111)
6. 🗣 Commented on PR #24 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/issues/24#issuecomment-7168080697)
7. ❌ Closed issue #19 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/issues/19)
8. 🔀 Merged PR #23 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/23)
9. 🔎 Created PR #23 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/23#pullrequestreview-6060677884)
10. 🔎 Created PR #23 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/23#pullrequestreview-6060673208)
<!--END_SECTION:activity-->

## Release safety

Every push to `main` runs one workflow with four stages. A stage only starts if
the one before it succeeded.

| Stage | What it does | What it prevents |
| --- | --- | --- |
| **build** | Jekyll builds the site, and the commit SHA is written into `version.txt` | — |
| **validate** | Checks the activity markers survived, the HTML parses, and every link resolves | A broken page reaching the live site at all |
| **deploy** | Publishes to GitHub Pages | — |
| **smoke test** | Fetches the *live* `version.txt` and fails unless it is this exact commit | A deploy that silently served the old site |

A failed smoke test does not repair anything by itself. `rollback.yml` is run by
hand with a release tag and republishes that exact built site without rebuilding
it, which is why each successful deploy is archived as a release asset rather
than a workflow artifact — artifacts expire after a day.

The reason the smoke test checks a version rather than a status code: the
previous version of the site also returns HTTP 200. A check that only asks
"is something there?" passes most of the ways a deploy can go wrong.
