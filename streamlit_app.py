import streamlit as st
import streamlit.components.v1 as components
st.title("Jupyterlite in Streamlit")
st.sidebar.header("Configuration")
components.iframe(
    "https://github.com/jeyabalang/upload/blob/master/Layer-dynamic-routes.ipynb",
    height=500
)
