import streamlit as st

from e2e_test import e2e_test_page
from nlu_test import nlu_test_page
from agent_interaction import agent_interaction_page

st.set_page_config(page_title="TEST PLAT for Thought Agent", layout="wide")

pages = {
    "NLU Test": nlu_test_page,
    "E2E Test": e2e_test_page,
    "Chat with Agent": agent_interaction_page,
    "Prompt Debug": agent_interaction_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

pages[selection]()