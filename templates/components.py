import streamlit as st


@st.cache_data
def _read_css(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_css(path: str = "assets/styles.css") -> None:
    """
    Load external CSS into Streamlit.

    Parameters
    ----------
    path : str
        Path to the CSS file.
    """
    try:
        css = _read_css(path)
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )

    except FileNotFoundError:
        st.warning(f"CSS file not found: {path}")