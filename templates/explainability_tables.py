import html
from typing import Optional, Union

import pandas as pd
import streamlit as st


def inject_explainability_table_css() -> None:
    st.markdown(
        """
        <style>
        .explain-table-wrap {
          margin-top: 0.55rem;
          margin-bottom: 0.7rem;
          width: 100%;
        }

        .explain-table {
          width: 100%;
          border-collapse: separate;
          border-spacing: 0;
          border: 1px solid rgba(214, 204, 224, 0.55);
          border-radius: 12px;
          overflow: hidden;
          background: rgba(255, 255, 255, 0.72);
          font-size: 0.94rem;
          color: #3D4F5A;
        }

        .explain-table-compact {
          font-size: 0.86rem;
        }

        .explain-table thead th {
          background: #F3EFF8;
          color: #5A4878;
          font-weight: 700;
          padding: 0.78rem 0.95rem;
          border-bottom: 1px solid rgba(214, 204, 224, 0.7);
          border-right: 1px solid rgba(232, 226, 240, 0.85);
          text-align: left;
          white-space: nowrap;
        }

        .explain-table-compact thead th {
          padding: 0.52rem 0.7rem;
        }

        .explain-table thead th:last-child {
          border-right: none;
        }

        .explain-table tbody td {
          padding: 0.78rem 0.95rem;
          border-bottom: 1px solid rgba(232, 226, 240, 0.8);
          border-right: 1px solid rgba(232, 226, 240, 0.65);
          color: #3D4F5A;
          background: rgba(255, 255, 255, 0.55);
          vertical-align: top;
        }

        .explain-table-compact tbody td {
          padding: 0.5rem 0.7rem;
        }

        .explain-table tbody td:last-child {
          border-right: none;
        }

        .explain-table tbody tr:last-child td {
          border-bottom: none;
        }

        .explain-table td.num,
        .explain-table th.num {
          text-align: right;
          font-variant-numeric: tabular-nums;
        }

        .explain-table td.text,
        .explain-table th.text {
          text-align: left;
        }

        .explain-table-permutation thead th {
          padding: 0.72rem 0.95rem !important;
        }

        .explain-table-permutation tbody td {
          padding: 0.72rem 0.95rem !important;
        }

        .explain-table-permutation {
          margin-bottom: 25px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_html_table(
    df: pd.DataFrame,
    max_height: Optional[int] = None,
    compact: Union[bool, str] = False,
    variant: Optional[str] = None,
) -> None:
    if df is None or df.empty:
        return

    df_to_show = df.copy()

    numeric_cols = []
    for col in df_to_show.columns:
        converted = pd.to_numeric(df_to_show[col], errors="coerce")
        if converted.notna().all():
            numeric_cols.append(col)

    if compact == "extra":
        table_class = "explain-table explain-table-compact explain-table-extra-compact"
    elif compact:
        table_class = "explain-table explain-table-compact"
    else:
        table_class = "explain-table"

    if variant:
        table_class += f" explain-table-{variant}"

    header_html = ""
    for col in df_to_show.columns:
        cls = "num" if col in numeric_cols else "text"
        header_html += f'<th class="{cls}">{html.escape(str(col))}</th>'

    body_rows = []
    for _, row in df_to_show.iterrows():
        cells = []
        for col in df_to_show.columns:
            value = row[col]
            cls = "num" if col in numeric_cols else "text"

            if pd.isna(value):
                display = ""
            elif isinstance(value, float):
                display = f"{value:.4f}".rstrip("0").rstrip(".")
            else:
                display = str(value)

            cells.append(f'<td class="{cls}">{html.escape(display)}</td>')
        body_rows.append(f"<tr>{''.join(cells)}</tr>")

    wrapper_style = ""
    if max_height is not None:
        wrapper_style = f'max-height: {max_height}px; overflow-y: auto;'

    table_html = f"""
    <div class="explain-table-wrap" style="{wrapper_style}">
      <table class="{table_class}">
        <thead>
          <tr>{header_html}</tr>
        </thead>
        <tbody>
          {''.join(body_rows)}
        </tbody>
      </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)