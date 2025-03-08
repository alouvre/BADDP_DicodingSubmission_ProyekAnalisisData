import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Capital Bikeshare: Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# --- Membaca Data ---
df_day = pd.read_csv("dashboard/day_cleaned.csv")
df_hour = pd.read_csv("dashboard/hour_cleaned.csv")

# # --- Fungsi untuk Membuat DataFrame Penyewaan Harian ---
# def create_daily_casual_rent_df(df):
#     """
#     Mengelompokkan data berdasarkan tanggal
#     untuk menghitung total penyewaan casual.
#     """
#     daily_casual_rent_df = df.groupby(by='dateday').agg({
#         'casual': 'sum'
#     }).reset_index()
#     return daily_casual_rent_df

# def create_daily_registered_rent_df(df):
#     """
#     Mengelompokkan data berdasarkan tanggal
#     untuk menghitung total penyewaan registered.
#     """
#     daily_registered_rent_df = df.groupby(by='dateday').agg({
#         'registered': 'sum'
#     }).reset_index()
#     return daily_registered_rent_df


# --- Membangun Dashboard ---

# --- Sidebar: Filter Rentang Waktu ---
min_date = df_day["date"].min()
max_date = df_day["date"].max()

# ----- SIDEBAR -----

with st.sidebar:
    st.image(r"image\logo.png")
    st.sidebar.header("Filter:")
    # Mengambil start_date & end_date dari date_input
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

# --- Filter Data Utama Berdasarkan Rentang Waktu ---
main_df_days = df_day[(df_day["date"] >= str(start_date)) &
                      (df_day["date"] <= str(end_date))]
main_df_hour = df_hour[(df_hour["date"] >= str(start_date)) &
                       (df_hour["date"] <= str(end_date))]


# ----- MAINPAGE -----

st.title("Capital Bikeshare: Dashboard")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns([1, 1])

# Informasi Penyewaan Harian
with col1:
    st.metric("Total User", value=main_df_days['count_rent'].sum())
with col2:
    st.metric("Total Registered", value=main_df_days['registered'].sum())
with col3:
    st.metric("Total Casual", value=main_df_days['casual'].sum())


# Chart Tren Peminjaman Sepeda Per Jam
main_df_hour['period'] = main_df_hour['hour'].apply(lambda x: 'AM' if x < 12 else 'PM')
with col4:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=main_df_hour, x='hour', y='count_rent', hue='period',
                palette={"AM": "salmon", "PM": "red"}, alpha=0.9, ax=ax)
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Tren Peminjaman Sepeda Per Jam")
    plt.legend(title="Waktu")
    st.pyplot(fig)

# Grafik Tren Peminjaman Sepeda Tahunan Berdasarkan Tipe Pengguna
df_yearly_users = main_df_days.groupby('year', as_index=False)[['casual',
                                                                'registered']].sum()
df_melted = df_yearly_users.melt(id_vars="year", var_name="user_type",
                                 value_name="count")

with col5:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df_melted, x="year", y="count", hue="user_type",
                palette={"casual": "salmon", "registered": "red"},
                alpha=0.9, ax=ax)
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Tren Peminjaman Sepeda: Casual vs Registered")
    plt.legend(title="Tipe Pengguna")
    st.pyplot(fig)

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
