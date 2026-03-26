import base64
import json
import os
from textwrap import dedent

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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
    "pipeline",
}


def _normalize_query_value(value, default: str) -> str:
    if value is None:
        return default

    if isinstance(value, (list, tuple)):
        if not value:
            return default
        value = value[0]

    value = str(value).strip()
    return value or default


def _get_requested_home_page() -> str:
    requested_page = _normalize_query_value(st.query_params.get("page", "home"), "home")
    if requested_page not in VALID_HOME_PAGES:
        return "home"
    return requested_page


def _set_home_page_state(page: str) -> None:
    target_page = page if page in VALID_HOME_PAGES else "home"
    st.session_state["home_page"] = target_page
    st.query_params["page"] = target_page


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
    keys_json = json.dumps(TAB_KEYS)
    active_json = json.dumps(active_tab_key)

    components.html(
        f"""
        <script>
        (function() {{
            const KEYS = {keys_json};
            const ACTIVE = {active_json};
            const MAX_RETRIES = 30;
            const RETRY_MS = 100;

            function setUrlTab(key) {{
                const url = new URL(window.parent.location.href);
                url.searchParams.set("tab", key);
                window.parent.history.replaceState({{}}, "", url.toString());
            }}

            function getTabButtons() {{
                return window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
            }}

            function attachListeners() {{
                const btns = getTabButtons();
                btns.forEach((btn, i) => {{
                    if (btn.__tabPersistPatched) return;
                    btn.__tabPersistPatched = true;

                    btn.addEventListener("click", () => {{
                        const key = KEYS[i] || "home";
                        setUrlTab(key);
                    }});
                }});
            }}

            function restoreActiveTab() {{
                const btns = getTabButtons();
                const idx = KEYS.indexOf(ACTIVE);
                if (idx >= 0 && btns[idx]) {{
                    if (btns[idx].getAttribute("aria-selected") !== "true") {{
                        btns[idx].click();
                    }}
                    return true;
                }}
                return false;
            }}

            function initWithRetry(attempt) {{
                attachListeners();
                if (restoreActiveTab()) return;
                if (attempt < MAX_RETRIES) {{
                    setTimeout(() => initWithRetry(attempt + 1), RETRY_MS);
                }}
            }}

            if (ACTIVE !== "home") {{
                initWithRetry(0);
            }} else {{
                setTimeout(attachListeners, 200);
            }}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


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


def initialize_session_state(defaults: dict) -> None:
    st.session_state.setdefault("unified_mode", "SQLi-style")
    st.session_state.setdefault("unified_presets_initialized", False)
    st.session_state.setdefault("threshold", 0.5)

    requested_page = _get_requested_home_page()
    current_page = st.session_state.get("home_page")

    if current_page not in VALID_HOME_PAGES:
        st.session_state["home_page"] = requested_page
    elif current_page != requested_page:
        st.session_state["home_page"] = requested_page

    for feat, val in defaults.items():
        st.session_state.setdefault(f"feat_{feat}", float(val))
        st.session_state.setdefault(f"ufeat_{feat}", float(val))

    for feat, cfg in UNIFIED_EMOTET_CONFIG.items():
        st.session_state.setdefault(f"ufeat_{feat}", float(cfg["default"]))


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
    _set_home_page_state("home")


def go_page(page: str) -> None:
    _set_home_page_state(page)


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
