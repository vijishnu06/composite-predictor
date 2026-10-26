# Publish to GitHub from Windows

First run the README setup and tests. Inspect your files for private uploads and remove any sensitive content before publishing. The default .gitignore excludes uploads, virtual environments and caches. The simulated CSV and locally generated model may be included; the literature template must remain empty until verified measurements are available.

Install Git for Windows, then open PowerShell in `composite-predictor`:

```powershell
git init
git branch -M main
git status
git add .
git diff --cached --stat
git commit -m "Build simulation-based composite strength prototype"
```

If Git requests your identity, set your own name and email with `git config user.name "YOUR NAME"` and `git config user.email "YOUR EMAIL"`, then retry the commit.

Create an empty repository named `composite-predictor` on GitHub using your account; do not initialize a second README. Replace YOUR-USERNAME below:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/composite-predictor.git
git push -u origin main
```

Complete Git's normal authentication prompt; never put access tokens in source files. For later changes: review `git diff`, use `git add .`, commit with a meaningful message and `git push`. Repository: https://github.com/vijishnu06/composite-predictor. The commands above describe the initial publication workflow. Choose an appropriate licence before public reuse; this project does not assume one on your behalf.
