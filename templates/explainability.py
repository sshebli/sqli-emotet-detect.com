from typing import Optional

import pandas as pd
import streamlit as st

from templates.explainability_sections import (
    render_bordered_section,
    render_bottom_row,
    render_cross_validation_section,
    render_generalisation_section,
    render_importance_side_by_side,
    render_intro_inline,
    render_model_comparisons_section,
    render_page_title,
)
from templates.explainability_tables import inject_explainability_table_css


def render_explainability_tab(
    importance: Optional[pd.DataFrame],
    unified_importance: Optional[pd.DataFrame],
    pretty_feature_group_fn,
) -> None:
    render_page_title("Explainability")
    render_intro_inline()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    render_importance_side_by_side(unified_importance, pretty_feature_group_fn)

    render_bordered_section(
        render_cross_validation_section,
        key="explain_cv_box",
    )

    render_bordered_section(
        render_model_comparisons_section,
        key="explain_model_comp_box",
    )

    render_bordered_section(
        render_generalisation_section,
        key="explain_generalisation_box",
    )

    render_bottom_row()

    inject_explainability_table_css()