import streamlit as st
from app import (TEMA, apply_tema, halaman_login,
                 tampilkan_header, halaman_dashboard,
                 halaman_input_transaksi, halaman_jurnal_umum,
                 halaman_buku_besar, halaman_neraca_saldo,
                 halaman_jurnal_penyesuaian, halaman_laba_rugi,
                 halaman_neraca, halaman_jurnal_penutup,
                 halaman_ekspor, halaman_kelola_akun,
                 halaman_pengaturan)
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
if "tema" not in st.session_state:
    st.session_state.tema = "Pink"

t = TEMA[st.session_state.tema]
apply_tema(t)

if not st.session_state.logged_in:
    halaman_login()
    st.stop()

akun = load_akun()
data = load_transaksi()

tampilkan_header(t)

with st.sidebar:
    st.markdown(
        f"<h3 style='color:{t['accent']}'>📌 Menu</h3>",
        unsafe_allow_html=True)
    menu = st.selectbox("", [
        "🏠 Dashboard",
        "➕ Input Transaksi",
        "📋 Jurnal Umum",
        "📚 Buku Besar",
        "⚖️ Neraca Saldo",
        "🔧 Jurnal Penyesuaian",
        "⚖️ Neraca Saldo Disesuaikan",
        "📊 Laporan Laba Rugi",
        "🏦 Neraca",
        "📝 Jurnal Penutup",
        "📁 Ekspor Excel",
        "✏️ Kelola Akun",
        "⚙️ Pengaturan Tema"
    ])

if menu == "🏠 Dashboard":
    halaman_dashboard(data, akun, t)
elif menu == "➕ Input Transaksi":
    halaman_input_transaksi(data, akun, t)
elif menu == "📋 Jurnal Umum":
    halaman_jurnal_umum(data, akun, t)
elif menu == "📚 Buku Besar":
    halaman_buku_besar(data, akun, t)
elif menu == "⚖️ Neraca Saldo":
    halaman_neraca_saldo(data, akun, t,
        "Neraca Saldo", "Sebelum Penyesuaian")
elif menu == "🔧 Jurnal Penyesuaian":
    halaman_jurnal_penyesuaian(data, akun, t)
elif menu == "⚖️ Neraca Saldo Disesuaikan":
    halaman_neraca_saldo(data, akun, t,
        "Neraca Saldo Disesuaikan", "Setelah Penyesuaian")
elif menu == "📊 Laporan Laba Rugi":
    halaman_laba_rugi(data, akun, t)
elif menu == "🏦 Neraca":
    halaman_neraca(data, akun, t)
elif menu == "📝 Jurnal Penutup":
    halaman_jurnal_penutup(data, akun, t)
elif menu == "📁 Ekspor Excel":
    halaman_ekspor(data, akun, t)
elif menu == "✏️ Kelola Akun":
    halaman_kelola_akun(akun, t)
elif menu == "⚙️ Pengaturan Tema":
    halaman_pengaturan(t)