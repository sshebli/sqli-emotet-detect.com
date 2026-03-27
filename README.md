# A Machine Learning Approach to Multi-Stage Cyber-Attack Detection: SQL Injection and Emotet Behaviour Analysis

This project presents a machine learning pipeline for detecting cyber-attack behaviour across two distinct stages: SQL injection (SQLi) and Emotet-related network activity. It includes trained Random Forest models, dataset preparation scripts, evaluation utilities, and a Streamlit dashboard for interactive testing and explainability -- https://cross-layer-detection.streamlit.app/

## Project Overview

The project contains two main detection components:

- **SQLi binary classifier**  
  Detects whether an input resembles normal traffic or a SQL injection payload using engineered structural features.

- **Unified multiclass classifier**  
  Detects one of three classes:
  - `0 = Normal`
  - `1 = SQLi`
  - `2 = Emotet`

The unified model combines:

- **9 SQLi structural features**
- **17 Emotet behavioural network features**

The repository also includes a Streamlit dashboard for:

- testing saved models interactively
- visualising explainability outputs
- exploring project content and evaluation results

## Repository Structure

```text
app.py                          # Streamlit application entry point

assets/                         # CSS and styling assets
static/                         # Images and static visual assets

templates/                      # Dashboard UI layout and rendering logic
src/                            # Core feature engineering and inference helpers
scripts/                        # Training, evaluation, validation, and analysis scripts

models/                         # Saved pretrained model artifacts (.joblib)
data/                           # Datasets and derived files
outputs/                        # Metrics, figures, schemas, and generated outputs

requirements.txt                # Python dependencies
README.md                       # Project documentation
```

## Key Model Artifacts

Saved models are stored in `models/` and are loaded directly from disk at runtime.

### SQLi model

- `rf_sqli.joblib`

This artifact contains:

- the trained `RandomForestClassifier`
- the associated SQLi feature names

It expects **9 input features**:

- `Sentence Length`
- `AND Count`
- `OR Count`
- `UNION Count`
- `Single Quote Count`
- `Double Quote Count`
- `Constant Value Count`
- `Parentheses Count`
- `Special Characters Total`

### Unified multiclass models

- `rf_unified_multiclass.joblib`
- `rf_unified_multiclass_balanced.joblib`

These artifacts load as trained `RandomForestClassifier` objects and expect **26 input features**:

- 9 SQLi features
- 17 Emotet behavioural features

## Runtime Workflow

The dashboard uses an **inference-only workflow**.

At runtime:

1. saved model artifacts are loaded from `models/`
2. user-provided feature inputs are assembled
3. the model performs `predict()` / `predict_proba()`
4. the dashboard displays the result

### Important

The application does **not retrain models during normal use**.

Training, tuning, and evaluation are handled separately in `scripts/` and `src/`, but these are **not required** for normal dashboard use.

## Reproducibility Notes

The project is designed so that the dashboard can run directly from saved model artifacts without retraining.

### Included in the repository

- pretrained model artifacts
- processed datasets
- Zeek-derived logs
- generated outputs such as metrics, figures, and schemas

### Not included in the repository

Raw PCAP files are **not bundled in the repository due to size**.

These raw PCAPs were obtained from external public sources and kept outside the tracked repository. This does not affect normal dashboard use or model inference. The repository includes the processed derivatives used by the project, and the original source links are provided below for traceability and optional regeneration.

### Minor reproducibility limitation

The final saved model artifacts were produced iteratively during development. Training scripts are included in the repository, but exact serialized artifacts may differ across runs due to non-deterministic elements of Random Forest training, such as bootstrap sampling.

## Data Sources

The project uses data derived from the following sources:

- **Kaggle SQL injection dataset** — [SQL Injection Dataset with SQL Features Value](https://www.kaggle.com/datasets/syedsaqlainhussain/sql-injection-dataset)
- **Zenodo SQLi corpus** (external validation) — [Superviz25-SQL: SQL Injection Detection Dataset](https://zenodo.org/records/17086037)
- **Unit42 Emotet infection captures** — [Wireshark Tutorial: Examining Emotet Infection Traffic](https://unit42.paloaltonetworks.com/wireshark-tutorial-emotet-infection/) and [GitHub repository](https://github.com/pan-unit42/wireshark-tutorial-Emotet-traffic)
- **Stratosphere IPS normal captures** — [Malware Capture Facility Project](https://www.stratosphereips.org/datasets-malware) and [Normal Captures](https://www.stratosphereips.org/datasets-normal)


## Data and Feature Engineering

### SQLi features

The SQLi classifier uses 9 engineered structural features extracted from payload text, including token counts, quote counts, parentheses, and special-character statistics.

### Emotet features

The Emotet component uses behavioural features derived from Zeek connection logs, including:

- connection count
- protocol ratios
- byte and packet statistics
- interarrival variation
- unique destination counts
- TCP / UDP / DNS / HTTP / SSL ratios

### Time-windowed aggregation

Network events were aggregated into short fixed windows so that each row describes traffic behaviour over a small time interval rather than a single raw connection.

## Dashboard

The Streamlit dashboard provides:

- SQLi model testing
- unified model testing
- explainability views
- project content pages
- quiz / educational sections

To run the dashboard:

```bash
streamlit run app.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://git.cs.bham.ac.uk/projects-2025-26/sma308.git
cd dissertation-ml-pipeline
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Requirements

- **Python 3.9+**
- Main Python dependencies are listed in `requirements.txt`

## Running the Project

### Run the dashboard

```bash
streamlit run app.py
```

### Notes

- No training step is required for dashboard use
- Saved model files must be present in `models/`
- Processed datasets and outputs should remain in their expected folders

## Training and Evaluation Scripts

The repository also contains separate scripts for:

- model training
- cross-validation
- external validation
- group-aware holdout evaluation
- confusion matrix generation
- ROC analysis
- feature importance analysis
- dataset comparison and variance checks

These scripts are intended for experimentation, evaluation, and reproducibility support, not for normal dashboard execution.

## Outputs

The `outputs/` directory stores generated files such as:

- metrics CSVs / JSON files
- plots and figures
- feature importance outputs
- schema files used by the dashboard

## Notes for Examiners / Reproduction

For normal reproduction of the dashboard:

- install dependencies
- ensure the saved model artifacts exist in `models/`
- run `streamlit run app.py`

For deeper data regeneration:

- use the scripts in `src/` and `scripts/`
- raw PCAPs must be obtained separately from their original public sources if full raw-data reconstruction is required

## Author

**Shahad Shebli**  
University of Birmingham Dubai  
BSc Artificial Intelligence and Computer Science