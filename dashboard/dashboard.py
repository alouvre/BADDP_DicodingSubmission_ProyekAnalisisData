import streamlit as st
import pandas as pd

df_day = pd.read_csv("dashboard/day_cleaned.csv")
df_hour = pd.read_csv("dashboard/hour_cleaned.csv")

st.title("Bike Sharing Data Analysis")
st.caption("By Alifia Mustika Sari")


min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://th.bing.com/th/id/R.2e28d8f8496fc0674fa0a7d600598298?rik=Ynk8i9VuwEKH7w&riu=http%3a%2f%2fmikerazar.com%2fchart-it%2fwp-content%2fuploads%2f2019%2f09%2fCapitalBikeshare_Logo.jpg&ehk=AVnjVCVP9ZBWbv%2fc71LBEmFJPkz3MCFn2S1M2VPgy9o%3d&risl=&pid=ImgRaw&r=0")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Sidebar filters
st.sidebar.header("Filters")
season_filter = st.sidebar.multiselect(
    "Select Season(s):", 
    options=df_day['season'].unique(), 
    default=df_day['season'].unique()
)
hour_filter = st.sidebar.slider(
    "Select Hour Range:", 
    min_value=int(df_hour['hr'].min()), 
    max_value=int(df_hour['hr'].max()), 
    value=(0, 23)
)