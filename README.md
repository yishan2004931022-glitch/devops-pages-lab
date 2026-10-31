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
1. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/fbd29cb9aee64ff147dea52a9d88526593071e66)
2. 📝 Committed to main in a private repository
3. 🆕 Opened issue in a private repository
4. 👤 Assigned issue in a private repository
5. 🆕 Opened issue in a private repository
6. 👤 Assigned issue in a private repository
7. 🎉 Created a new branch exp4/seed-open-question in a private repository
8. 🔀 Merged PR in a private repository
9. 📝 Committed to exp4/seed-open-question in a private repository
10. 📥 Opened PR in a private repository
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
