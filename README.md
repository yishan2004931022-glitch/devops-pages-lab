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
1. 📝 Committed to main in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/commit/b25211fa207099bc1d3579b770a890f95ba5b536)
2. 🔀 Merged PR #11 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/11)
3. 📥 Opened PR #11 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/11)
4. ❌ Closed issue #6 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/issues/6)
5. 🔎 Created PR #10 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/10#pullrequestreview-6013125727)
6. 🔀 Merged PR #8 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/8)
7. 📥 Opened PR #8 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/8)
8. Added [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy)
9. 🔀 Merged PR #4 in [yishan2004931022-glitch/coursebuddy](https://github.com/yishan2004931022-glitch/coursebuddy/pull/4)
10. 🎉 Created a new branch main in [yishan2004931022-glitch/coursebuddy](https://github.com/yishan2004931022-glitch/coursebuddy/tree/main)
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
