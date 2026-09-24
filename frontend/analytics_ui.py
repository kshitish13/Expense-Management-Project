import streamlit as st
from datetime import datetime,date
import requests
import pandas as pd

API_URL="http://127.0.0.1:8000"

def analytics_tab():
    col1,col2=st.columns(2) # we used to add both dates in one row or else it was up and down and for this only we used with
    with col1:
        start_date=st.date_input("Start Date",datetime(2026,8,1))

    with col2:
        end_date=st.date_input("End Date",datetime(2026,8,5))

    if st.button("Get Analytics"):
        payload={
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response=requests.post(f"{API_URL}/analytics/",json=payload)
        response = response.json()
        #st.write(response)

        data = {
            "Category": list(response.keys()),
            "Total": [response[category]["total"] for category in response],
            "Percentage": [response[category]["percentage"] for category in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        st.title("Expense Breakdown By Category")

        st.bar_chart(data=df_sorted.set_index("Category")['Total'])

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
        st.table(df_sorted)

