# Model and Dataset Provenance

This note summarises the main dataset and model relationships used in the project so that the repository remains easy to interpret later.

## Purpose of this note

The project contains several related datasets and more than one saved unified model artifact. Some of these files are closely related, but they are not interchangeable. This note records the intended role of each major dataset and model.

## SQLi pipeline

### Main SQLi training source
The final SQLi model was trained from:

- `data/updated_file.csv`

This is the engineered SQLi dataset used as the final training source for the saved SQLi Random Forest model.

### Saved SQLi model
The final saved SQLi model is:

- `models/rf_sqli.joblib`

Its role is binary SQLi detection using the 9 engineered SQLi features.

### Why `updated_file.csv` matters
`updated_file.csv` should be treated as the effective SQLi training dataset used by the final pipeline. Although other related SQLi files exist in the repository, this is the dataset tied to the final saved SQLi model and should be treated as the primary source for SQLi model training.

## Emotet behavioural pipeline

### Main behavioural dataset
The Emotet behavioural side of the project is built from:

- `data/emotet/emotet_windows.csv`

This dataset contains the windowed behavioural rows derived from Zeek logs and provides the Emotet-side feature rows used when constructing the unified datasets.

### Behavioural windowing
The Emotet data is represented in short behavioural windows rather than raw packet rows or single raw flows. Each row represents summarised host behaviour over a short interval, making it suitable for tabular machine learning.

## Unified datasets

### Standard unified dataset
The main combined unified dataset is:

- `data/unified_multiclass.csv`

This dataset is the standard full multiclass dataset used for the main unified model. It combines:

- SQLi-side rows derived from `updated_file.csv`
- Emotet-side rows derived from `emotet_windows.csv`

Missing cross-domain features are aligned across the union of SQLi and Emotet features, with absent feature blocks filled to produce a single 26-feature schema.

### Balanced unified dataset
The balanced comparison dataset is:

- `data/unified_multiclass_balanced.csv`

This is a separate sampled dataset designed for class-balanced comparison experiments. It should not be treated as the same dataset as `unified_multiclass.csv`.

### Grouped evaluation dataset
The grouped evaluation dataset is:

- `data/unified_multiclass_with_groups.csv`

This dataset is separate from the standard unified dataset and should not be treated as interchangeable with it. Its purpose is evaluation under grouped splits, where `group_id` is used to keep related rows together and reduce leakage risk.

### Why the grouped dataset is distinct
`unified_multiclass_with_groups.csv` is not just `unified_multiclass.csv` with one extra column added. It serves a different evaluation purpose and contains a different class composition, especially on the Emotet side. It should therefore be discussed separately whenever grouped holdout or group-aware evaluation is being described.

## Unified saved models

### Main unified dissertation model
The main saved unified model is:

- `models/rf_unified_multiclass.joblib`

This should be treated as the primary unified multiclass dissertation model.

Its role is:
- 3-class classification
- 26-feature unified schema
- main full-data unified training setup
- weighted Random Forest variant used as the principal unified model

### Balanced comparison model
The second unified saved model is:

- `models/rf_unified_multiclass_balanced.joblib`

This is a separate comparison model trained on the balanced unified dataset. It is useful for comparison and analysis, but it should not be treated as the primary unified dissertation model.

## Main distinction between the two unified models

### `rf_unified_multiclass.joblib`
- main unified model
- trained on `data/unified_multiclass.csv`
- intended as the principal dissertation unified model
- weighted full multiclass setup

### `rf_unified_multiclass_balanced.joblib`
- comparison / experimental variant
- trained on `data/unified_multiclass_balanced.csv`
- balanced-class setup
- separate from the main dissertation model

## Practical interpretation

For normal project interpretation:

- use `rf_sqli.joblib` as the final SQLi model
- use `rf_unified_multiclass.joblib` as the main unified model
- treat `rf_unified_multiclass_balanced.joblib` as a comparison model
- treat `unified_multiclass_with_groups.csv` as a separate grouped-evaluation dataset
- treat `updated_file.csv` as the effective final SQLi training source
- treat `emotet_windows.csv` as the behavioural source feeding the Emotet side of the unified pipeline

## Final note

This note is intended to make the repository easier to understand. It does not replace the individual training, evaluation, and preprocessing scripts. Further details can be found in other papers in the Docs and Notes folder, where these datasets and scripts are also explicitly mentioned and explained. 