import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Visualisasi Kasus H1N1 2009", page_icon="🦠", layout="wide")

# Muat data dari CSV
data_path = 'dataset.csv'
data = pd.read_csv(data_path)

# Bersihkan data
data.columns = data.columns.str.strip()
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.dropna(subset=['Date'])

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Kasus Tertinggi 2009", "Kasus Terendah 2009", "Kasus dari Waktu ke Waktu 2009", "Kasus Baru Harian", "Kasus Fatal Harian", "Filter Data"])

# Fungsi untuk menampilkan kasus tertinggi di 2009
def show_highest_2009():
    st.header("10 Negara dengan Kasus H1N1 Tertinggi pada 2009")
    data_2009 = data[data['Date'].dt.year == 2009]
    top_10_countries_2009 = data_2009.groupby('Country')['Cumulative no. of cases'].max().nlargest(10).reset_index()

    fig = px.bar(top_10_countries_2009, x='Country', y='Cumulative no. of cases', title="10 Negara dengan Kasus H1N1 Tertinggi pada 2009", color='Country')
    st.plotly_chart(fig)
    st.write("Tabel berikut menunjukkan 10 negara dengan jumlah kasus H1N1 tertinggi pada 2009.")
    st.table(top_10_countries_2009)

    # Tambahkan diagram lingkaran
    pie_chart = px.pie(top_10_countries_2009, names='Country', values='Cumulative no. of cases', title='Persentase Kasus di 10 Negara Teratas pada 2009')
    st.plotly_chart(pie_chart)

# Fungsi untuk menampilkan kasus terendah di 2009
def show_lowest_2009():
    st.header("10 Negara dengan Kasus H1N1 Terendah pada 2009")
    data_2009 = data[data['Date'].dt.year == 2009]
    bottom_10_countries_2009 = data_2009.groupby('Country')['Cumulative no. of cases'].max().nsmallest(10).reset_index()

    fig = px.bar(bottom_10_countries_2009, x='Country', y='Cumulative no. of cases', title="10 Negara dengan Kasus H1N1 Terendah pada 2009", color='Country')
    st.plotly_chart(fig)
    st.write("Tabel berikut menunjukkan 10 negara dengan jumlah kasus H1N1 terendah pada 2009.")
    st.table(bottom_10_countries_2009)

    # Tambahkan diagram lingkaran
    pie_chart = px.pie(bottom_10_countries_2009, names='Country', values='Cumulative no. of cases', title='Persentase Kasus di 10 Negara Terendah pada 2009')
    st.plotly_chart(pie_chart)

# Fungsi untuk menampilkan kasus dari waktu ke waktu pada 2009
def show_cases_over_time_2009():
    st.header("Kasus H1N1 dari Waktu ke Waktu pada 2009")
    data_2009 = data[data['Date'].dt.year == 2009]
    cases_over_time = data_2009.groupby('Date')['Cumulative no. of cases'].sum().reset_index()

    fig = px.line(cases_over_time, x='Date', y='Cumulative no. of cases', title="Kasus H1N1 dari Waktu ke Waktu pada 2009")
    st.plotly_chart(fig)
    st.write("Tabel berikut menunjukkan jumlah kumulatif harian kasus H1N1 pada 2009.")
    st.table(cases_over_time)

# Fungsi untuk menampilkan kasus baru harian pada 2009
def show_daily_new_cases_2009():
    st.header("Kasus Baru Harian H1N1 pada 2009")
    data_2009 = data[data['Date'].dt.year == 2009]
    data_2009['New Cases'] = data_2009.groupby('Country')['Cumulative no. of cases'].diff().fillna(0)
    daily_new_cases = data_2009.groupby('Date')['New Cases'].sum().reset_index()

    fig = px.line(daily_new_cases, x='Date', y='New Cases', title="Kasus Baru Harian H1N1 pada 2009")
    st.plotly_chart(fig)
    st.write("Tabel berikut menunjukkan jumlah kasus baru harian H1N1 pada 2009.")
    st.table(daily_new_cases)

# Fungsi untuk menampilkan kasus fatal harian pada 2009
def show_daily_fatal_cases_2009():
    st.header("Kasus Fatal Harian H1N1 pada 2009")
    data_2009 = data[data['Date'].dt.year == 2009]
    data_2009['New Fatal Cases'] = data_2009.groupby('Country')['Cumulative no. of deaths'].diff().fillna(0)
    daily_fatal_cases = data_2009.groupby('Date')['New Fatal Cases'].sum().reset_index()

    fig = px.line(daily_fatal_cases, x='Date', y='New Fatal Cases', title="Kasus Fatal Harian H1N1 pada 2009")
    st.plotly_chart(fig)
    st.write("Tabel berikut menunjukkan jumlah kasus fatal baru harian H1N1 pada 2009.")
    st.table(daily_fatal_cases)

# Fungsi untuk memfilter data
def filter_data():
    st.sidebar.header("Filter Data")
    selected_year = st.sidebar.selectbox("Pilih Tahun", options=[2009], index=0)
    selected_country = st.sidebar.selectbox("Pilih Negara", options=data['Country'].unique())

    # Filter data berdasarkan pilihan
    filtered_data_year = data[data['Date'].dt.year == selected_year]
    filtered_data_country = filtered_data_year[filtered_data_year['Country'] == selected_country]

    # Tampilkan data yang difilter berdasarkan pilihan
    st.subheader(f"Kasus H1N1 di {selected_country} pada tahun {selected_year}")
    cases_country_year = filtered_data_country.groupby('Date')['Cumulative no. of cases'].sum().reset_index()

    fig = px.line(cases_country_year, x='Date', y='Cumulative no. of cases', title=f"Kasus H1N1 di {selected_country} pada tahun {selected_year}")
    st.plotly_chart(fig)
    st.write(f"Tabel berikut menunjukkan jumlah kumulatif harian kasus H1N1 di {selected_country} pada tahun {selected_year}.")
    st.table(cases_country_year)

# Tampilkan halaman yang dipilih
if page == "Kasus Tertinggi 2009":
    show_highest_2009()
elif page == "Kasus Terendah 2009":
    show_lowest_2009()
elif page == "Kasus dari Waktu ke Waktu 2009":
    show_cases_over_time_2009()
elif page == "Kasus Baru Harian":
    show_daily_new_cases_2009()
elif page == "Kasus Fatal Harian":
    show_daily_fatal_cases_2009()
elif page == "Filter Data":
    filter_data()
