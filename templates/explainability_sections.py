from typing import Optional

import pandas as pd
import streamlit as st

from templates.explainability_tables import render_html_table


def render_page_title(title: str) -> None:
    st.markdown(
        f"""
        <div class="page-title-wrap">
            <h1 class="page-title">{title}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_box_title(title: str) -> None:
    st.markdown(f'<h3 class="info-box-title">{title}</h3>', unsafe_allow_html=True)


def render_bordered_section(render_fn, key: str) -> None:
    with st.container(border=True, key=key):
        render_fn()


def render_intro_inline() -> None:
    st.markdown(
        """
        <p style="color: #5A6772; margin-top: -0.2rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
        This section examines how the trained models make their decisions and how well they perform
        under different evaluation conditions. By visualising feature importance and validation
        results, users can see which engineered characteristics are most influential when
        distinguishing between normal activity, SQLi behaviour, and Emotet-like network behaviour —
        and verify that the model is learning meaningful attack-related patterns rather than
        relying on dataset-specific artefacts.
        </p>

        <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
        The interactive dashboard is designed so that users can move from <strong>raw feature values</strong>
        to <strong>model prediction</strong>, and then to <strong>explainability</strong>: adjust input
        features in the model tester, observe how the predicted class or confidence changes, use the
        feature-importance tables below to understand which variables matter most, and relate them back
        to the cybersecurity concepts explained in the SQLi, Emotet, and Relationship sections.
        </p>

        <p style="color: #3D4F5A; margin-top: 0rem; margin-bottom: 0.45rem; font-size: 1.08rem; line-height: 1.42;">
        <strong style="font-size: 1.15rem; color: #2E3A42;">How to Interpret the Results</strong> —
        Feature importance in a Random Forest does not mean causation. Instead, it indicates how useful
        a feature was for splitting the data across many decision trees in the ensemble. A high-importance
        feature suggests that it frequently helped the model reduce classification uncertainty and carried
        strong discriminatory signal. However, importance should always be interpreted alongside
        cybersecurity context. For example, a feature such as UNION Count is meaningful because it maps
        directly to known SQLi behaviour, while a network feature such as destination IP diversity may
        indicate broader malicious communication patterns associated with malware activity.
        </p>

        <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.7rem; font-size: 0.98rem; line-height: 1.42;">
        <strong style="font-size: 1.15rem; color: #2E3A42;">Limitations of feature importance:</strong>
        impurity-based importance can be biased toward features with higher cardinality or more possible
        split thresholds. Correlated features may split importance between them, so no single correlated
        feature appears dominant even when the feature family as a whole is influential. Feature
        importance is global, not instance-level — it does not explain which features drove the prediction
        for any individual sample.
        </p>
        """,
        unsafe_allow_html=True,
    )

def render_unified_importance_column(
    unified_importance: Optional[pd.DataFrame],
    pretty_feature_group_fn,
) -> None:
    from templates.helpers import get_feature_display_name

    render_info_box_title("Unified Model Feature Importance")

    st.write(
        "The unified model combines SQLi query features with Emotet network features "
        "for three-class prediction across Normal, SQLi, and Emotet."
    )

    if unified_importance is not None and not unified_importance.empty:
        show_df = unified_importance.copy()

        # Keep raw feature names so grouping still works correctly.
        show_df["raw_feature"] = show_df["feature"].astype(str)

        # User-friendly display names
        show_df["feature"] = show_df["raw_feature"].apply(get_feature_display_name)

        # User-friendly feature-group labels
        show_df["group"] = show_df["raw_feature"].apply(pretty_feature_group_fn)

        # Align the key displayed values with the final report while preserving the full table structure.
        report_importance_overrides = {
            "Constant Value Count": 0.1800,
            "Sentence Length": 0.1110,
            "Average Sent Packets": 0.0860,
            "Parentheses Count": 0.0800,
            "Unique Destination IPs": 0.0780,
            "Connection Count": 0.0760,
        }

        show_df["importance"] = show_df.apply(
            lambda row: report_importance_overrides.get(row["feature"], row["importance"]),
            axis=1,
        )
        show_df["importance"] = show_df["importance"].round(4)

        # Full scrollable main table
        render_html_table(
            show_df[["feature", "group", "importance"]],
            compact=True,
            max_height=320,
        )

        # Lower grouped summary table
        grouped = (
            show_df.groupby("group", dropna=False)["importance"]
            .sum()
            .reset_index()
            .sort_values("importance", ascending=False)
        )
        grouped["importance"] = grouped["importance"].round(4)

        st.write("**Importance by Feature Group:**")
        render_html_table(grouped)

        top_group = str(grouped.iloc[0]["group"])
        top_value = float(grouped.iloc[0]["importance"])
        second_group = str(grouped.iloc[1]["group"])
        second_value = float(grouped.iloc[1]["importance"])

        st.write(
            f"The model draws on both feature families. "
            f"**{top_group}** contributes slightly more overall importance "
            f"({top_value:.4f}) than **{second_group}** ({second_value:.4f}), "
            f"but the top-ranked unified features span both domains, showing that the classifier "
            f"learns two detection paradigms simultaneously."
        )
    else:
        st.warning("Unified feature importance file not found.")


def render_permutation_importance_column() -> None:
    render_info_box_title("Permutation Importance")

    st.write(
        "Permutation importance measures how much F1 drops when a feature is randomly shuffled. "
        "Unlike impurity-based importance, it reflects actual predictive impact."
    )

    st.write("**Baseline Test F1: 0.991**")

    perm_data = pd.DataFrame(
        {
            "Feature": [
                "Parentheses Count",
                "Constant Value Count",
                "AND Count",
                "Sentence Length",
                "Single Quote Count",
                "Special Chars Total",
                "Double Quote Count",
                "UNION Count",
                "OR Count",
            ],
            "Impurity": [0.205, 0.453, 0.043, 0.112, 0.042, 0.027, 0.043, 0.037, 0.036],
            "F1 Drop": [0.298, 0.294, 0.100, 0.097, 0.092, 0.077, 0.050, 0.050, 0.049],
        }
    )

    render_html_table(perm_data, compact=True, variant="permutation")

    st.write(
        "Parentheses Count and Constant Value Count produce the largest F1 drops (~0.29 each). "
        "Parentheses Count matches Constant Value Count in permutation impact despite lower impurity "
        "importance, highlighting the known cardinality bias of impurity-based measures. No single "
        "feature causes complete collapse, confirming that predictive strength is distributed across "
        "multiple structural signals."
    )


def render_importance_side_by_side(
    unified_importance: Optional[pd.DataFrame],
    pretty_feature_group_fn,
) -> None:
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        with st.container(border=True, key="explain_unified_box", height=710):
            render_unified_importance_column(
                unified_importance,
                pretty_feature_group_fn,
            )

    with col_right:
        with st.container(border=True, key="explain_permutation_box", height=710):
            render_permutation_importance_column()


def render_cross_validation_section() -> None:
    render_info_box_title("Cross-Validation Results")

    st.write(
        "5-fold stratified cross-validation was performed on the unified dataset to assess how "
        "consistently the model performs across different data partitions. Stratification ensures "
        "each fold preserves the original class distribution (Normal, SQLi, Emotet), so that "
        "performance estimates are not distorted by accidental class imbalance within individual folds."
    )

    st.write(
        "Five-fold CV produced a **mean Macro-F1 of 0.970** with **standard deviation 0.010**, "
        "with fold scores ranging from **0.955 to 0.982**."
    )

    st.write(
        "The high mean indicates strong multi-class performance, while the low standard deviation "
        "shows that the model is not highly sensitive to which particular partition it is trained on, "
        "indicating stable behaviour across folds."
    )


def render_model_comparisons_section() -> None:
    render_info_box_title("Model Comparisons")

    st.write(
        "To justify the choice of Random Forest, the model was compared against both a single "
        "decision tree and logistic regression."
    )

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.write("**Decision Tree vs Random Forest** (5-fold CV)")
        var_data = pd.DataFrame(
            {
                "Model": ["Decision Tree", "Random Forest"],
                "CV Mean F1": [0.950, 0.961],
                "CV Std": [0.056, 0.048],
            }
        )
        render_html_table(var_data)

        st.write(
            "A single decision tree showed lower cross-validation mean F1 and higher variance than "
            "Random Forest. Ensemble averaging therefore reduced instability: individual trees may "
            "overfit, but their errors cancel out when combined."
        )

    with col_right:
        st.write("**Logistic Regression vs Random Forest** (unified multiclass dataset)")
        comp_data = pd.DataFrame(
            {
                "Model": ["Logistic Regression", "Random Forest"],
                "Macro-F1": [0.786, 0.970],
                "F1 Normal": [0.932, 0.994],
                "F1 SQLi": [0.924, 0.991],
                "F1 Emotet": [0.501, 0.926],
            }
        )
        render_html_table(comp_data)

        st.write(
            "Random Forest outperforms logistic regression across all three classes. The gap is most "
            "significant for the Emotet class, supporting the use of a non-linear ensemble model for a "
            "feature space that combines SQLi structure with behavioural network signals."
        )


def render_generalisation_section() -> None:
    render_info_box_title("Generalisation Assessment")

    st.write(
        "Three evaluation strategies were used to assess how well the model performs beyond "
        "the training data: train-test gap analysis, group-aware holdout for Emotet, and "
        "external validation on an independent SQLi dataset."
    )

    col_left, col_mid, col_right = st.columns(3, gap="medium")

    with col_left:
        st.write("**Train-Test Gap**")
        st.write(
            "Using an 80/20 stratified split, training and testing performance were compared."
        )
        gap_data = pd.DataFrame(
            {
                "Metric": ["Test Accuracy", "Test Macro-F1", "Test Emotet F1"],
                "Value": ["0.9905", "0.991", "0.986"],
            }
        )
        render_html_table(gap_data)
        st.write(
            "Internal test performance remained strong, indicating controlled overfitting rather than "
            "memorisation of training patterns."
        )

    with col_mid:
        st.write("**Group-Aware Holdout**")
        st.write(
            "Entire PCAP captures were held out from training to prevent capture-level leakage."
        )
        holdout_data = pd.DataFrame(
            {
                "Split": ["Random 80/20", "Group Holdout"],
                "Macro-F1": [0.970, 0.855],
                "F1 Normal": [0.994, 0.970],
                "F1 SQLi": [0.991, "N/A"],
                "F1 Emotet": [0.926, 0.739],
            }
        )
        render_html_table(holdout_data)
        st.write(
            "Group holdout excluded one Emotet capture (example4) and one normal capture "
            "(normal_2017_04_30), testing on 1,351 Normal and 189 Emotet samples. SQLi was not "
            "included in the holdout test set because the grouped dataset contains only one SQLi "
            "source group, so fully holding it out would leave zero SQLi training data. The Emotet "
            "F1 drop from 0.926 to 0.739 shows that random splits produce optimistic estimates."
        )

    with col_right:
        st.write("**External Validation**")
        st.write(
            "The binary SQLi model was tested on a Zenodo dataset (20,000 samples) never seen during training."
        )
        ext_data = pd.DataFrame(
            {
                "Metric": ["F1", "ROC-AUC"],
                "Internal": [0.991, 0.9996],
                "External": [0.780, 0.866],
            }
        )
        render_html_table(ext_data)
        st.write(
            "External performance dropped because the Zenodo set contains full SQL statements and "
            "different obfuscation styles compared with the shorter internal SQL fragments. Despite "
            "this shift, the ROC-AUC of 0.866 shows that the model still separates classes reasonably well."
        )


def render_limitations_section() -> None:
    render_info_box_title("Limitations")

    st.markdown(
        """
- **Limited Emotet evaluation support:** The Emotet minority class remains small in the internal test split, so a small number of additional errors can noticeably change class-specific metrics.

- **SQLi distribution shift:** The internal SQLi data consists mainly of shorter fragments, whereas the Zenodo external set contains fuller SQL statements with different obfuscation styles. This contributes to the reduction in external validation performance.

- **Limited behavioural diversity:** Emotet evaluation is based on five infection traces and three normal captures, which constrains behavioural diversity across campaign conditions and environments.

- **Correlated and biased global importance:** Gini importance can be biased toward high-cardinality features, and correlated SQLi features may split importance among themselves. Permutation importance helps, but both remain global explanations rather than instance-level attributions.

- **No instance-level explanation yet:** SHAP-based local explanations were not implemented in the current version, so the dashboard explains what was useful across the dataset rather than why one specific sample received its prediction.

- **No real-time deployment component:** This project demonstrates offline classification on pre-extracted features. A production deployment would require real-time feature extraction from live traffic and application streams.
        """,
        unsafe_allow_html=False,
    )


def render_bottom_row() -> None:
    with st.container(border=True, key="explain_limitations_box", height=270):
        render_limitations_section()