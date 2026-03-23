from templates.input_controls import (
    HYBRID_PANEL_HEIGHT,
    SQLI_FEATURE_SLIDERS_HEIGHT,
    UNIFIED_EMOTET_INPUTS_HEIGHT,
    UNIFIED_MODES,
    UNIFIED_SQLI_INPUTS_HEIGHT,
    render_sqli_controls,
    render_sqli_feature_sliders,
    render_unified_emotet_inputs,
    render_unified_hybrid_inputs,
    render_unified_mode_selector,
    render_unified_sqli_inputs,
)
from templates.prediction_panels import (
    SQLI_PREDICTION_PANEL_HEIGHT,
    render_feature_importance_card,
    render_sqli_prediction_panel,
    render_unified_prediction_panel,
)


def render_sqli_feature_explanations():
    from templates.helpers import render_feature_explanation_html, SQLI_FEATURE_EXPLANATIONS
    import streamlit as st

    with st.container(border=True, key="sqli_feature_explain_box"):
        st.markdown(
            '<h3 class="info-box-title">Feature Descriptions</h3>',
            unsafe_allow_html=True,
        )
        st.write(
            "These features are entirely numeric, making them directly usable by the Random Forest classifier without requiring text vectorisation or natural language processing."
        )
        st.markdown(
            render_feature_explanation_html(SQLI_FEATURE_EXPLANATIONS),
            unsafe_allow_html=True,
        )


def render_sqli_feature_importance_section(importance):
    import streamlit as st

    with st.container(border=True, key="sqli_importance_section_box"):
        st.markdown(
            '<h3 class="info-box-title">SQLi Model Feature Importance</h3>',
            unsafe_allow_html=True,
        )
        st.write(
            "The SQLi model was trained on nine engineered payload features. "
            "Importance is measured by Mean Decrease in Impurity (Gini) across all 300 trees. "
            "Higher importance means the model relied more heavily on that feature when "
            "separating malicious SQL injection inputs from benign queries. "
            "The model's behaviour is driven by structural properties — Constant Value Count and "
            "Parentheses Count — rather than isolated SQL keywords. Structural signals generalise "
            "better across datasets than keyword tokens, which can be easily obfuscated."
        )

        if importance is not None and not importance.empty:
            show_df = importance.copy()
            show_df["feature"] = show_df["feature"].astype(str)
            show_df["importance"] = show_df["importance"].round(4)
            render_feature_importance_card(show_df)

            st.markdown('<div style="height: 0.6rem;"></div>', unsafe_allow_html=True)

            top3 = show_df.head(3)["feature"].tolist()
            if len(top3) >= 3:
                st.info(
                    f"Top SQLi features: **{top3[0]}**, **{top3[1]}**, and **{top3[2]}**."
                )
        else:
            st.info("SQLi feature importance data not available.")


def render_emotet_feature_explanations():
    from templates.helpers import render_feature_explanation_html, EMOTET_FEATURE_EXPLANATIONS
    import streamlit as st

    with st.container(border=True, key="emotet_feature_explain_box"):
        st.markdown(
            '<h3 class="info-box-title">Emotet Feature Descriptions</h3>',
            unsafe_allow_html=True,
        )
        st.write(
            "Together, these features describe how a host communicates rather than what it communicates. This allows the model to identify infected hosts even when the traffic content is encrypted or the malware binary has been obfuscated."
        )
        st.markdown(
            render_feature_explanation_html(EMOTET_FEATURE_EXPLANATIONS),
            unsafe_allow_html=True,
        )


__all__ = [
    "UNIFIED_MODES",
    "SQLI_FEATURE_SLIDERS_HEIGHT",
    "SQLI_PREDICTION_PANEL_HEIGHT",
    "UNIFIED_SQLI_INPUTS_HEIGHT",
    "UNIFIED_EMOTET_INPUTS_HEIGHT",
    "HYBRID_PANEL_HEIGHT",
    "render_feature_importance_card",
    "render_sqli_controls",
    "render_sqli_feature_sliders",
    "render_sqli_prediction_panel",
    "render_sqli_feature_explanations",
    "render_sqli_feature_importance_section",
    "render_unified_mode_selector",
    "render_unified_sqli_inputs",
    "render_unified_emotet_inputs",
    "render_unified_hybrid_inputs",
    "render_unified_prediction_panel",
    "render_emotet_feature_explanations",
]