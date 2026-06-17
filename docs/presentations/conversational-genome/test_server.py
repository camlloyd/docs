"""Red/green tests for the Conversational Genome live backend.

The backend must execute the REAL ClawBio pharmgx-reporter skill per request
and serve the static demo page. Run: pytest test_server.py
"""
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_health_reports_clawbio():
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["skill"] == "pharmgx-reporter"
    assert body["version"] == "0.2.0"


def test_run_executes_real_clawbio():
    r = client.post("/api/run")
    assert r.status_code == 200
    b = r.json()
    assert b["executed_live"] is True
    assert b["elapsed_ms"] >= 0
    gp = b["gene_profiles"]
    # real ClawBio calls on the Corpasome genotypes
    assert gp["CYP2C9"]["diplotype"] == "*1/*2"
    assert "Intermediate" in gp["CYP2C9"]["phenotype"]
    assert "High" in gp["VKORC1"]["phenotype"]          # high warfarin sensitivity
    assert gp["CYP2C19"]["diplotype"] == "*1/*1"
    assert gp["CYP2D6"]["diplotype"] == "*1/*41"


def test_run_drug_levels_match_skill():
    b = client.post("/api/run").json()
    levels = b["drug_levels"]
    assert levels["warfarin"] == "avoid"
    assert levels["clopidogrel"] == "standard"
    assert levels["codeine"] == "caution"
    assert levels["capecitabine"] == "indeterminate"   # DPYD incomplete coverage
    s = b["summary"]
    assert s["drugs_avoid"] == 1
    assert s["drugs_assessed"] == 59


def test_serves_static_page():
    r = client.get("/")
    assert r.status_code == 200
    assert "Conversational Genome" in r.text
