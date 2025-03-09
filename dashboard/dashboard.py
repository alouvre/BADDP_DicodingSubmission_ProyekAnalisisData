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
        "count_rent": "total",
        "casual": "casual",
        "registered": "registered"
    }, inplace=True)
    return monthly_users_df

# --- Tren Peminjaman Sepeda Per Jam ---
def plot_hourly_trend(df):
    hourly_data = main_df_hour.groupby("hour", as_index=False)["count_rent"].sum()
    rush_hours = [8, 17]  # Morning rush jam 08:00 dan evening rush jam 17:00
    hourly_data["rush"] = hourly_data["hour"].apply(lambda x: "Rush Hour" if x in rush_hours else "Normal")
    fig = px.bar(
        hourly_data,
        x="hour",
        y="count_rent",
        color="rush",  # Memberi warna berbeda untuk jam sibuk
        color_discrete_map={"Rush Hour": "red", "Normal": "#D3D3D3"},
        labels={"hour": "Jam", "count_rent": "Total Penyewa"},
        title="Tren Jumlah Pengguna Layanan Bike-Sharing Per Jam")
    fig.update_layout(
        xaxis=dict(tickmode="linear", dtick=1),
        yaxis_title="Jumlah Pengguna Bike-Sharing",
        xaxis_title="Jam",
        legend_title="Tipe Waktu")
    return fig


# --- Tren Peminjaman Sepeda Tahunan Berdasarkan Tipe Pengguna ---
def plot_yearly_trend(df):
    df_melted = df.melt(id_vars="year", value_vars=["casual", "registered"], 
                        var_name="user_type", value_name="count")
    fig = px.bar(
        df_melted,
        x="year",
        y="count",
        color="user_type",
        barmode="group",
        title="Tren Peminjaman Sepeda: Casual vs Registered",
        labels={"year": "Tahun", "count": "Jumlah Peminjaman"},
        color_discrete_map={"casual": "#D3D3D3", "registered": "red"}
    )
    fig.update_layout(legend_title="Tipe Pengguna")
    return fig

# --- Tren Bulanan ---
def plot_monthly_trend(df):
    fig = px.line(
        df, x='yearmonth', y=['casual', 'registered', 'total'],
        color_discrete_sequence=["#D3D3D3", "orange", "red"],
        markers=True,
        title="Tren Jumlah Pengguna Layanan Bike-Sharing Per Bulan",
        labels={'yearmonth': 'Bulan-Tahun'})
    fig.update_layout(
        xaxis=dict(tickmode="linear", dtick=1),
        yaxis_title="Jumlah Pengguna Bike-Sharing",
        xaxis_title="Bulan-Tahun",
        legend_title="Tipe Pengguna"
    )
    return fig

# --- Tren Musim ---
def plot_seasonly_users(df):
    # --- Mengelompokkan dan Mengurutkan Data ---
    seasonly_users_df_sorted = df.groupby("season", as_index=False)["count_rent"].sum()
    seasonly_users_df_sorted = seasonly_users_df_sorted.sort_values(by="count_rent", ascending=False)

    # Menentukan musim dengan jumlah peminjaman tertinggi
    max_season = seasonly_users_df_sorted.iloc[0]["season"]

    # Membuat warna: merah untuk yang tertinggi, abu-abu untuk lainnya
    seasonly_users_df_sorted["color"] = seasonly_users_df_sorted["season"].apply(
        lambda season: "red" if season == max_season else "#D3D3D3"
    )

    # Membuat plot dengan Plotly
    fig = px.bar(
        seasonly_users_df_sorted,
        x="count_rent",
        y="season",
        orientation="h",
        color="color",
        color_discrete_map="identity",
        text="count_rent",
        title="Jumlah Pengguna Layanan Bike-Sharing Per Musim",
        labels={"count_rent": "Total Pengguna", "season": "Musim"}
    )

    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(
        showlegend=False,
        xaxis_title="Total Pengguna Layanan Bike-Sharing",
        yaxis_title="Musim"
    )
    return fig


# ===== LOAD DATA =====
df_day, df_hour = load_data()


# ===== SIDEBAR =====
with st.sidebar:
    st.image("image/logo.png")
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
    st.metric("Total Pengguna", value=main_df_days['count_rent'].sum())
with col2:
    st.metric("Total Registered", value=main_df_days['registered'].sum())
with col3:
    st.metric("Total Casual", value=main_df_days['casual'].sum())


# ===== CHART =====
col4, col5 = st.columns([2, 1])
col4.plotly_chart(plot_hourly_trend(main_df_hour), use_container_width=True, key="hourly_trend")
col5.plotly_chart(plot_yearly_trend(main_df_days), use_container_width=True, key="yearly_trend")

col6, col7 = st.columns([1.8, 1.2])
col6.plotly_chart(plot_monthly_trend(monthly_users_df), use_container_width=True, key="monthly_trend")
col7.plotly_chart(plot_seasonly_users(main_df_days), use_container_width=True, key="seasonal_trend")


# ===== HIDE STREAMLIT STYLE =====
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
