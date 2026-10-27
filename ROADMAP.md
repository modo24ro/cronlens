# Roadmap

Planned work, roughly in priority order. Each item is meant to be a self-contained
change with tests.

## Parser

- [ ] Macros: `@yearly`, `@annually`, `@monthly`, `@weekly`, `@daily`, `@midnight`, `@hourly`
- [ ] `@reboot` (parse and explain; it has no next run)
- [ ] Optional seconds field (6-field expressions) behind a "dialect" option
- [ ] Quartz extensions: `?`, `L`, `W`, `#` (e.g. `0 0 12 ? * MON#2`)
- [ ] Dialect selector: Vixie, Quartz, AWS EventBridge, GitHub Actions (UTC only)
- [ ] Warnings (not errors) for suspicious expressions: `* 9 * * *` (every minute of an hour),
      day-of-month 31 in short months, `0 0 30 2 *` that never fires
- [ ] Column positions in syntax errors so the UI can underline the bad token

## Schedule engine

- [ ] Timezone support (IANA names via `zoneinfo`), with clear DST behaviour:
      skipped runs in spring-forward, duplicate runs in fall-back
- [ ] Faster next-run search (jump straight to the next matching value per field)
- [ ] Previous runs (`before` instead of `after`)
- [ ] Runs between two dates, with a hard cap
- [ ] Property-based tests (Hypothesis) comparing against a brute-force minute scanner

## Descriptions

- [ ] Better phrasing for steps inside ranges (`10-50/10`) and hour steps (`0 */2 * * *`)
- [ ] 12-hour clock option
- [ ] Localised descriptions (start with Romanian), translation tables kept outside code

## Crontab files

- [ ] Parse a whole crontab file (comments, env lines, user field in `/etc/crontab`)
- [ ] Overlap report: jobs that start in the same minute
- [ ] Weekly heatmap of how many jobs start in each hour

## Other schedule formats

- [ ] Import Kubernetes `CronJob` YAML (`spec.schedule`, `spec.timeZone`)
- [ ] Import GitHub Actions workflow `on.schedule`
- [ ] systemd `OnCalendar=` expressions (explain + convert to cron where possible)

## Frontend

- [ ] Live validation while typing (debounced), with the bad field highlighted
- [ ] Visual builder: pick minutes/hours/days with toggles, generate the expression
- [ ] Calendar / timeline view of next runs
- [ ] Shareable URL (`?e=0+9+*+*+1-5`)
- [ ] Copy buttons and keyboard shortcuts
- [ ] Dark mode
- [ ] Component tests with Testing Library

## Tooling and packaging

- [ ] CLI: `cronlens explain "0 9 * * 1-5" --next 5`
- [ ] Serve the built frontend from FastAPI so one process runs everything
- [ ] Dockerfile and `docker compose up`
- [ ] Publish the Python package to PyPI
- [ ] Type checking with mypy in CI
- [ ] ESLint + Prettier for the frontend
- [ ] Coverage report in CI
