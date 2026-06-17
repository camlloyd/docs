#!/usr/bin/env python3
"""Conversational Genome live backend.

Runs the REAL ClawBio pharmgx-reporter skill per request and serves the demo
page. The frontend calls /api/run on each question; if this backend is not
reachable (e.g. on the static docs.clawbio.ai host) the page falls back to the
embedded skill output, so the public URL keeps working.

Run:
    pip install -r requirements.txt
    uvicorn server:app --reload
    open http://localhost:8000

NOT FOR CLINICAL USE. Research and educational demonstration only.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_pharmgx():
    """Locate the ClawBio pharmgx-reporter skill (dev checkout or installed
    wheel) and return its api.run callable. No side effects beyond sys.path."""
    try:
        import clawbio  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "ClawBio is not installed. Run: pip install clawbio"
        ) from exc
    pkg = Path(clawbio.__file__).resolve().parent
    candidates = [
        pkg.parent / "skills" / "pharmgx-reporter",   # dev checkout
        pkg / "skills" / "pharmgx-reporter",           # bundled wheel
    ]
    for skill_dir in candidates:
        if (skill_dir / "api.py").exists():
            for p in (str(skill_dir.parent.parent), str(skill_dir)):
                if p not in sys.path:
                    sys.path.insert(0, p)
            from api import run as pharmgx_run  # type: ignore
            return pharmgx_run
    raise RuntimeError("pharmgx-reporter skill not found in the ClawBio install")


pharmgx_run = _load_pharmgx()

# Manuel Corpas's real genotypes at the PGx panel rsIDs, from the published
# 23andMe Corpasome (CC0, figshare doi:10.6084/m9.figshare.693052).
GENOTYPES = {
    "rs10264272": "CC", "rs1057910": "AA", "rs1065852": "GG", "rs1142345": "TT",
    "rs12248560": "CC", "rs1799853": "CT", "rs1800460": "CC", "rs1800462": "CC",
    "rs28371725": "CT", "rs28399499": "TT", "rs28399504": "AA", "rs3745274": "GT",
    "rs3918290": "CC", "rs4148323": "GG", "rs4149056": "TT", "rs4244285": "GG",
    "rs4986893": "GG", "rs5030655": "II", "rs762551": "AA", "rs776746": "CC",
    "rs9923231": "TT", "rs1801131": "GT", "rs1801133": "GG",
}

SKILL = "pharmgx-reporter"
VERSION = "0.2.0"

from fastapi import FastAPI                       # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import FileResponse        # noqa: E402
from fastapi.staticfiles import StaticFiles        # noqa: E402

app = FastAPI(title="Conversational Genome", version=VERSION)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


def _drug_levels(drug_recs: dict) -> dict:
    levels = {}
    for level in ("avoid", "caution", "standard", "indeterminate"):
        for d in drug_recs.get(level, []):
            name = d.get("drug") if isinstance(d, dict) else d
            if name:
                levels[name.lower()] = level
    return levels


@app.get("/api/health")
def health():
    return {"status": "ok", "skill": SKILL, "version": VERSION,
            "genotypes": len(GENOTYPES)}


@app.post("/api/run")
def run_skill():
    """Execute the real ClawBio pharmgx-reporter skill on the genotypes and
    return its genuine output plus timing. Called once per question."""
    t0 = time.perf_counter()
    res = pharmgx_run(GENOTYPES)
    elapsed = round((time.perf_counter() - t0) * 1000, 1)
    return {
        "executed_live": True,
        "elapsed_ms": elapsed,
        "skill": SKILL,
        "version": VERSION,
        "gene_profiles": res["gene_profiles"],
        "drug_levels": _drug_levels(res["drug_recommendations"]),
        "summary": res["summary"],
    }


@app.get("/")
def index():
    return FileResponse(str(HERE / "index.html"))


# Serve the rest of the demo assets (none required today, but future-proof).
app.mount("/static", StaticFiles(directory=str(HERE)), name="static")
