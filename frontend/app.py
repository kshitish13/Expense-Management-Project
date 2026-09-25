import streamlit as st
from analytics_ui import analytics_tab
from add_update_ui import add_update_tab
from monthly_summary import monthly_summary_tab

API_URL="http://127.0.0.1:8000"

st.title("Expense Tracking System")

tab1,tab2,tab3 = st.tabs(["Add/Update","Analytics","Monthly Summary"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_summary_tab()