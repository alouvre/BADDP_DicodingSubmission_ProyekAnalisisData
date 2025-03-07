import streamlit as st
import pandas as pd


# --- Fungsi untuk Membuat DataFrame Penyewaan Harian ---
def create_daily_casual_rent_df(df):
    """
    Mengelompokkan data berdasarkan tanggal
    untuk menghitung total penyewaan casual.
    """
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df


def create_daily_registered_rent_df(df):
    """
    Mengelompokkan data berdasarkan tanggal
    untuk menghitung total penyewaan registered.
    """
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df


# --- Membaca Data ---
df_day = pd.read_csv("dashboard/day_cleaned.csv")
df_hour = pd.read_csv("dashboard/hour_cleaned.csv")


# --- Membangun Dashboard ---

# Membuat Judul
st.title("Bike Share Dashboard")
# Nama Author
st.caption("By Alifia Mustika Sari")

# --- Sidebar: Filter Rentang Waktu ---
# Pastikan kolom tanggal pada file CSV menggunakan nama 'date'
min_date = df_day["date"].min()
max_date = df_day["date"].max()

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

# --- Filter Data Utama Berdasarkan Rentang Waktu ---
main_df_days = df_day[(df_day["date"] >= str(start_date)) &
                      (df_day["date"] <= str(end_date))]
main_df_hour = df_hour[(df_hour["date"] >= str(start_date)) &
                       (df_hour["date"] <= str(end_date))]


# --- Konten Utama: Informasi Penyewaan Harian ---
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)
with col1:
    daily_rent_total = main_df_days['count_rental'].sum()
    st.metric('Total User', value=daily_rent_total)
with col2:
    daily_rent_registered = main_df_days['registered'].sum()
    st.metric('Total Registered', value=daily_rent_registered)
with col3:
    daily_rent_casual = main_df_days['casual'].sum()
    st.metric('Total Casual', value=daily_rent_casual)