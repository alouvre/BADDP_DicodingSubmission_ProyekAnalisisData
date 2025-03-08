import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Bike Share Dashboard", layout="wide")

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

## Membuat Judul Dashboard
st.title("Bike Share Dashboard")
st.caption("By Alifia Mustika Sari")

# --- Sidebar: Filter Rentang Waktu ---
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


# --- Konten Utama 1: Informasi Penyewaan Harian ---
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total User", value=main_df_days['count_rent'].sum())
with col2:
    st.metric("Total Registered", value=main_df_days['registered'].sum())
with col3:
    st.metric("Total Casual", value=main_df_days['casual'].sum())


# --- Konten Utama 2: Visualisasi Tren Pengguna Sepeda ---
col4, col5 = st.columns([1, 1])

## Grafik Tren Peminjaman Sepeda Per Jam
main_df_hour['period'] = main_df_hour['hour'].apply(lambda x: 'AM' if x < 12 else 'PM')
with col4:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=main_df_hour, x='hour', y='count_rent', hue='period', palette={"AM": "salmon", "PM": "red"}, alpha=0.9, ax=ax)
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Tren Peminjaman Sepeda Per Jam")
    plt.legend(title="Waktu")
    st.pyplot(fig)

## Grafik Tren Peminjaman Sepeda Tahunan Berdasarkan Tipe Pengguna
df_yearly_users = main_df_days.groupby('year', as_index=False)[['casual', 'registered']].sum()
df_melted = df_yearly_users.melt(id_vars="year", var_name="user_type", value_name="count")

with col5:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df_melted, x="year", y="count", hue="user_type", palette={"casual": "salmon", "registered": "red"}, alpha=0.9, ax=ax)
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Tren Peminjaman Sepeda: Casual vs Registered")
    plt.legend(title="Tipe Pengguna")
    st.pyplot(fig)
