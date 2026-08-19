from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .engine import build_approval_queue, sample_opportunities
from .models import ApplicantProfile


ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"

app = FastAPI(title="PrizePilot Agent", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class ProfilePayload(BaseModel):
    country: str = "Denmark"
    is_adult: bool = True
    works_solo: bool = True
    internet_access: bool = True
    verified_student: bool = False


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "approval-first"}


@app.post("/api/queue")
def queue(payload: ProfilePayload) -> dict:
    profile = ApplicantProfile(
        country=payload.country,
        is_adult=payload.is_adult,
        works_solo=payload.works_solo,
        attributes={
            "internet_access": payload.internet_access,
            "verified_student": payload.verified_student,
        },
        evidence={},
    )
    return {
        "items": [
            asdict(item)
            for item in build_approval_queue(profile, sample_opportunities())
        ]
    }

