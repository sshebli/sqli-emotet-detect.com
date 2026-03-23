from textwrap import dedent

import streamlit as st


def make_step(min_v, max_v, configured_step="auto"):
    if configured_step != "auto":
        return float(configured_step)

    span = float(max_v) - float(min_v)

    if span <= 10:
        return 1.0
    elif span <= 100:
        return 1.0
    elif span <= 1000:
        return 5.0
    else:
        return max(1.0, round(span / 100.0, 2))


def is_int_like(step, configured_step="auto"):
    if configured_step != "auto":
        try:
            return float(configured_step).is_integer()
        except Exception:
            return False

    try:
        return float(step).is_integer()
    except Exception:
        return False


def _html(text: str) -> str:
    return dedent(text).strip()


def render_probability_bar(label, value):
    pct = max(0.0, min(1.0, float(value)))
    percent = pct * 100.0

    label_clean = str(label).strip().lower()

    if label_clean == "normal":
        fill = "linear-gradient(90deg,#2D8C73,#3DAA8B)"
    elif label_clean == "sqli":
        fill = "linear-gradient(90deg,#D9534F,#F06A6A)"
    elif label_clean == "emotet":
        fill = "linear-gradient(90deg,#C98A2E,#E7A93B)"
    else:
        fill = "linear-gradient(90deg,#5F6C73,#7B8790)"

    html = (
        f'<div style="margin-bottom:12px;">'
        f'  <div style="display:flex;justify-content:space-between;'
        f'      font-size:0.9rem;margin-bottom:4px;color:#2C3A40;">'
        f'    <span>{label}</span>'
        f'    <span>{percent:.1f}%</span>'
        f'  </div>'
        f'  <div style="width:100%;height:10px;background:#E6ECEF;'
        f'      border-radius:6px;overflow:hidden;">'
        f'    <div style="width:{percent:.1f}%;height:100%;background:{fill};'
        f'        border-radius:6px;transition:width 0.3s ease;"></div>'
        f'  </div>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_prediction_card(label, value, sub_text=""):
    sub_html = ""
    if sub_text:
        sub_html = (
            '<div style="font-size:0.85rem;color:#7A6B8E;'
            f'margin-top:0.25rem;">{sub_text}</div>'
        )

    html = _html(f"""
    <div style="
        background: linear-gradient(135deg, #F6F0FB 0%, #EDE5F6 100%);
        border: 1px solid rgba(138, 112, 184, 0.35);
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 24px rgba(92, 72, 125, 0.10);
    ">
        <div style="
            font-size:0.82rem;
            font-weight:600;
            color:#6C5A7E;
            text-transform:uppercase;
            letter-spacing:0.06em;
            margin-bottom:0.3rem;
        ">{label}</div>
        <div style="
            font-size:2rem;
            font-weight:750;
            color:#3D2B5A;
            letter-spacing:-0.03em;
            line-height:1.1;
            font-variant-numeric:tabular-nums;
        ">{value}</div>
        {sub_html}
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)


def render_feature_explanation_html(explanations: dict) -> str:
    items = list(explanations.items())
    num_columns = 3
    columns = [[] for _ in range(num_columns)]

    for idx, item in enumerate(items):
        columns[idx % num_columns].append(item)

    def _card(feat, desc):
        return _html(f"""
        <div style="
            background: rgba(248, 245, 252, 0.6);
            border: 1px solid rgba(138, 112, 184, 0.18);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 10px;
        ">
            <div style="
                font-size:0.88rem;
                font-weight:700;
                color:#5A2D91;
                margin-bottom:0.2rem;
            ">{feat}</div>
            <div style="
                font-size:0.88rem;
                color:#4D5D66;
                line-height:1.35;
            ">{desc}</div>
        </div>
        """)

    column_html = []
    for col_items in columns:
        cards_html = "".join(_card(f, d) for f, d in col_items)
        column_html.append(f'<div style="flex:1;min-width:0;">{cards_html}</div>')

    return _html(f"""
    <div style="
        display:flex;
        gap:16px;
        margin-top:0.5rem;
        align-items:flex-start;
    ">
        {''.join(column_html)}
    </div>
    """)