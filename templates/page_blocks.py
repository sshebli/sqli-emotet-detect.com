import streamlit as st
from textwrap import dedent
from typing import Callable


HomePageFn = Callable[[str], None]
VoidFn = Callable[[], None]


def markdown_block(html: str) -> None:
    st.markdown(html, unsafe_allow_html=True)


def render_page_title(title: str) -> None:
    markdown_block(
        f"""
        <div class="page-title-wrap">
            <h1 class="page-title">{title}</h1>
        </div>
        """
    )


def render_section_heading(title: str) -> None:
    markdown_block(
        f"""
        <div class="section-heading-wrap">
            <h2 class="section-heading">{title}</h2>
        </div>
        """
    )


def render_info_box_title(title: str) -> None:
    markdown_block(f'<h3 class="info-box-title">{title}</h3>')


def render_back_home_button(go_home_fn: VoidFn) -> None:
    with st.container(key="back_home_wrap"):
        st.button("Back to Home", on_click=go_home_fn)


def render_bullets(markdown_text: str) -> None:
    markdown_block(dedent(markdown_text))


def render_paragraph(text: str, style: str = "") -> None:
    style_attr = f' style="{style}"' if style else ""
    markdown_block(f"<p{style_attr}>{text}</p>")