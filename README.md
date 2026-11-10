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
1. 🔀 Merged PR #1 in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/pull/1)
2. 📥 Opened PR #1 in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/pull/1)
3. 🌍 Made repository public [yishan2004931022-glitch/NTUST_QuestionnaireOptimizationSystem_project](https://github.com/yishan2004931022-glitch/NTUST_QuestionnaireOptimizationSystem_project)
4. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/c22eecffcb010b0a2c629ec31ebf4b5cfc8162aa)
5. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/19373f41acda7eab932cbddd0f76d302ea81735f)
6. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/1521c191fa22245ddff16087d679f0a1fc7201ac)
7. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/730bab248357857ac98f91412166db9002118c80)
8. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/11f8e501efea05f8a780961d5506f9d5a1754ed4)
9. 📝 Committed to main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/commit/dcf546186d27b71f925a883d12a9be31f35da088)
10. 🎉 Created a new branch main in [yishan2004931022-glitch/devops-pages-lab](https://github.com/yishan2004931022-glitch/devops-pages-lab/tree/main)
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
