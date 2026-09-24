import streamlit as st
from analytics_ui import analytics_tab
from add_update_ui import add_update_tab

API_URL="http://127.0.0.1:8000"

st.title("Expense Tracking System")

tab1,tab2 = st.tabs(["Add/Update","Analytics"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()