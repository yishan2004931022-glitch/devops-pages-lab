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
1. 📥 Opened PR #8 in [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy/pull/8)
2. Added [CourseBuddy-AI/CourseBuddy](https://github.com/CourseBuddy-AI/CourseBuddy)
3. 🔀 Merged PR #4 in [yishan2004931022-glitch/coursebuddy](https://github.com/yishan2004931022-glitch/coursebuddy/pull/4)
4. 🎉 Created a new branch main in [yishan2004931022-glitch/coursebuddy](https://github.com/yishan2004931022-glitch/coursebuddy/tree/main)
5. 📝 Committed to a9-devsecops in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/e92c8e45c34c7f65236fc340f8ea97155e9f589a)
6. 🎉 Created a new branch a9-devsecops in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/tree/a9-devsecops)
7. 🔀 Merged PR #1 in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/pull/1)
8. 📥 Opened PR #1 in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/pull/1)
9. 🌍 Made repository public [yishan2004931022-glitch/NTUST_QuestionnaireOptimizationSystem_project](https://github.com/yishan2004931022-glitch/NTUST_QuestionnaireOptimizationSystem_project)
10. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/c22eecffcb010b0a2c629ec31ebf4b5cfc8162aa)
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
