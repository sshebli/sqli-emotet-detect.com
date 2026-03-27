import streamlit as st

from templates.components import load_css
from templates.dashboard_config import (
    CLASS_LABELS,
    TAB_KEYS,
    TAB_NAMES,
    UNIFIED_EMOTET_CONFIG,
)
from templates.dashboard_runtime import (
    ensure_unified_presets_initialized,
    get_unified_prediction_panel_height,
    go_home,
    go_page,
    initialize_session_state,
    inject_home_card_assets,
    inject_tab_persistence,
    load_importance,
    load_model,
    load_schema,
    load_unified_features,
    load_unified_importance,
    load_unified_model,
    reset_to_defaults,
    reset_unified_defaults,
)
from templates.dashboard_tabs import (
    render_home_tab,
    render_main_tabs,
    render_unified_tab,
)
from templates.helpers import (
    is_int_like,
    make_step,
    pretty_feature_group,
    render_probability_bar,
)
from templates.ui_renderers import render_dashboard_hero


st.set_page_config(
    page_title="SQLi & Emotet Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
)
load_css()
inject_home_card_assets()

render_dashboard_hero()

model, feature_names = load_model()
schema = load_schema()
importance = load_importance()

unified_model = load_unified_model()
unified_features = load_unified_features()
unified_importance = load_unified_importance()


@st.cache_data
def _build_schema_map(_schema: tuple) -> dict:
    return {item["feature"]: item for item in _schema}


@st.cache_data
def _build_defaults(_schema: tuple) -> dict:
    return {item["feature"]: float(item["default"]) for item in _schema}


@st.cache_data
def _build_feature_lists(
    _feature_names: tuple, _unified_features: tuple
) -> tuple:
    sqli = list(_feature_names)
    emotet = [
        f for f in _unified_features
        if f not in sqli and f not in ["y", "group_id"]
    ]
    return sqli, emotet


# Convert lists to tuples so st.cache_data can hash them
schema_map = _build_schema_map(tuple(schema))
defaults = _build_defaults(tuple(schema))
SQLI_FEATURES, EMOTET_FEATURES = _build_feature_lists(
    tuple(feature_names), tuple(unified_features)
)

initialize_session_state(defaults)
ensure_unified_presets_initialized(defaults, SQLI_FEATURES)

requested_tab = st.query_params.get("tab", "home")
active_tab_key = requested_tab if requested_tab in TAB_KEYS else "home"


def _reset_to_defaults() -> None:
    reset_to_defaults(defaults)


def _reset_unified_defaults() -> None:
    reset_unified_defaults(defaults, SQLI_FEATURES)


def _apply_unified_mode_presets() -> None:
    from templates.dashboard_runtime import apply_unified_mode_presets
    apply_unified_mode_presets(defaults, SQLI_FEATURES)


def _render_home_tab() -> None:
    render_home_tab(
        go_home=go_home,
        go_page=go_page,
        reset_to_defaults_fn=_reset_to_defaults,
        feature_names=feature_names,
        schema_map=schema_map,
        make_step=make_step,
        is_int_like=is_int_like,
        model=model,
        importance=importance,
    )


def _render_unified_tab() -> None:
    render_unified_tab(
        reset_unified_defaults_fn=_reset_unified_defaults,
        apply_unified_mode_presets_fn=_apply_unified_mode_presets,
        SQLI_FEATURES=SQLI_FEATURES,
        EMOTET_FEATURES=EMOTET_FEATURES,
        schema_map=schema_map,
        UNIFIED_EMOTET_CONFIG=UNIFIED_EMOTET_CONFIG,
        make_step=make_step,
        is_int_like=is_int_like,
        unified_features=unified_features,
        unified_model=unified_model,
        CLASS_LABELS=CLASS_LABELS,
        render_probability_bar=render_probability_bar,
        unified_importance=unified_importance,
        get_unified_prediction_panel_height_fn=get_unified_prediction_panel_height,
    )


render_main_tabs(
    TAB_NAMES=TAB_NAMES,
    TAB_KEYS=TAB_KEYS,
    active_tab_key=active_tab_key,
    inject_tab_persistence_fn=inject_tab_persistence,
    render_home_tab_fn=_render_home_tab,
    render_unified_tab_fn=_render_unified_tab,
    importance=importance,
    unified_importance=unified_importance,
    pretty_feature_group_fn=pretty_feature_group,
    go_home=go_home,
)