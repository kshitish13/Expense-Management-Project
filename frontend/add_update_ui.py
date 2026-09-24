import streamlit as st
from datetime import datetime,date
import requests

API_URL="http://127.0.0.1:8000"


def add_update_tab():
    selected_dt = st.date_input("Select Date", date.today())
    st.write("Selected date:", selected_dt)
    response = requests.get(f"{API_URL}/expenses/{selected_dt}")

    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["None", "Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0  # these are the default values
                category = "None"
                notes = " "
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label="Amount", step=1.0, min_value=0.0, value=amount,
                                               key=f"amount_{selected_dt}_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"category_{selected_dt}_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{selected_dt}_{i}",
                                            label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                "category": category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button()
        if submit_button:

            invalid = any(
                exp["amount"] > 0 and exp["category"] == "None"
                for exp in expenses
            )

            if invalid:
                st.error("Please select a category for all expenses.")
            else:
                filtered_expenses = [
                    exp for exp in expenses
                    if exp["amount"] > 0 and exp["category"] != "None"
                ]

                response = requests.post(
                    f"{API_URL}/expenses/{selected_dt}",
                    json=filtered_expenses
                )

                if response.status_code == 200:
                    st.success("Expenses saved successfully!")
                else:
                    st.error("Failed to save expenses.")