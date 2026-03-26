import base64
import json
import os
from textwrap import dedent

import joblib
import pandas as pd
import streamlit as st

from templates.dashboard_config import (
    EMOTET_DEMO_PRESET,
    HOME_CARD_ASSET_MAP,
    HYBRID_EMOTET_DEMO_PRESET,
    HYBRID_SQLI_DEMO_PRESET,
    IMPORTANCE_PATH,
    MODEL_PATH,
    SCHEMA_PATH,
    SQLI_DEMO_PRESET,
    STATIC_DIR,
    TAB_KEYS,
    UNIFIED_EMOTET_CONFIG,
    UNIFIED_FEATURES_PATH,
    UNIFIED_IMPORTANCE_PATH,
    UNIFIED_MODEL_PATH,
)

VALID_HOME_PAGES = {
    "home",
    "sqli",
    "sqli_model",
    "emotet",
    "relationship",
}


def inject_home_card_assets() -> None:
    css_variables = []

    for css_var_name, filename in HOME_CARD_ASSET_MAP.items():
        image_path = STATIC_DIR / filename
        if image_path.exists():
            image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
            css_variables.append(
                f'--{css_var_name}: url("data:image/png;base64,{image_b64}");'
            )

    if css_variables:
        st.markdown(
            dedent(f"""
            <style>
            :root {{
                {' '.join(css_variables)}
            }}
            </style>
            """).strip(),
            unsafe_allow_html=True,
        )


def inject_tab_persistence(active_tab_key: str) -> None:
    # Kept as a no-op so existing imports/calls do not break.
    # Top-level tab persistence is now handled server-side via set_active_tab().
    return None


@st.cache_resource
def load_model():
    bundle = joblib.load(MODEL_PATH)
    return bundle["model"], bundle["feature_names"]


@st.cache_data
def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


@st.cache_data
def load_importance():
    if os.path.exists(IMPORTANCE_PATH):
        return pd.read_csv(IMPORTANCE_PATH).sort_values("importance", ascending=False)
    return None


@st.cache_resource
def load_unified_model():
    return joblib.load(UNIFIED_MODEL_PATH)


@st.cache_data
def load_unified_features():
    with open(UNIFIED_FEATURES_PATH, "r") as f:
        return json.load(f)


@st.cache_data
def load_unified_importance():
    if os.path.exists(UNIFIED_IMPORTANCE_PATH):
        return pd.read_csv(UNIFIED_IMPORTANCE_PATH).sort_values("importance", ascending=False)
    return None


def _get_valid_home_page(value: str) -> str:
    return value if value in VALID_HOME_PAGES else "home"



def _get_valid_tab_key(value: str) -> str:
    return value if value in TAB_KEYS else "home"



def sync_query_params() -> None:
    current_page = _get_valid_home_page(st.session_state.get("home_page", "home"))
    current_tab = _get_valid_tab_key(st.session_state.get("active_tab", "home"))
    st.query_params["page"] = current_page
    st.query_params["tab"] = current_tab



def initialize_session_state(defaults: dict) -> None:
    params = st.query_params

    stored_page = _get_valid_home_page(params.get("page", "home"))
    stored_tab = _get_valid_tab_key(params.get("tab", "home"))

    st.session_state.setdefault("unified_mode", "SQLi-style")
    st.session_state.setdefault("unified_presets_initialized", False)
    st.session_state.setdefault("threshold", 0.5)
    st.session_state.setdefault("home_page", stored_page)
    st.session_state.setdefault("active_tab", stored_tab)

    # Refresh from URL on every rerun so deployed refresh always restores state.
    st.session_state.home_page = stored_page
    st.session_state.active_tab = stored_tab

    for feat, val in defaults.items():
        st.session_state.setdefault(f"feat_{feat}", float(val))
        st.session_state.setdefault(f"ufeat_{feat}", float(val))

    for feat, cfg in UNIFIED_EMOTET_CONFIG.items():
        st.session_state.setdefault(f"ufeat_{feat}", float(cfg["default"]))

    sync_query_params()



def apply_sqli_preset(SQLI_FEATURES, preset: dict) -> None:
    for feat in SQLI_FEATURES:
        feat_key = str(feat).strip().lower()
        if feat_key in preset:
            st.session_state[f"ufeat_{feat}"] = float(preset[feat_key])



def apply_emotet_preset(preset: dict) -> None:
    for feat, val in preset.items():
        state_key = f"ufeat_{feat}"
        if state_key in st.session_state:
            st.session_state[state_key] = float(val)



def reset_to_defaults(defaults: dict) -> None:
    st.session_state["threshold"] = 0.5
    for feat, val in defaults.items():
        st.session_state[f"feat_{feat}"] = float(val)



def apply_unified_mode_presets(defaults: dict, SQLI_FEATURES) -> None:
    mode = st.session_state.get("unified_mode", "SQLi-style")

    for feat, val in defaults.items():
        st.session_state[f"ufeat_{feat}"] = float(val)

    for feat, cfg in UNIFIED_EMOTET_CONFIG.items():
        st.session_state[f"ufeat_{feat}"] = float(cfg["default"])

    if mode == "SQLi-style":
        apply_sqli_preset(SQLI_FEATURES, SQLI_DEMO_PRESET)
    elif mode == "Emotet-style":
        apply_emotet_preset(EMOTET_DEMO_PRESET)
    elif mode == "Hybrid":
        apply_sqli_preset(SQLI_FEATURES, HYBRID_SQLI_DEMO_PRESET)
        apply_emotet_preset(HYBRID_EMOTET_DEMO_PRESET)



def reset_unified_defaults(defaults: dict, SQLI_FEATURES) -> None:
    apply_unified_mode_presets(defaults, SQLI_FEATURES)



def go_home() -> None:
    st.session_state.home_page = "home"
    sync_query_params()



def go_page(page: str) -> None:
    st.session_state.home_page = _get_valid_home_page(page)
    st.session_state.active_tab = "home"
    sync_query_params()



def set_active_tab(tab_key: str) -> None:
    st.session_state.active_tab = _get_valid_tab_key(tab_key)
    sync_query_params()



def ensure_unified_presets_initialized(defaults: dict, SQLI_FEATURES) -> None:
    if not st.session_state["unified_presets_initialized"]:
        apply_unified_mode_presets(defaults, SQLI_FEATURES)
        st.session_state["unified_presets_initialized"] = True



def get_unified_prediction_panel_height(mode: str) -> int:
    if mode == "SQLi-style":
        return 760
    if mode == "Emotet-style":
        return 930
    return 930
