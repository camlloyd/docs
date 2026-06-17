# Conversational Genome

A live demo: ask a genome questions in natural language and get answers that are
**executed by a real, versioned ClawBio skill**, with provenance, confidence and
an ancestry-validity flag. Runs on Manuel Corpas's openly published genome (the
23andMe Corpasome, CC0, figshare doi:10.6084/m9.figshare.693052).

Live page: https://docs.clawbio.ai/presentations/conversational-genome/

## Two ways it runs

| Mode | What happens | Where |
|------|--------------|-------|
| **Live** | Each question calls the backend, which runs `pharmgx-reporter v0.2.0` and returns its genuine output, with the elapsed time shown on the card. | your machine |
| **Static fallback** | No backend reachable, so the page renders the same skill output pre-computed and embedded at build time. | docs.clawbio.ai |

The frontend tries the backend first and silently falls back, so the public URL
keeps working with no server.

## Run the live backend

```bash
pip install -r requirements.txt        # clawbio + fastapi + uvicorn
uvicorn server:app --reload            # serves the page and the API
open http://localhost:8000             # ask a question -> live ClawBio
```

When connected, the genome bar shows a green **live** indicator and every drug
answer carries an "executed live in N ms" badge.

## Endpoints

- `GET  /api/health` -> skill name and version
- `POST /api/run` -> executes the skill on the genotypes, returns
  `gene_profiles`, `drug_levels`, `summary`, and `elapsed_ms`
- `GET  /` -> the demo page

## Tests

```bash
pytest test_server.py        # asserts the real skill output (warfarin AVOID, etc.)
```

## Regenerate the static fallback data

```bash
python3 gen_clawbio_data.py > /tmp/new_genome.js   # runs the skill, emits GENOME
```

NOT FOR CLINICAL USE. Research and educational demonstration only. Interpretations
follow CPIC guidelines via the ClawBio pharmgx-reporter skill.
