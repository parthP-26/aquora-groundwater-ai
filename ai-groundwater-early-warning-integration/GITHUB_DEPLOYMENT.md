# GitHub deployment

Create each folder as its own repository; URLs are intentionally placeholders.

```bash
git init
git add .
git commit -m "Initial implementation"
git branch -M main
git remote add origin <REPOSITORY_URL>
git push -u origin main
```

Suggested description: station-level groundwater research decision-support prototype. Topics: `groundwater`, `machine-learning`, `gis`, `fastapi`, `react`, `india`. Use protected `main`, short-lived feature branches, Conventional Commit-style messages, reviewed pull requests, and tagged releases. Report reproducible issues without sensitive data.
