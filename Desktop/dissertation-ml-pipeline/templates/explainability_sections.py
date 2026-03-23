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
        feature suggests that it frequently helped the model reduce classification uncertainty, it
        carried strong discriminatory signal, and it likely represents a meaningful behavioural
        difference between classes. However, importance should always be interpreted alongside
        cybersecurity context. For example, a feature such as UNION Count is meaningful because it maps
        directly to known SQLi behaviour, while a network feature such as destination IP diversity may
        indicate broader malicious communication patterns associated with malware activity.
        </p>

        <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.7rem; font-size: 0.98rem; line-height: 1.42;">
        <strong style="font-size: 1.15rem; color: #2E3A42;">Limitations of feature importance:</strong> impurity-based importance can be biased toward
        features with higher cardinality or more possible split thresholds. Correlated features split
        importance between them, so no single correlated feature appears dominant even though the feature
        family as a whole may be highly influential. Feature importance is global, not instance-level — it
        does not explain which features drove the prediction for any individual sample.
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
        show_df["feature"] = show_df["feature"].astype(str).apply(get_feature_display_name)
        show_df["importance"] = show_df["importance"].round(4)
        show_df["group"] = show_df["feature"].apply(pretty_feature_group_fn)

        render_html_table(
            show_df[["feature", "group", "importance"]],
            compact=True,
            max_height=320,
        )

        grouped = (
            show_df.groupby("group", dropna=False)["importance"]
            .sum()
            .reset_index()
            .sort_values("importance", ascending=False)
        )
        grouped["importance"] = grouped["importance"].round(4)

        st.write("**Importance by Feature Group:**")
        render_html_table(grouped)

        st.write(
            "The near-even split (52.7% network / 47.3% query) confirms the model draws on "
            "both feature families rather than over-relying on one attack domain."
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
        "Notably, Parentheses Count matches Constant Value Count in permutation impact despite "
        "lower impurity importance — highlighting the cardinality bias of impurity-based measures. "
        "No single feature causes complete collapse, confirming distributed predictive strength."
    )


def render_importance_side_by_side(
    unified_importance: Optional[pd.DataFrame],
    pretty_feature_group_fn,
) -> None:
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        with st.container(border=True, key="explain_unified_box", height=660):
            render_unified_importance_column(
                unified_importance,
                pretty_feature_group_fn,
            )

    with col_right:
        with st.container(border=True, key="explain_permutation_box", height=660):
            render_permutation_importance_column()


def render_cross_validation_section() -> None:
    render_info_box_title("Cross-Validation Results")

    st.write(
        "5-fold stratified cross-validation was performed on the unified dataset to assess how "
        "consistently the model performs across different data partitions. Stratification ensures "
        "each fold preserves the original class distribution (Normal, SQLi, Emotet), so that "
        "performance estimates are not distorted by accidental class imbalance within individual folds."
    )

    cv_results = [
        (1, 0.972),
        (2, 0.973),
        (3, 0.982),
        (4, 0.955),
        (5, 0.967),
    ]

    st.markdown(
        "\n".join(
            [f"- Fold {fold}, Macro-F1 of {score:.3f}" for fold, score in cv_results]
        )
    )

    st.write("**Mean Macro-F1: 0.970** · **Standard Deviation: ~0.010** -- The high mean indicates consistently strong performance. The low standard deviation indicates that the model is not sensitive to which particular data partition it is trained on — performance is stable across different subsets. This low variance aligns with ensemble learning theory, where averaging predictions across multiple trees reduces instability."
    )


