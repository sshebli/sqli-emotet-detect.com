from textwrap import dedent

import streamlit as st

from templates.explainability import render_explainability_tab
from templates.model_inputs import (
    render_emotet_feature_explanations,
    render_sqli_controls,
    render_sqli_feature_explanations,
    render_sqli_feature_importance_section,
    render_sqli_feature_sliders,
    render_sqli_prediction_panel,
    render_unified_emotet_inputs,
    render_unified_hybrid_inputs,
    render_unified_mode_selector,
    render_unified_prediction_panel,
    render_unified_sqli_inputs,
)
from templates.quiz import render_quiz_tab
from templates.ui_renderers import (
    render_emotet_info_page,
    render_home_about_sections,
    render_home_card_grid,
    render_home_intro,
    render_pipeline_info_page,
    render_relationship_info_page,
    render_sqli_info_page,
)

MAIN_NAV_KEY = "main_nav_selection"


def _sync_nav_to_query(TAB_NAMES, TAB_KEYS) -> str:
    key_to_name = dict(zip(TAB_KEYS, TAB_NAMES))
    name_to_key = dict(zip(TAB_NAMES, TAB_KEYS))

    requested_key = st.query_params.get("tab", "home")
    default_name = key_to_name.get(requested_key, TAB_NAMES[0])

    if MAIN_NAV_KEY not in st.session_state:
        st.session_state[MAIN_NAV_KEY] = default_name

    current_name = st.session_state.get(MAIN_NAV_KEY, default_name)
    if requested_key in key_to_name and current_name != key_to_name[requested_key]:
        st.session_state[MAIN_NAV_KEY] = key_to_name[requested_key]
        current_name = st.session_state[MAIN_NAV_KEY]

    selected_key = name_to_key.get(current_name, TAB_KEYS[0])
    if st.query_params.get("tab", None) != selected_key:
        st.query_params["tab"] = selected_key

    return current_name


def render_page_title(title: str) -> None:
    st.markdown(
        dedent(
            f"""
        <div class="page-title-wrap">
            <h1 class="page-title">{title}</h1>
        </div>
        """
        ).strip(),
        unsafe_allow_html=True,
    )


