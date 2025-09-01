import streamlit as st

def load_css(file_name: str):
    """Load custom CSS file into a Streamlit app."""
    with open(file_name) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