def render_model_comparisons_section() -> None:
    render_info_box_title("Model Comparisons")

    st.write(
        "To justify the choice of Random Forest, the model was compared against both a single "
        "decision tree and logistic regression."
    )

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.write("**Decision Tree vs Random Forest** (SQLi dataset, 5-fold CV)")
        var_data = pd.DataFrame(
            {
                "Model": ["Decision Tree", "Random Forest"],
                "Train F1": [0.997, 0.997],
                "Test F1": [0.991, 0.991],
                "CV Mean F1": [0.950, 0.961],
                "CV Std": [0.056, 0.048],
            }
        )
        render_html_table(var_data)

        st.write(
            "Both models achieve similar single-split performance, but cross-validation reveals "
            "that the decision tree has higher variance (std 0.056 vs 0.048). Random Forest "
            "reduces this instability by averaging predictions across many trees — individual "
            "trees may overfit, but their errors cancel out when combined."
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
            "Logistic regression collapses on Emotet (F1 = 0.501), demonstrating that linear "
            "decision boundaries cannot capture the complex behavioural patterns in network "
            "traffic features. Random Forest nearly doubles Emotet detection performance."
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
                "Metric": ["Train F1", "Test F1", "Gap"],
                "Value": ["0.996", "0.991", "0.005"],
            }
        )
        render_html_table(gap_data)
        st.write(
            "The small gap indicates mild but controlled overfitting — the model generalises "
            "well without significantly memorising training patterns."
        )

    with col_mid:
        st.write("**Group-Aware Holdout**")
        st.write(
            "Entire PCAP captures were held out from training to prevent Emotet data leakage."
        )
        holdout_data = pd.DataFrame(
            {
                "Split": ["Random 80/20", "Group Holdout"],
                "Macro-F1": [0.970, 0.855],
                "F1 Emotet": [0.926, 0.739],
            }
        )
        render_html_table(holdout_data)
        st.write(
            "The Emotet F1 drop (0.926 → 0.739) shows that different captures exhibit "
            "behavioural variations, making the random split optimistic."
        )

    with col_right:
        st.write("**External Validation**")
        st.write(
            "The SQLi model was tested on a Zenodo dataset (20k samples) never seen during training."
        )
        ext_data = pd.DataFrame(
            {
                "Metric": ["F1", "ROC-AUC"],
                "Internal": [0.991, 0.999],
                "External": [0.780, 0.866],
            }
        )
        render_html_table(ext_data)
        st.write(
            "The drop reflects distribution shift — the Zenodo set contains full SQL statements "
            "and different obfuscation styles. The ROC-AUC of 0.866 shows the model still "
            "distinguishes classes reasonably well."
        )


def render_limitations_section() -> None:
    render_info_box_title("Limitations")

    st.write(
        "**Feature Simplicity:** The SQLi features are surface-level counts that do not capture "
        "query semantics, token ordering, or encoding-based obfuscation. This limits generalisation "
        "to datasets with different payload structures, as demonstrated by the external validation results."
    )

    st.write(
        "**Emotet Sample Size:** The Emotet class contains significantly fewer samples (555) than "
        "Normal (22,358) or SQLi (11,382). Even with class weighting, the model has limited exposure "
        "to the full range of Emotet behavioural variation. Group-aware holdout results confirm that "
        "performance is sensitive to which specific captures the model has seen during training."
    )

    st.write(
        "**Correlated Feature Splitting:** Many SQLi features are correlated (e.g., Single Quote Count "
        "and Special Characters Total tend to increase together). When features encode overlapping signals, "
        "importance gets distributed across them, making no single feature appear dominant even though "
        "the feature family as a whole is highly influential."
    )

    st.write(
        "**Global vs Instance-Level Explanation:** Feature importance describes what was useful across "
        "the entire dataset, but does not explain which features drove the prediction for any individual "
        "sample. Instance-level methods such as SHAP could address this in future work."
    )

    st.write(
        "**No Real-Time Component:** This project demonstrates offline classification on pre-extracted "
        "features. A production deployment would require real-time feature extraction from live network "
        "streams, which introduces additional engineering challenges not addressed here."
    )


def render_bottom_row() -> None:
    with st.container(border=True, key="explain_limitations_box", height=275):
        render_limitations_section()