def render_home_tab(
    go_home,
    go_page,
    reset_to_defaults_fn,
    feature_names,
    schema_map,
    make_step,
    is_int_like,
    model,
    importance,
):
    page = st.session_state.home_page

    if page == "home":
        render_home_intro()
        render_home_card_grid(go_page)
        render_home_about_sections()
        return

    if page == "sqli":
        render_sqli_info_page(go_home_fn=go_home, go_page_fn=go_page)
        return

    if page == "sqli_model":
        with st.container(key="back_home_wrap"):
            st.button("Back to SQLi Page", on_click=go_page, args=("sqli",))

        render_page_title("SQLi Model Tester")
        st.markdown(
            """
            <p style="color: #5A6772; margin-top: -0.2rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
            This page provides an interactive interface for testing the binary SQL injection classifier. The model is a Random Forest trained on 30,919 labelled queries using nine structural features that capture how a query is constructed — operator frequency, quote usage, numeric literal counts, and overall complexity. Users can adjust individual feature values using the sliders below and observe how the model's predicted probability changes in real time.
            </p>

            <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
            The <strong>decision threshold</strong> controls the boundary between a benign and malicious classification. At the default threshold of 0.50, any input with a predicted SQLi probability above 50% is flagged as malicious. Lowering the threshold increases recall (catches more attacks but risks more false positives), while raising it increases precision (fewer false alarms but may miss some attacks).
            </p>

            <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.7rem; font-size: 0.98rem; line-height: 1.42;">
            For detailed validation results, feature importance analysis, and model comparison metrics, see the <strong>Explainability</strong> tab.
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        with st.container(key="sqli_tester_row"):
            left_col, right_col = st.columns([1, 1], gap="large")

            with left_col:
                render_sqli_controls(reset_to_defaults_fn)
                threshold = float(st.session_state["threshold"])
                st.write("")
                inputs = render_sqli_feature_sliders(
                    feature_names=feature_names,
                    schema_map=schema_map,
                    make_step_fn=make_step,
                    is_int_like_fn=is_int_like,
                )

            with right_col:
                render_sqli_prediction_panel(
                    model=model,
                    feature_names=feature_names,
                    inputs=inputs,
                    threshold=threshold,
                    importance=importance,
                )

        render_sqli_feature_explanations("sqli_feature_explain_box_main")
        render_sqli_feature_importance_section(importance)
        return

    if page == "emotet":
        render_emotet_info_page(go_home)
        return

    if page == "relationship":
        render_relationship_info_page(go_home)
        return


def render_unified_tab(
    reset_unified_defaults_fn,
    apply_unified_mode_presets_fn,
    SQLI_FEATURES,
    EMOTET_FEATURES,
    schema_map,
    UNIFIED_EMOTET_CONFIG,
    make_step,
    is_int_like,
    unified_features,
    unified_model,
    CLASS_LABELS,
    render_probability_bar,
    unified_importance,
    get_unified_prediction_panel_height_fn,
):
    render_page_title("Unified Model Tester")

    st.markdown(
        """
        <p style="color: #5A6772; margin-top: -0.2rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
        This page provides an interactive interface for testing the unified multi-class classifier. The model is a Random Forest trained on a combined dataset of 34,295 samples using 26 features — nine structural features from SQL injection payloads and seventeen behavioural features from Emotet network traffic. It classifies input as <strong>Normal</strong>, <strong>SQLi</strong>, or <strong>Emotet</strong> within a single prediction.
        </p>

        <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
        Three <strong>test modes</strong> are available: <strong>SQLi-style</strong> edits only SQLi features while Emotet features are set to zero, <strong>Emotet-style</strong> edits only Emotet features while SQLi features are set to zero, and <strong>Hybrid</strong> makes both feature groups editable simultaneously. The selected mode controls which features are active, but the model still decides the final class based on the full 26-feature input.
        </p>

        <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 2rem; font-size: 0.98rem; line-height: 1.42;">
        For detailed validation results, feature importance analysis, and model comparison metrics, see the <strong>Explainability</strong> tab.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    with st.container(key="unified_tester_row"):
        left_col, right_col = st.columns([1, 1], gap="large")

        with left_col:
            mode = render_unified_mode_selector(
                reset_unified_defaults_fn,
                apply_unified_mode_presets_fn,
            )

            if mode == "SQLi-style":
                render_unified_sqli_inputs(
                    SQLI_FEATURES=SQLI_FEATURES,
                    schema_map=schema_map,
                    make_step_fn=make_step,
                )
            elif mode == "Emotet-style":
                render_unified_emotet_inputs(
                    EMOTET_FEATURES=EMOTET_FEATURES,
                    UNIFIED_EMOTET_CONFIG=UNIFIED_EMOTET_CONFIG,
                )
            else:
                render_unified_hybrid_inputs(
                    SQLI_FEATURES=SQLI_FEATURES,
                    EMOTET_FEATURES=EMOTET_FEATURES,
                    schema_map=schema_map,
                    UNIFIED_EMOTET_CONFIG=UNIFIED_EMOTET_CONFIG,
                    make_step_fn=make_step,
                )

        with right_col:
            render_unified_prediction_panel(
                mode=mode,
                unified_features=unified_features,
                SQLI_FEATURES=SQLI_FEATURES,
                EMOTET_FEATURES=EMOTET_FEATURES,
                schema_map=schema_map,
                make_step_fn=make_step,
                is_int_like_fn=is_int_like,
                unified_model=unified_model,
                CLASS_LABELS=CLASS_LABELS,
                render_probability_bar_fn=render_probability_bar,
                unified_importance=unified_importance,
                panel_height=get_unified_prediction_panel_height_fn(mode),
            )

    mode = st.session_state.get("unified_mode", "SQLi-style")
    if mode == "SQLi-style":
        render_sqli_feature_explanations("sqli_feature_explain_box_unified")
    elif mode == "Emotet-style":
        render_emotet_feature_explanations()


def render_main_tabs(
    TAB_NAMES,
    TAB_KEYS,
    active_tab_key,
    inject_tab_persistence_fn,
    render_home_tab_fn,
    render_unified_tab_fn,
    importance,
    unified_importance,
    pretty_feature_group_fn,
    go_home,
):
    selected_name = _sync_nav_to_query(TAB_NAMES, TAB_KEYS)

    st.radio(
        label="Main navigation",
        options=TAB_NAMES,
        key=MAIN_NAV_KEY,
        horizontal=True,
        label_visibility="collapsed",
    )

    name_to_key = dict(zip(TAB_NAMES, TAB_KEYS))
    selected_name = st.session_state.get(MAIN_NAV_KEY, selected_name)
    selected_key = name_to_key.get(selected_name, TAB_KEYS[0])

    if st.query_params.get("tab", None) != selected_key:
        st.query_params["tab"] = selected_key

    if selected_key == "home":
        render_home_tab_fn()
    elif selected_key == "unified":
        render_unified_tab_fn()
    elif selected_key == "pipeline":
        render_pipeline_info_page(go_home)
    elif selected_key == "explain":
        with st.spinner("Loading explainability..."):
            render_explainability_tab(
                importance=importance,
                unified_importance=unified_importance,
                pretty_feature_group_fn=pretty_feature_group_fn,
            )
    elif selected_key == "quiz":
        with st.spinner("Loading quiz..."):
            render_quiz_tab()
    else:
        render_home_tab_fn()