from urllib import response

import streamlit as st
from datetime import datetime,date
import requests
import pandas as pd

API_URL="http://127.0.0.1:8000"

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def monthly_summary_tab():
    col1,col2=st.columns(2)
    with col1:
        month=st.selectbox(label="Month", options=months)

    with col2:
        year = st.number_input("Year", min_value=2000, max_value=2100, value=2026, step=1)

    if st.button("Get Summary"):
        response=requests.get(f"{API_URL}/{month}/{year}/summary")
        data=response.json()

        if response.status_code == 200:
            pass
            #st.write(data)
        else:
            st.error("Failed to retrieve Summary")

        data_df=pd.DataFrame(data)

        st.title(f"Expense Summary Of {month}")
        st.bar_chart(data=data_df.set_index("Category")['Total'])

        data_df["Total"] = data_df["Total"].map("{:.2f}".format)
        st.table(data_df)
