# CLAUDE.md

Notes for AI coding assistants working in this repository.

## Project

CronLens explains, validates and previews cron expressions. It is pure computation:
no database, no network calls, no user accounts and no personal data. Keep it that way.

- `backend/cronlens/parser.py` - parses 5-field cron into `CronExpression` (sets of ints per field)
- `backend/cronlens/schedule.py` - computes next run times (naive datetimes, treated as UTC)
- `backend/cronlens/describe.py` - English description of an expression
- `backend/cronlens/api.py` - FastAPI app (`POST /api/explain`, `GET /api/health`)
- `frontend/src/` - React + TypeScript UI (Vite); `/api` is proxied to port 8000 in dev

## Commands

```bash
cd backend && source .venv/bin/activate
pytest                      # tests
ruff check . && ruff format --check .

cd frontend
npm test                    # vitest
npm run build               # type-check + production build
```

## Conventions

- Python 3.11+, type hints everywhere, ruff line length 100.
- Parser errors raise `CronSyntaxError` with `field` set when a single field is at fault.
- Day-of-week uses cron numbering (Sunday = 0); Python's `weekday()` is Monday = 0.
- Every behaviour change comes with a test. Use fixed dates in tests, never `now()`.
- Add dependencies only when clearly needed; prefer the standard library.
- Planned work lives in `ROADMAP.md`; tick items off there when done.
