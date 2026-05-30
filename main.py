import streamlit as st
from app import (halaman_login,
                 tampilkan_header, halaman_dashboard,
                 halaman_input_transaksi, halaman_jurnal_umum,
                 halaman_buku_besar, halaman_neraca_saldo,
                 halaman_jurnal_penyesuaian,halaman_buku_besar_setelah_penyesuaian, halaman_laba_rugi,
                 halaman_neraca, halaman_jurnal_penutup,
                 halaman_ekspor, halaman_kelola_akun)
from akun import load_akun
from transaksi import load_transaksi

st.set_page_config(
    page_title="SICABE",
    page_icon="🌶️",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    halaman_login()
    st.stop()

akun = load_akun()
data = load_transaksi()

tampilkan_header()

with st.sidebar:
    st.header("📌 Menu")
    menu = st.selectbox("", [
        "🏠 Dashboard",
        "➕ Input Transaksi",
        "📋 Jurnal Umum",
        "📚 Buku Besar",
        "⚖️ Neraca Saldo",
        "🔧 Jurnal Penyesuaian",
        "📚 Buku Besar Setelah Penyesuaian",
        "⚖️ Neraca Saldo Disesuaikan",
        "📊 Laporan Laba Rugi",
        "🏦 Neraca",
        "📝 Jurnal Penutup",
        "📁 Ekspor Excel",
        "✏️ Kelola Akun",
    ])
        
if menu == "🏠 Dashboard":
    halaman_dashboard(data, akun)
elif menu == "➕ Input Transaksi":
    halaman_input_transaksi(data, akun)
elif menu == "📋 Jurnal Umum":
    halaman_jurnal_umum(data, akun)
elif menu == "📚 Buku Besar":
    halaman_buku_besar(data, akun)
elif menu == "⚖️ Neraca Saldo":
    halaman_neraca_saldo(data, akun,
        "Neraca Saldo", "Sebelum Penyesuaian")
elif menu == "🔧 Jurnal Penyesuaian":
    halaman_jurnal_penyesuaian(data, akun)
elif menu == "📚 Buku Besar Setelah Penyesuaian":
    halaman_buku_besar_setelah_penyesuaian(data, akun)
elif menu == "⚖️ Neraca Saldo Disesuaikan":
    halaman_neraca_saldo(data, akun,
        "Neraca Saldo Disesuaikan", "Setelah Penyesuaian")
elif menu == "📊 Laporan Laba Rugi":
    halaman_laba_rugi(data, akun)
elif menu == "🏦 Neraca":
    halaman_neraca(data, akun)
elif menu == "📝 Jurnal Penutup":
    halaman_jurnal_penutup(data, akun)
elif menu == "📁 Ekspor Excel":
    halaman_ekspor(data, akun)
elif menu == "✏️ Kelola Akun":
    halaman_kelola_akun(akun)