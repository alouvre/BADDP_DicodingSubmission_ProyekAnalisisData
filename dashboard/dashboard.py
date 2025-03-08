import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Capital Bikeshare: Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# --- Fungsi untuk Membaca Data ---
def load_data():
    df_day = pd.read_csv("dashboard/day_cleaned.csv")
    df_hour = pd.read_csv("dashboard/hour_cleaned.csv")
    df_day["date"] = pd.to_datetime(df_day["date"])
    df_hour["date"] = pd.to_datetime(df_hour["date"])
    return df_day, df_hour

def create_monthly_users_df(df):
    df["date"] = pd.to_datetime(df["date"])
    monthly_users_df = df.resample(rule='M', on='date').agg({
        "casual": "sum",
        "registered": "sum",
        "count_rent": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
        "count_rent": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

# --- Tren Peminjaman Sepeda Per Jam ---
def plot_hourly_trend(df):
    hourly_data = df.groupby("hour", as_index=False)["count_rent"].sum()
    max_hour = hourly_data.loc[hourly_data["count_rent"].idxmax(), "hour"]
    hourly_data["color"] = hourly_data["hour"].apply(lambda x: 'red' if x == max_hour else '#D3D3D3')
    fig = px.bar(
        hourly_data, x='hour', y='count_rent', color='color', 
        color_discrete_map='identity', barmode='group',
        title="Jam dengan Jumlah Penyewaan Sepeda Tertinggi")
    fig.update_layout(xaxis_title="Jam", yaxis_title="Jumlah Penyewa", 
                      showlegend=True)
    return fig

# --- Tren Peminjaman Sepeda Tahunan Berdasarkan Tipe Pengguna ---
def plot_yearly_trend(df):
    yearly_data = df.groupby("year", as_index=False)[["casual", "registered"]].sum()
    df_melted = yearly_data.melt(id_vars="year", var_name="user_type", value_name="count")
    fig = px.bar(
        df_melted, x="year", y="count", color="user_type", barmode='group',
        color_discrete_map={"casual": "#D3D3D3", "registered": "red"},
        title="Pengguna Casual vs Registered",
        labels={'year': 'Tahun', 'count': 'Jumlah Peminjaman', 'user_type': 'Tipe Pengguna'})
    fig.update_layout(xaxis_title="Tahun", yaxis_title="Jumlah Penyewa", 
                      showlegend=True)
    return fig

# --- Tren Bulanan ---
def plot_monthly_trend(df):
    fig = px.line(df, x='yearmonth', y=['casual_rides', 'registered_rides', 'total_rides'],
                  color_discrete_sequence=["#D3D3D3", "orange", "red"],
                  markers=True,
                  title="Monthly Count of Bikeshare Rides",
                  labels={'yearmonth': 'Tahun-Bulan'})                  
    fig.update_layout(yaxis_title='Jumlah Penyewa')
    return fig


# ===== LOAD DATA =====
df_day, df_hour = load_data()


# ===== SIDEBAR =====
with st.sidebar:
    st.image(r"image\logo.png")
    st.sidebar.header("Filter:")
    min_date, max_date = df_day["date"].min(), df_day["date"].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    st.sidebar.header("Visit my profile!")
    st.sidebar.subheader("Alifia Mustika Sari")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/alifiamustika/)")
    with col2:
        st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/alouvre)")

# --- Filter Data Berdasarkan Rentang Waktu ---
main_df_days = df_day[(df_day["date"] >= str(start_date)) &
                      (df_day["date"] <= str(end_date))]
main_df_hour = df_hour[(df_hour["date"] >= str(start_date)) &
                       (df_hour["date"] <= str(end_date))]
monthly_users_df = create_monthly_users_df(main_df_days)


# ===== MAINPAGE =====
st.title("Capital Bikeshare: Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total User", value=main_df_days['count_rent'].sum())
with col2:
    st.metric("Total Registered", value=main_df_days['registered'].sum())
with col3:
    st.metric("Total Casual", value=main_df_days['casual'].sum())


# ===== CHART =====
col4, col5 = st.columns([2, 1])
col4.plotly_chart(plot_hourly_trend(main_df_hour), use_container_width=True)
col5.plotly_chart(plot_yearly_trend(main_df_days), use_container_width=True)
st.plotly_chart(plot_monthly_trend(monthly_users_df), use_container_width=True)


# ===== HIDE STREAMLIT STYLE =====
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
