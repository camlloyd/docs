# ClawBio growth figure

`growth.png` / `growth.svg`: a 2x2 panel (commits, pull requests, contributors,
PyPI downloads) for the KCL agentic-genomics hackathon deck (18 Jun 2026),
styled to the ClawBio deck theme.

Generated 16 Jun 2026. Regenerate with:

```bash
python3 make_growth_figure.py
```

The script reads only the two CSVs below (no synthetic data).

## Data provenance

| Series | Source | Command / endpoint |
|--------|--------|--------------------|
| Commits (cumulative) | local git history of `ClawBio/ClawBio` | `git log --pretty=format:%ad --date=format:%Y-%m \| sort \| uniq -c` (cumulated) |
| Pull requests opened/merged | GitHub API | `gh pr list --repo ClawBio/ClawBio --state all --json createdAt,mergedAt` |
| Contributors (cumulative) | local git history | unique commit authors deduped by normalised name, bot/automation authors excluded, first-seen month cumulated. Ends at 44; the GitHub contributors API reports 33 accounts and the site badge 43 (different counting methods). |
| GitHub stars (cumulative) | GitHub API | `gh api repos/ClawBio/ClawBio/stargazers -H "Accept: application/vnd.github.star+json" --paginate` |
| PyPI downloads (daily) | pypistats.org | `https://pypistats.org/api/packages/clawbio/overall?mirrors=false` |
| Clones + unique cloners (daily) | GitHub API | `gh api repos/ClawBio/ClawBio/traffic/clones`. **14-day window only** (GitHub does not retain older clone traffic, and the repo keeps no historical log). Raw clones (8,617) include CI/automation re-clones; unique cloners (611) is the human "unique downloaders" signal. |

Repository created 25 Feb 2026; `pip install clawbio` launched 11 Jun 2026.
Numbers are as of 16 Jun 2026 and will drift; rerun the source commands and
update the CSVs before reusing the figure.

## Comparison figures (`comparison.*` = stars, `forks.*` = forks)

`make_comparison_figure.py` reads `peers.csv` (live `gh api repos/<owner>/<repo>`
data, 16 Jun 2026) and renders two charts:

- `comparison.png/svg`: GitHub **stars** gained per month (lifetime average).
- `forks.png/svg`: **forks** gained per month (lifetime average).

**Why forks, not clones.** GitHub clone traffic is private to each repository's
own maintainers; `gh api repos/<peer>/traffic/clones` returns `403 Must have
push access` for any repo you do not own, so a cross-project *clone* comparison
cannot be built from real data. Forks (public copies of a repo) are the
comparable "took a copy" proxy. ClawBio's own clone traffic (8,617 clones / 611
unique cloners, 14-day window) is in `clones_daily.csv` for the growth figure.

Caveat shown on both figures: per-month is a lifetime average, the comparators
are 7 to 17 years old, and the agentic-era GitHub is larger/faster than when
those tools launched, so the honest claim is "an order of magnitude faster
velocity," not a quality ranking. OpenClaw Medical Skills is flagged dormant
(no push for 81 days).

## Native workflow graphs (`make_workflow_figures.py`)

Three dark-theme SVGs that redraw the bioRxiv study-design figures in the deck's
own style, so the benchmark slides stop showing white paper PNGs on a dark deck.
Regenerate with:

```bash
python3 make_workflow_figures.py
```

| File | Slide | Content |
|------|-------|---------|
| `design-workflow.svg` | Experimental design | Scale strip (110 cases x 9 LLMs x 3 ancestries x 3 replicates = 44,550); the five-condition constraint gradient; two validation arms (curated to real-genome, 72/51/40 by ancestry). |
| `result-workflow.svg` | Result | Phenotype accuracy by condition (80.6 / 89.5 / 95.5 / 93.3 / 100.0) and the clinical-grade guarantees matrix; only skill-execution and the control satisfy all five. |
| `paradox-workflow.svg` | Counterintuitive result | Lethal-class error rate by condition (24.6 / 36.6 RAG-worst / 8.5 / 15.3 / 0); retrieval raised lethal errors by 12 points. |

Every number is a real reported aggregate from the preprint (Corpas, Iacoangeli,
Bourdenx, Aldraimli, Skene, Fatumo, Guio. *Trustworthy agentic genomics through
versioned skill libraries*. bioRxiv 2026, doi:10.64898/2026.06.11.731523). No
synthetic data: the SVGs encode only the published aggregates, not invented
per-model points. The original extracted PNGs remain in `paper/` for provenance.
