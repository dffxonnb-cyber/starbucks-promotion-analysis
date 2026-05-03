# Verification Guide

This project has two verification levels: public artifact verification for GitHub review, and full notebook reproduction when the original Kaggle CSV files are available locally.

## Verification Scope

| Area | Publicly Verifiable | Notes |
| --- | --- | --- |
| Public review artifacts | Yes | `scripts/check_public_artifacts.py` checks README, docs, images, Tableau workbook, and pipeline entry point. |
| Pipeline entry-point syntax | Yes | CI compiles `run_pipeline.py` and the artifact checker. |
| Notebook sequence | Yes, structurally | Notebook files are tracked and ordered through `run_pipeline.py`. |
| Full notebook execution | Requires data | Needs `portfolio.csv`, `profile.csv`, and `transcript.csv`. |
| Tableau review | Yes | The `.twb` workbook is tracked for public inspection. |

## Local Verification

Public review check:

```bash
python -m py_compile run_pipeline.py scripts/check_public_artifacts.py
python scripts/check_public_artifacts.py
```

Full notebook pipeline after placing the Kaggle CSV files in `data/`:

```bash
pip install -r requirements.txt
python run_pipeline.py --clear-artifacts --stop-on-error
```

## CI Verification

GitHub Actions runs:

```bash
python -m py_compile run_pipeline.py scripts/check_public_artifacts.py
python scripts/check_public_artifacts.py
```

## Data Boundary

- Required raw files: `portfolio.csv`, `profile.csv`, `transcript.csv`.
- Raw CSVs are not tracked and must be downloaded from the original Kaggle source.
- Generated notebook outputs and logs are written under `artifacts/` and are not committed by default.

## Known Limits

- CI does not execute notebooks because the required CSV files are not committed.
- Public verification confirms reviewability and pipeline entry-point health, not current model retraining.
- Validation metrics should be read together with `docs/reproducibility_and_validation.md`.
