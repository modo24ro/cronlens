# CronLens

Explain, validate and preview cron schedules.

Paste a cron expression such as `0 9 * * MON-FRI` and CronLens tells you, in plain
English, when it runs, shows how each field expands, and lists the next run times.
It catches mistakes (out-of-range values, reversed ranges, zero steps) and points to
the field that is wrong.

CronLens is a small, self-contained developer tool: a Python library + FastAPI
backend and a React + TypeScript frontend. It does pure date arithmetic, needs no
database and stores nothing.

## Status

Early stage (v0.1). Standard 5-field cron works today; timezones, macros, crontab
import and more are planned in [ROADMAP.md](ROADMAP.md).

## Quick start

Requirements: Python 3.11+, Node.js 20+.

```bash
# Backend (http://127.0.0.1:8000, docs at /docs)
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn cronlens.api:app --reload

# Frontend (http://localhost:5173), in a second terminal
cd frontend
npm install
npm run dev
```

## API

`POST /api/explain`

```json
{ "expression": "0 9 * * MON-FRI", "count": 3, "after": "2026-01-01T00:00:00Z" }
```

returns

```json
{
  "expression": "0 9 * * MON-FRI",
  "description": "At 09:00, on Monday through Friday.",
  "fields": [{ "name": "minute", "source": "0", "values": [0] }, "..."],
  "next_runs": ["2026-01-01T09:00:00Z", "2026-01-02T09:00:00Z", "2026-01-05T09:00:00Z"]
}
```

Syntax errors return `422` with `{"detail": {"message": "...", "field": "minute"}}`.

## Supported syntax

| Field        | Range | Names     |
| ------------ | ----- | --------- |
| minute       | 0-59  |           |
| hour         | 0-23  |           |
| day of month | 1-31  |           |
| month        | 1-12  | JAN-DEC   |
| day of week  | 0-7   | SUN-SAT (0 and 7 are Sunday) |

Each field accepts `*`, values, ranges `a-b`, lists `a,b,c` and steps `*/n`, `a-b/n`,
`a/n`. When both day-of-month and day-of-week are restricted, a day matches if
**either** matches (classic Vixie cron behaviour).

## Development

```bash
cd backend && pytest && ruff check . && ruff format --check .
cd frontend && npm test && npm run build
```

CI runs the same checks on every push and pull request.

## License

[MIT](LICENSE)
