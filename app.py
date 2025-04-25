import streamlit as st
from datetime import date
import pandas as pd
from db import insert_expense, get_all_expenses  # Make sure db.py is correct

# Page configuration
st.set_page_config(page_title="Expense Tracker", layout="centered")

# 🌑 Custom CSS for Dark Theme
st.markdown("""
    <style>
        body { background-color: #121212; color: #E0E0E0; }
        .title { color: #00C9A7; text-align: center; font-size: 2.2em; margin-bottom: 25px; }
        .stButton>button {
            background-color: #00C9A9;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }
        .stButton>button:hover { background-color: #00B89F; }
        .stTextInput input, .stNumberInput input, .stSelectbox div, .stDateInput input {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }
    </style>
""", unsafe_allow_html=True)

# 🧾 App Title
st.markdown("<div class='title'>💸 Expense Tracker</div>", unsafe_allow_html=True)

# ➕ Expense Input Form
with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Other"])
    with col2:
        expense_date = st.date_input("Date", value=date.today())
        description = st.text_input("Description")

    submitted = st.form_submit_button("Add Expense")

if submitted:
    insert_expense(amount, category, description, expense_date)
    st.success("✅ Expense added successfully!")

# 📊 Show Expense Table
st.subheader("📅 Expense History")
expenses = get_all_expenses()

if expenses:
    df = pd.DataFrame(expenses, columns=["ID", "Amount", "Category", "Description", "Date"])
    st.dataframe(df.drop("ID", axis=1), use_container_width=True)

    # 🔢 Convert date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # 📊 Chart 1: Spending by Category
    st.subheader("📊 Spending by Category")
    category_totals = df.groupby("Category")["Amount"].sum()
    st.plotly_chart({
        "data": [{
            "labels": category_totals.index,
            "values": category_totals.values,
            "type": "pie"
        }],
        "layout": {"margin": {"t": 0, "b": 0}}
    })

    # 📈 Chart 2: Expenses Over Time
    st.subheader("📈 Daily Expenses")
    daily_totals = df.groupby(df["Date"].dt.date)["Amount"].sum()
    st.bar_chart(daily_totals)
else:
    st.info("No expenses recorded yet. Add some to get started!")

