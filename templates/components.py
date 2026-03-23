import streamlit as st


def load_css(path: str = "assets/styles.css") -> None:
    """
    Load external CSS into Streamlit.

    Parameters
    ----------
    path : str
        Path to the CSS file.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            css = f.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )

    except FileNotFoundError:
        st.warning(f"CSS file not found: {path}")