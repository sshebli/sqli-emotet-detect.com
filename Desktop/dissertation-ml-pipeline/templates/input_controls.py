import streamlit as st


UNIFIED_MODES = ["SQLi-style", "Emotet-style", "Hybrid"]

SQLI_FEATURE_SLIDERS_HEIGHT = 520
UNIFIED_SQLI_INPUTS_HEIGHT = 630
UNIFIED_EMOTET_INPUTS_HEIGHT = 800
HYBRID_PANEL_HEIGHT = 750


def control_row_button_spacer() -> None:
    st.markdown('<div style="height: 2.2rem;"></div>', unsafe_allow_html=True)


def normalise_slider_bounds(item):
    min_v = float(item["min"])
    max_v = float(item["max"])

    if min_v > max_v:
        min_v, max_v = max_v, min_v

    return min_v, max_v


def is_integer_step(step: float) -> bool:
    return abs(float(step) - 1.0) < 1e-9


def render_feature_slider(
    feat,
    item,
    slider_key,
    make_step_fn,
    is_int_like_fn=None,
    return_value=False,
):
    min_v, max_v = normalise_slider_bounds(item)
    step = make_step_fn(min_v, max_v, item.get("step", "auto"))

    slider_value = st.slider(
        feat,
        min_value=float(min_v),
        max_value=float(max_v),
        step=step,
        key=slider_key,
    )

    if not return_value:
        return None

    int_like = (
        is_int_like_fn(step, item.get("step", "auto")) if is_int_like_fn else False
    )
    return int(round(slider_value)) if int_like else float(slider_value)


def render_emotet_number_input(feat, cfg, key_prefix: str = "ufeat_") -> None:
    from templates.helpers import get_feature_display_name

    use_int = is_integer_step(cfg["step"])

    st.number_input(
        get_feature_display_name(feat),
        min_value=int(cfg["min"]) if use_int else float(cfg["min"]),
        max_value=int(cfg["max"]) if use_int else float(cfg["max"]),
        step=int(cfg["step"]) if use_int else float(cfg["step"]),
        key=f"{key_prefix}{feat}",
    )


def render_sqli_slider_group(
    feature_names,
    schema_map,
    make_step_fn,
    is_int_like_fn=None,
    slider_key_prefix: str = "feat_",
    columns: int = 2,
    return_inputs: bool = False,
):
    inputs = {}
    column_refs = st.columns(columns, gap="large")

    for idx, feat in enumerate(feature_names):
        item = schema_map[feat]
        with column_refs[idx % columns]:
            value = render_feature_slider(
                feat=feat,
                item=item,
                slider_key=f"{slider_key_prefix}{feat}",
                make_step_fn=make_step_fn,
                is_int_like_fn=is_int_like_fn,
                return_value=return_inputs,
            )
            if return_inputs:
                inputs[feat] = value

    return inputs if return_inputs else None


def render_sqli_controls(reset_to_defaults_fn):
    with st.container(border=True, key="sqli_controls_box"):
        col1, col2 = st.columns([3, 1], gap="medium")

        with col1:
            st.subheader("Decision Threshold")
            st.slider(
                "Decision threshold slider",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                key="threshold",
                label_visibility="collapsed",
            )

        with col2:
            control_row_button_spacer()
            st.button("Reset to defaults", on_click=reset_to_defaults_fn)


def render_sqli_feature_sliders(feature_names, schema_map, make_step_fn, is_int_like_fn):
    with st.container(
        border=True,
        key="sqli_feature_sliders_box",
        height=SQLI_FEATURE_SLIDERS_HEIGHT,
    ):
        st.subheader("Feature sliders")
        inputs = render_sqli_slider_group(
            feature_names=feature_names,
            schema_map=schema_map,
            make_step_fn=make_step_fn,
            is_int_like_fn=is_int_like_fn,
            slider_key_prefix="feat_",
            columns=2,
            return_inputs=True,
        )

    return inputs


def render_unified_mode_selector(reset_unified_defaults_fn, apply_unified_mode_presets_fn):
    with st.container(border=True, key="unified_mode_selector_box"):
        top_left, top_right = st.columns([3, 1], gap="medium")

        with top_left:
            st.subheader("Test Mode")
            mode = st.radio(
                "Unified test mode selector",
                options=UNIFIED_MODES,
                horizontal=True,
                key="unified_mode",
                on_change=apply_unified_mode_presets_fn,
                label_visibility="collapsed",
            )

        with top_right:
            control_row_button_spacer()
            st.button("Reset unified inputs", on_click=reset_unified_defaults_fn)

    return mode


def render_unified_sqli_inputs(SQLI_FEATURES, schema_map, make_step_fn):
    with st.container(
        border=True,
        key="unified_sqli_inputs_box",
        height=UNIFIED_SQLI_INPUTS_HEIGHT,
    ):
        st.markdown(
            """
            <h3 style="margin: 0 0 10px 0;">SQLi feature inputs</h3>
            """,
            unsafe_allow_html=True,
        )
        render_sqli_slider_group(
            feature_names=SQLI_FEATURES,
            schema_map=schema_map,
            make_step_fn=make_step_fn,
            slider_key_prefix="ufeat_",
            columns=2,
            return_inputs=False,
        )


def render_unified_emotet_inputs(EMOTET_FEATURES, UNIFIED_EMOTET_CONFIG):
    with st.container(
        border=True,
        key="unified_emotet_inputs_box",
        height=UNIFIED_EMOTET_INPUTS_HEIGHT,
    ):
        st.subheader("Emotet/network feature inputs")

        col_left, col_right = st.columns(2, gap="large")
        half = (len(EMOTET_FEATURES) + 1) // 2

        for idx, feat in enumerate(EMOTET_FEATURES):
            with col_left if idx < half else col_right:
                render_emotet_number_input(feat, UNIFIED_EMOTET_CONFIG[feat])


def render_unified_hybrid_inputs(
    SQLI_FEATURES,
    EMOTET_FEATURES,
    schema_map,
    UNIFIED_EMOTET_CONFIG,
    make_step_fn,
):
    hybrid_left, hybrid_right = st.columns([1, 1], gap="large")

    with hybrid_left:
        st.subheader("SQLi feature inputs")
        with st.container(border=True, key="hybrid_sqli_inputs_box", height=HYBRID_PANEL_HEIGHT):
            for feat in SQLI_FEATURES:
                render_feature_slider(
                    feat=feat,
                    item=schema_map[feat],
                    slider_key=f"ufeat_{feat}",
                    make_step_fn=make_step_fn,
                    return_value=False,
                )

    with hybrid_right:
        st.subheader("Emotet/network feature inputs")
        with st.container(border=True, key="hybrid_emotet_inputs_box", height=HYBRID_PANEL_HEIGHT):
            for feat in EMOTET_FEATURES:
                render_emotet_number_input(feat, UNIFIED_EMOTET_CONFIG[feat])