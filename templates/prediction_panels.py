import pandas as pd
import streamlit as st

from templates.input_controls import normalise_slider_bounds


SQLI_PREDICTION_PANEL_HEIGHT = 665


def render_feature_importance_card(df: pd.DataFrame, value_col: str = "importance") -> None:
    if df is None or df.empty:
        return

    display_df = df.reset_index(drop=True).copy()

    rows_html = ""
    for _, row in display_df.iterrows():
        feature = str(row["feature"])
        value = f"{float(row[value_col]):.4f}"

        rows_html += (
            f'<div style="display:grid;grid-template-columns:1fr 140px;'
            f'align-items:center;background:rgba(248, 245, 252, 0.6);'
            f'border-bottom:1px solid rgba(235,230,242,0.8);'
            f'transition:background 0.15s ease;">'
            f'<div style="padding:0.8rem 1rem;font-size:0.92rem;font-weight:550;color:#3D4F5A;">{feature}</div>'
            f'<div style="border-left:1px solid rgba(138,112,184,0.14);text-align:right;'
            f'padding:0.8rem 1rem;font-size:0.92rem;font-weight:650;color:#5A2D91;'
            f'font-variant-numeric:tabular-nums;">{value}</div>'
            f'</div>'
        )

    html = (
        '<div style="margin-top:0.35rem;'
        'border:1px solid rgba(138,112,184,0.30);'
        'border-radius:18px;overflow:hidden;'
        'background:linear-gradient(180deg, rgba(255,255,255,0.99) 0%, rgba(248,245,252,0.98) 100%);'
        'box-shadow:0 10px 24px rgba(92,72,125,0.08);">'
        '<div style="display:grid;grid-template-columns:1fr 140px;align-items:center;'
        'background:linear-gradient(180deg, #F3EFF8 0%, #EBE5F2 100%);'
        'border-bottom:1px solid rgba(138,112,184,0.22);">'
        '<div style="border-left:1px solid rgba(138,112,184,0.14);padding:0.75rem 1rem;'
        'font-size:0.82rem;font-weight:700;color:#5A4878;text-transform:uppercase;'
        'letter-spacing:0.04em;">Feature</div>'
        '<div style="border-left:1px solid rgba(138,112,184,0.14);text-align:right;'
        'padding:0.75rem 1rem;font-size:0.82rem;font-weight:700;color:#5A4878;'
        'text-transform:uppercase;letter-spacing:0.04em;">Importance</div>'
        '</div>'
        f'{rows_html}'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_sqli_prediction_panel(
    model,
    feature_names,
    inputs,
    threshold,
    importance,
    render_prediction_card_fn=None,
):
    from templates.helpers import render_prediction_card

    with st.container(
        border=True,
        key="sqli_prediction_box",
        height=SQLI_PREDICTION_PANEL_HEIGHT,
    ):
        st.subheader("Prediction")

        X_one = pd.DataFrame([[inputs[f] for f in feature_names]], columns=feature_names)
        proba = float(model.predict_proba(X_one)[0, 1])
        decision = "SQLi" if proba >= threshold else "Benign"

        render_prediction_card(
            "SQLi Probability",
            f"{proba:.4f}",
        )
        st.progress(proba)

        if proba >= threshold:
            st.error("Model confidence indicates likely SQL Injection.")
        else:
            st.success("Model confidence indicates benign query.")

        st.info(
            "Lower thresholds increase recall (catch more SQLi but risk more false positives). "
            "Higher thresholds increase precision (reduce false alarms but may miss attacks)."
        )

        st.write(f"**Decision (threshold = {threshold:.2f}):** `{decision}`")

        st.subheader("Top Global Features (Training)")
        if importance is not None:
            top3 = importance.head(3).copy()
            top3["importance"] = top3["importance"].round(4)
            render_feature_importance_card(top3)
        else:
            st.info("feature_importance.csv not found.")

        st.markdown('<div style="height: 0.7rem;"></div>', unsafe_allow_html=True)

    return proba, decision


def render_unified_prediction_panel(
    mode,
    unified_features,
    SQLI_FEATURES,
    EMOTET_FEATURES,
    schema_map,
    make_step_fn,
    is_int_like_fn,
    unified_model,
    CLASS_LABELS,
    render_probability_bar_fn,
    unified_importance,
    panel_height,
):
    from templates.helpers import get_feature_display_name, render_prediction_card

    with st.container(border=True, key="unified_prediction_box", height=panel_height):
        st.subheader("Unified prediction")

        unified_input = {feat: 0.0 for feat in unified_features}

        if mode in ["SQLi-style", "Hybrid"]:
            for feat in SQLI_FEATURES:
                item = schema_map[feat]
                min_v, max_v = normalise_slider_bounds(item)
                step = make_step_fn(min_v, max_v, item.get("step", "auto"))
                int_like = is_int_like_fn(step, item.get("step", "auto"))
                raw_val = st.session_state[f"ufeat_{feat}"]
                unified_input[feat] = int(round(raw_val)) if int_like else float(raw_val)

        if mode in ["Emotet-style", "Hybrid"]:
            for feat in EMOTET_FEATURES:
                unified_input[feat] = float(st.session_state[f"ufeat_{feat}"])

        X_unified = pd.DataFrame(
            [[unified_input[f] for f in unified_features]],
            columns=unified_features,
        )

        proba = unified_model.predict_proba(X_unified)[0]
        pred_class = int(unified_model.predict(X_unified)[0])
        pred_label = CLASS_LABELS[pred_class]
        pred_conf = float(max(proba))

        render_prediction_card("Predicted Class", pred_label)
        render_prediction_card("Top Confidence", f"{pred_conf:.2%}")

        if pred_class == 0:
            st.success("The unified model predicts a normal pattern.")
        elif pred_class == 1:
            st.error("The unified model predicts SQL Injection.")
        else:
            st.warning("The unified model predicts Emotet-like behaviour.")

        st.write("### Class probabilities")
        for cls, p in zip(unified_model.classes_, proba):
            render_probability_bar_fn(CLASS_LABELS[int(cls)], float(p))

        st.write("### Top Global Unified Features")
        if unified_importance is not None:
            top6 = unified_importance.head(6).copy()
            top6["feature"] = top6["feature"].apply(get_feature_display_name)
            top6["importance"] = top6["importance"].round(4)
            render_feature_importance_card(top6)
        else:
            st.info("feature_importance_unified.csv not found.")

    return proba, pred_class, pred_label, pred_conf