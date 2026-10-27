"""HTTP API for CronLens."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from cronlens import __version__
from cronlens.describe import describe
from cronlens.parser import CronSyntaxError, parse
from cronlens.schedule import next_runs

app = FastAPI(title="CronLens", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ExplainRequest(BaseModel):
    expression: str = Field(min_length=1, max_length=200)
    count: int = Field(default=10, ge=1, le=100)
    after: datetime | None = Field(default=None, description="Start point (UTC). Defaults to now.")


class FieldInfo(BaseModel):
    name: str
    source: str
    values: list[int]


class ExplainResponse(BaseModel):
    expression: str
    description: str
    fields: list[FieldInfo]
    next_runs: list[datetime]


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/api/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    try:
        expr = parse(request.expression)
    except CronSyntaxError as exc:
        raise HTTPException(
            status_code=422, detail={"message": str(exc), "field": exc.field}
        ) from exc

    after = request.after or datetime.now(UTC)
    if after.tzinfo is not None:
        after = after.astimezone(UTC).replace(tzinfo=None)
    runs = next_runs(expr, after, request.count)
    return ExplainResponse(
        expression=expr.source,
        description=describe(expr),
        fields=[
            FieldInfo(name=f.name, source=f.source, values=sorted(f.values)) for f in expr.fields
        ],
        next_runs=[run.replace(tzinfo=UTC) for run in runs],
    )
