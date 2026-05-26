import streamlit as st
import pandas as pd
import json
import os
import io
from PIL import Image
from akun import load_akun, simpan_akun, get_nama
from transaksi import (load_transaksi, simpan_transaksi,
                       load_penyesuaian, simpan_penyesuaian,
                       hitung_saldo)

# ========================
# TEMA
# ========================
TEMA = {
    "Pink": {
        "bg": "#ffe0e0", "bg2": "#fdb1b1",
        "accent": "#194bff", "text": "#100f0f", "card": "#fff23a"
    },
    "Kuning": {
        "bg": "#fffcbe", "bg2": "#f1f18f",
        "accent": "#ff0000", "text": "#151510", "card": "#006aff"
    },
    "Biru": {
        "bg": "#e0e0ff", "bg2": "#93a9f0",
        "accent": "#ff0303", "text": "#101012", "card": "#ffee00"
    },
    "Terang": {
        "bg": "#f0f0f0", "bg2": "#ffffff",
        "accent": "#cc0000", "text": "#111111", "card": "#e0e0e0"
    },
}

def apply_tema(t):
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, {t['bg']} 0%, {t['bg2']} 50%, {t['bg']} 100%);
        }}
        section[data-testid="stSidebar"] {{
            background-color: {t['bg2']};
        }}
        h1, h2, h3, h4 {{ color: {t['accent']} !important; }}
        .stButton>button {{
            background-color: {t['accent']} !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
        }}
        div[data-testid="metric-container"] {{
            background-color: {t['card']};
            border: 1px solid {t['accent']};
            border-radius: 10px;
            padding: 10px;
        }}
        .stDataFrame {{
            border: 1px solid {t['accent']};
            border-radius: 8px;
        }}
    </style>
    """, unsafe_allow_html=True)

# ========================
# USERS
# ========================
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except:
            return {}
    return {}

def simpan_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ========================
# LOGIN
# ========================
def halaman_login():
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #ffe0e0 0%, #fdb1b1 100%); }
        .stButton>button {
            background-color: #194bff !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo di tengah atas
        try:
            logo = Image.open("logoo.png")
            st.image(logo, width=180, use_container_width=False)
        except:
            st.markdown("<h1 style='text-align:center;'>🌶️</h1>",
                unsafe_allow_html=True)

        st.markdown("""
        <h1 style='text-align:center; color:#ff4444;
        font-family:Georgia, serif; font-size:42px;'>SICABE</h1>
        <p style='text-align:center; color:#ffcccc; font-size:14px;'>
        Sistem Informasi Manajemen Cabai</p>
        """, unsafe_allow_html=True)

        st.markdown("---")

        tab1, tab2 = st.tabs(["🔑 Login", "📝 Daftar Akun Baru"])

        with tab1:
            username = st.text_input("👤 Username", key="login_user")
            password = st.text_input("🔒 Password",
                type="password", key="login_pass")
            if st.button("🔑 Login", use_container_width=True, key="btn_login"):
                if not username or not password:
                    st.error("❌ Username dan password harus diisi!")
                else:
                    users = load_users()
                    if username not in users:
                        st.error("❌ Username tidak ditemukan!")
                    elif users[username] != password:
                        st.error("❌ Password salah! Coba lagi.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"✅ Selamat datang, {username}!")
                        st.rerun()

        with tab2:
            st.markdown("##### Buat Akun Baru")
            new_user = st.text_input("👤 Username Baru", key="reg_user")
            new_pass = st.text_input("🔒 Password Baru",
                type="password", key="reg_pass")
            new_pass2 = st.text_input("🔒 Konfirmasi Password",
                type="password", key="reg_pass2")
            if st.button("📝 Daftar Sekarang",
                use_container_width=True, key="btn_daftar"):
                if not new_user or not new_pass:
                    st.error("❌ Semua field harus diisi!")
                else:
                    users = load_users()
                    if new_user in users:
                        st.error("❌ Username sudah dipakai!")
                    elif new_pass != new_pass2:
                        st.error("❌ Konfirmasi password tidak cocok!")
                    elif len(new_pass) < 6:
                        st.error("❌ Password minimal 6 karakter!")
                    else:
                        users[new_user] = new_pass
                        simpan_users(users)
                        st.success(f"✅ Akun '{new_user}' berhasil dibuat! Silakan login.")

# ========================
# HEADER
# ========================
def tampilkan_header(t):
    col1, col2, col3 = st.columns([2, 6, 1])
    with col1:
        try:
            logo = Image.open("logoo.png")
            st.image(logo, width=130)
        except:
            st.markdown("🌶️")
    with col2:
        st.markdown(f"""
        <h1 style='color:{t["accent"]}; font-size:48px;
        font-family:Georgia, serif; margin:0; padding-top:10px;'>SICABE</h1>
        <p style='color:{t["text"]}; margin:0; font-size:14px;'>
        Sistem Informasi Akuntansi Cabai Setan Lombo</p>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='color:{t['text']}; text-align:right; margin-top:15px;'>👤 {st.session_state.username}</p>",
            unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    st.divider()

# ========================
# DASHBOARD
# ========================
def halaman_dashboard(data, akun, t):
    st.header("🏠 Dashboard")
    saldo = hitung_saldo(data, akun)
    total_p = sum(saldo[k]["kredit"] - saldo[k]["debet"]
        for k in saldo if k.startswith("4-"))
    total_b = sum(saldo[k]["debet"] - saldo[k]["kredit"]
        for k in saldo if k.startswith("5-"))
    laba = total_p - total_b

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
    with col2:
        st.metric("💰 Total Pendapatan", f"Rp {total_p:,.0f}")
    with col3:
        st.metric("💸 Total Beban", f"Rp {total_b:,.0f}")
    with col4:
        st.metric(
            "📈 Laba Bersih" if laba >= 0 else "📉 Rugi Bersih",
            f"Rp {abs(laba):,.0f}")
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"📊 Total transaksi: {len(data)} | Periode: Januari – April 2026")

    st.markdown("---")
    st.subheader("📌 Panduan Pencatatan Transaksi")
    st.markdown(f"""
    <div style='background:{t["card"]}; border:1px solid {t["accent"]};
    border-radius:10px; padding:20px; line-height:2;'>
    <p style='color:{t["text"]}'><b>Panduan singkat penggunaan akun untuk kebun cabai:</b></p>
    <p style='color:{t["text"]}'>🌱 <b>Beli bibit/benih</b><br>
    → Debet: <i>Persediaan Bibit</i> | Kredit: <i>Kas</i></p>
    <p style='color:{t["text"]}'>🌿 <b>Beli pupuk</b><br>
    → Debet: <i>Persediaan Pupuk</i> | Kredit: <i>Kas</i></p>
    <p style='color:{t["text"]}'>🐛 <b>Beli pestisida/obat hama</b><br>
    → Debet: <i>Beban Pestisida</i> | Kredit: <i>Kas</i></p>
    <p style='color:{t["text"]}'>👷 <b>Bayar upah pekerja</b><br>
    → Debet: <i>Beban Tenaga Kerja</i> | Kredit: <i>Kas</i></p>
    <p style='color:{t["text"]}'>🌶️ <b>Terima uang hasil jual cabai</b><br>
    → Debet: <i>Kas</i> | Kredit: <i>Pendapatan Penjualan Cabai</i></p>
    <p style='color:{t["text"]}'>💧 <b>Pakai pupuk dari stok yang sudah dibeli</b><br>
    → Debet: <i>Beban Pupuk</i> | Kredit: <i>Persediaan Pupuk</i></p>
    <p style='color:{t["text"]}'>🏦 <b>Setor modal awal usaha</b><br>
    → Debet: <i>Kas</i> | Kredit: <i>Modal Pemilik</i></p>
    <p style='color:{t["text"]}'>💸 <b>Bayar bagi hasil ke pemilik lahan</b><br>
    → Debet: <i>Beban Bagi Hasil</i> | Kredit: <i>Kas</i></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📝 Catatan")
    catatan_lama = ""
    try:
        with open("catatan.txt", "r") as f:
            catatan_lama = f.read()
    except:
        pass
    catatan = st.text_area("Tulis catatan di sini...",
        value=catatan_lama, height=150,
        placeholder="Contoh: Musim tanam dimulai Januari 2026...")
    if st.button("💾 Simpan Catatan"):
        with open("catatan.txt", "w") as f:
            f.write(catatan)
        st.success("✅ Catatan tersimpan!")

# ========================
# INPUT TRANSAKSI
# ========================
def halaman_input_transaksi(data, akun, t):
    st.header("➕ Input Transaksi")
    if "jml_d" not in st.session_state:
        st.session_state.jml_d = 1
    if "jml_k" not in st.session_state:
        st.session_state.jml_k = 1

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("➕ Tambah Akun Debet"):
            st.session_state.jml_d += 1
            st.rerun()
    with col2:
        if st.button("➕ Tambah Akun Kredit"):
            st.session_state.jml_k += 1
            st.rerun()
    with col3:
        if st.button("🔄 Reset Form"):
            st.session_state.jml_d = 1
            st.session_state.jml_k = 1
            st.rerun()

    with st.form("form_transaksi"):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("📅 Tanggal")
        with col2:
            keterangan = st.text_input("📝 Keterangan Transaksi")

        col_d, col_k = st.columns(2)
        debets = []
        kredits = []

        with col_d:
            st.subheader("📤 Akun Debet")
            for i in range(st.session_state.jml_d):
                kode_d = st.selectbox(
                    f"Akun Debet {i+1}",
                    options=list(akun.keys()),
                    format_func=lambda x: f"{x} - {get_nama(x, akun)}",
                    key=f"d_{i}")
                nom_d = st.number_input(
                    f"Nominal Debet {i+1}",
                    min_value=0, step=1000, key=f"nd_{i}")
                debets.append({"kode": kode_d, "nominal": nom_d})

        with col_k:
            st.subheader("📥 Akun Kredit")
            for i in range(st.session_state.jml_k):
                kode_k = st.selectbox(
                    f"Akun Kredit {i+1}",
                    options=list(akun.keys()),
                    format_func=lambda x: f"{x} - {get_nama(x, akun)}",
                    key=f"k_{i}")
                nom_k = st.number_input(
                    f"Nominal Kredit {i+1}",
                    min_value=0, step=1000, key=f"nk_{i}")
                kredits.append({"kode": kode_k, "nominal": nom_k})

        total_d = sum(d["nominal"] for d in debets)
        total_k = sum(k["nominal"] for k in kredits)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Debet", f"Rp {total_d:,.0f}")
        col2.metric("Total Kredit", f"Rp {total_k:,.0f}")
        col3.metric("Selisih", f"Rp {abs(total_d-total_k):,.0f}")
        if total_d == total_k and total_d > 0:
            st.success("✅ Balance!")
        elif total_d > 0 or total_k > 0:
            st.error("❌ Tidak balance!")

        submit = st.form_submit_button("💾 Catat Transaksi",
            use_container_width=True)
        if submit:
            if not keterangan:
                st.error("❌ Keterangan harus diisi!")
            elif total_d != total_k or total_d == 0:
                st.error("❌ Total debet harus sama dengan kredit!")
            else:
                if len(debets) == 1 and len(kredits) == 1:
                    tr_baru = {
                        "id": f"T{len(data)+1:02d}",
                        "tanggal": str(tanggal),
                        "keterangan": keterangan,
                        "debet": debets[0]["kode"],
                        "kredit": kredits[0]["kode"],
                        "nominal": total_d
                    }
                else:
                    tr_baru = {
                        "id": f"T{len(data)+1:02d}",
                        "tanggal": str(tanggal),
                        "keterangan": keterangan,
                        "debet": debets if len(debets) > 1 else debets[0]["kode"],
                        "kredit": kredits if len(kredits) > 1 else kredits[0]["kode"],
                        "nominal": total_d if len(debets) == 1 else 0
                    }
                data.append(tr_baru)
                simpan_transaksi(data)
                st.session_state.jml_d = 1
                st.session_state.jml_k = 1
                st.success("✅ Transaksi berhasil dicatat!")
                st.rerun()

# ========================
# JURNAL UMUM
# ========================
def buat_rows_jurnal(data, akun):
    rows = []
    for i, tr in enumerate(data):
        tanggal = tr["tanggal"]
        keterangan = tr.get("keterangan", "")
        ref = tr["id"]

        if isinstance(tr["debet"], list):
            for j, d in enumerate(tr["debet"]):
                rows.append({
                    "Tanggal": tanggal if j == 0 else "",
                    "Nama Akun / Keterangan": get_nama(d["kode"], akun),
                    "Ref": ref if j == 0 else "",
                    "Debet": f"Rp {d['nominal']:,.0f}",
                    "Kredit": ""
                })
        else:
            rows.append({
                "Tanggal": tanggal,
                "Nama Akun / Keterangan": get_nama(tr["debet"], akun),
                "Ref": ref,
                "Debet": f"Rp {tr['nominal']:,.0f}",
                "Kredit": ""
            })

        if isinstance(tr["kredit"], list):
            for k in tr["kredit"]:
                rows.append({
                    "Tanggal": "",
                    "Nama Akun / Keterangan": f"          {get_nama(k['kode'], akun)}",
                    "Ref": "",
                    "Debet": "",
                    "Kredit": f"Rp {k['nominal']:,.0f}"
                })
        else:
            rows.append({
                "Tanggal": "",
                "Nama Akun / Keterangan": f"          {get_nama(tr['kredit'], akun)}",
                "Ref": "",
                "Debet": "",
                "Kredit": f"Rp {tr['nominal']:,.0f}"
            })

        rows.append({
            "Tanggal": "",
            "Nama Akun / Keterangan": f"     ({keterangan})",
            "Ref": "", "Debet": "", "Kredit": ""
        })

        rows.append({
            "Tanggal": "", "Nama Akun / Keterangan": "",
            "Ref": "", "Debet": "", "Kredit": ""
        })
    return rows

def halaman_jurnal_umum(data, akun, t):
    st.header("📋 Jurnal Umum")
    st.caption("Periode: Januari – April 2026")
    if not data:
        st.warning("⚠️ Belum ada transaksi!")
        return

    rows = buat_rows_jurnal(data, akun)
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=600)

    total = sum(
        sum(d["nominal"] for d in tr["debet"])
        if isinstance(tr["debet"], list) else tr["nominal"]
        for tr in data)
    st.success(f"Total: Rp {total:,.0f}")

    st.markdown("---")
    st.subheader("🗑️ Hapus Transaksi")
    hapus_idx = st.selectbox("Pilih transaksi:",
        options=range(len(data)),
        format_func=lambda i: f"{data[i]['id']} | {data[i]['tanggal']} | {data[i]['keterangan']}")
    if st.button("🗑️ Hapus Transaksi Ini"):
        data.pop(hapus_idx)
        for i, tr in enumerate(data):
            tr["id"] = f"T{i+1:02d}"
        simpan_transaksi(data)
        st.success("✅ Berhasil dihapus!")
        st.rerun()

# ========================
# BUKU BESAR
# ========================
def halaman_buku_besar(data, akun, t):
    st.header("📚 Buku Besar")
    st.caption("Otomatis dari Jurnal Umum")
    saldo = hitung_saldo(data, akun)
    for kode, nama in akun.items():
        d = saldo[kode]["debet"]
        k = saldo[kode]["kredit"]
        if d > 0 or k > 0:
            with st.expander(f"📖 {kode} - {nama}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Debet", f"Rp {d:,.0f}")
                col2.metric("Total Kredit", f"Rp {k:,.0f}")
                col3.metric("Saldo", f"Rp {abs(d-k):,.0f}")
                rows = []
                for tr in data:
                    dv = kv = 0
                    if isinstance(tr["debet"], list):
                        for item in tr["debet"]:
                            if item["kode"] == kode:
                                dv = item["nominal"]
                    else:
                        if tr["debet"] == kode:
                            dv = tr["nominal"]
                    if isinstance(tr["kredit"], list):
                        for item in tr["kredit"]:
                            if item["kode"] == kode:
                                kv = item["nominal"]
                    else:
                        if tr["kredit"] == kode:
                            kv = tr["nominal"]
                    if dv > 0 or kv > 0:
                        rows.append({
                            "Tanggal": tr["tanggal"],
                            "Keterangan": tr["keterangan"],
                            "Debet": f"Rp {dv:,.0f}" if dv > 0 else "-",
                            "Kredit": f"Rp {kv:,.0f}" if kv > 0 else "-",
                        })
                if rows:
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ========================
# NERACA SALDO
# ========================
def halaman_neraca_saldo(data, akun, t, judul="Neraca Saldo", caption=""):
    st.header(f"⚖️ {judul}")
    if caption:
        st.caption(caption)
    saldo = hitung_saldo(data, akun)
    rows = []
    total_d = total_k = 0
    for kode, nama in akun.items():
        d = saldo[kode]["debet"]
        k = saldo[kode]["kredit"]
        if d > 0 or k > 0:
            sd = d - k if d > k else 0
            sk = k - d if k > d else 0
            rows.append({
                "Kode": kode, "Nama Akun": nama,
                "Debet": f"Rp {sd:,.0f}" if sd > 0 else "-",
                "Kredit": f"Rp {sk:,.0f}" if sk > 0 else "-"
            })
            total_d += sd
            total_k += sk
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    col1, col2 = st.columns(2)
    col1.metric("Total Debet", f"Rp {total_d:,.0f}")
    col2.metric("Total Kredit", f"Rp {total_k:,.0f}")
    if total_d == total_k:
        st.success("✅ Balance!")
    else:
        st.error(f"❌ Selisih: Rp {abs(total_d-total_k):,.0f}")

# ========================
# JURNAL PENYESUAIAN
# ========================
def halaman_jurnal_penyesuaian(data, akun, t):
    st.header("🔧 Jurnal Penyesuaian")
    penyesuaian = load_penyesuaian()

    st.subheader("➕ Input Jurnal Penyesuaian")
    if "jml_dp" not in st.session_state:
        st.session_state.jml_dp = 1
    if "jml_kp" not in st.session_state:
        st.session_state.jml_kp = 1

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("➕ Tambah Debet", key="add_dp"):
            st.session_state.jml_dp += 1
            st.rerun()
    with col2:
        if st.button("➕ Tambah Kredit", key="add_kp"):
            st.session_state.jml_kp += 1
            st.rerun()
    with col3:
        if st.button("🔄 Reset", key="reset_p"):
            st.session_state.jml_dp = 1
            st.session_state.jml_kp = 1
            st.rerun()

    with st.form("form_penyesuaian"):
        col1, col2 = st.columns(2)
        with col1:
            tanggal_p = st.date_input("📅 Tanggal")
            ket_p = st.text_input("📝 Keterangan")

        col_d, col_k = st.columns(2)
        debets_p = []
        kredits_p = []

        with col_d:
            st.subheader("📤 Akun Debet")
            for i in range(st.session_state.jml_dp):
                kode_d = st.selectbox(
                    f"Akun Debet {i+1}",
                    options=list(akun.keys()),
                    format_func=lambda x: f"{x} - {get_nama(x, akun)}",
                    key=f"dp_{i}")
                nom_d = st.number_input(
                    f"Nominal {i+1}",
                    min_value=0, step=1000, key=f"ndp_{i}")
                debets_p.append({"kode": kode_d, "nominal": nom_d})

        with col_k:
            st.subheader("📥 Akun Kredit")
            for i in range(st.session_state.jml_kp):
                kode_k = st.selectbox(
                    f"Akun Kredit {i+1}",
                    options=list(akun.keys()),
                    format_func=lambda x: f"{x} - {get_nama(x, akun)}",
                    key=f"kp_{i}")
                nom_k = st.number_input(
                    f"Nominal {i+1}",
                    min_value=0, step=1000, key=f"nkp_{i}")
                kredits_p.append({"kode": kode_k, "nominal": nom_k})

        total_dp = sum(d["nominal"] for d in debets_p)
        total_kp = sum(k["nominal"] for k in kredits_p)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Debet", f"Rp {total_dp:,.0f}")
        col2.metric("Total Kredit", f"Rp {total_kp:,.0f}")
        col3.metric("Selisih", f"Rp {abs(total_dp-total_kp):,.0f}")
        if total_dp == total_kp and total_dp > 0:
            st.success("✅ Balance!")

        sub_p = st.form_submit_button("💾 Simpan Penyesuaian",
            use_container_width=True)
        if sub_p:
            if not ket_p:
                st.error("❌ Keterangan harus diisi!")
            elif total_dp != total_kp or total_dp == 0:
                st.error("❌ Total debet harus sama dengan kredit!")
            else:
                if len(debets_p) == 1 and len(kredits_p) == 1:
                    p_baru = {
                        "id": f"P{len(penyesuaian)+1:02d}",
                        "tanggal": str(tanggal_p),
                        "keterangan": ket_p,
                        "debet": debets_p[0]["kode"],
                        "kredit": kredits_p[0]["kode"],
                        "nominal": total_dp
                    }
                else:
                    p_baru = {
                        "id": f"P{len(penyesuaian)+1:02d}",
                        "tanggal": str(tanggal_p),
                        "keterangan": ket_p,
                        "debet": debets_p if len(debets_p) > 1 else debets_p[0]["kode"],
                        "kredit": kredits_p if len(kredits_p) > 1 else kredits_p[0]["kode"],
                        "nominal": total_dp if len(debets_p) == 1 else 0
                    }
                penyesuaian.append(p_baru)
                simpan_penyesuaian(penyesuaian)
                st.session_state.jml_dp = 1
                st.session_state.jml_kp = 1
                st.success("✅ Penyesuaian disimpan!")
                st.rerun()

    if penyesuaian:
        st.markdown("---")
        st.subheader("📋 Daftar Jurnal Penyesuaian")
        rows = buat_rows_jurnal(penyesuaian, akun)
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, height=400)

        existing_ket = [tr.get("keterangan") for tr in data]
        sudah = all(p["keterangan"] in existing_ket for p in penyesuaian)
        if sudah:
            st.success("✅ Semua penyesuaian sudah diposting!")
        else:
            if st.button("✅ Posting ke Jurnal Umum",
                use_container_width=True):
                for p in penyesuaian:
                    if p["keterangan"] not in existing_ket:
                        data.append({
                            "id": f"T{len(data)+1:02d}",
                            "tanggal": p.get("tanggal", "2026-04-30"),
                            "keterangan": p["keterangan"],
                            "debet": p["debet"],
                            "kredit": p["kredit"],
                            "nominal": p["nominal"]
                        })
                simpan_transaksi(data)
                st.success("✅ Berhasil diposting!")
                st.rerun()

        st.markdown("---")
        st.subheader("🗑️ Hapus Penyesuaian")
        hapus_p = st.selectbox("Pilih:",
            range(len(penyesuaian)),
            format_func=lambda i: f"{penyesuaian[i]['id']} | {penyesuaian[i]['keterangan']}")
        if st.button("🗑️ Hapus"):
            penyesuaian.pop(hapus_p)
            simpan_penyesuaian(penyesuaian)
            st.success("✅ Dihapus!")
            st.rerun()
    else:
        st.info("Belum ada jurnal penyesuaian.")

# ========================
# LAPORAN LABA RUGI
# ========================
def halaman_laba_rugi(data, akun, t):
    st.header("📊 Laporan Laba Rugi")
    st.caption("Periode: Januari – April 2026")
    saldo = hitung_saldo(data, akun)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💰 Pendapatan")
        total_p = 0
        for kode, nama in akun.items():
            if kode.startswith("4-"):
                nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
                if nilai > 0:
                    st.write(f"• {nama}: **Rp {nilai:,.0f}**")
                    total_p += nilai
        st.markdown(f"**Total Pendapatan: Rp {total_p:,.0f}**")
    with col2:
        st.subheader("💸 Beban")
        total_b = 0
        for kode, nama in akun.items():
            if kode.startswith("5-"):
                nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
                if nilai > 0:
                    st.write(f"• {nama}: **Rp {nilai:,.0f}**")
                    total_b += nilai
        st.markdown(f"**Total Beban: Rp {total_b:,.0f}**")
    st.divider()
    laba = total_p - total_b
    if laba >= 0:
        st.success(f"✅ LABA BERSIH: Rp {laba:,.0f}")
    else:
        st.error(f"❌ RUGI BERSIH: Rp {abs(laba):,.0f}")

# ========================
# NERACA
# ========================
def halaman_neraca(data, akun, t):
    st.header("🏦 Neraca")
    st.caption("Per 30 April 2026")
    saldo = hitung_saldo(data, akun)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏢 ASET")
        total_aset = 0
        for kode, nama in akun.items():
            if kode.startswith("1-"):
                nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
                if nilai > 0:
                    st.write(f"• {kode} - {nama}: **Rp {nilai:,.0f}**")
                    total_aset += nilai
        st.markdown(f"**Total Aset: Rp {total_aset:,.0f}**")
    with col2:
        st.subheader("💼 KEWAJIBAN")
        total_ke = 0
        for kode, nama in akun.items():
            if kode.startswith("2-"):
                nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
                if nilai > 0:
                    st.write(f"• {kode} - {nama}: **Rp {nilai:,.0f}**")
                    total_ke += nilai
        st.subheader("💼 EKUITAS")
        for kode, nama in akun.items():
            if kode.startswith("3-"):
                nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
                if nilai != 0:
                    st.write(f"• {kode} - {nama}: **Rp {abs(nilai):,.0f}**")
                    total_ke += nilai
        st.markdown(f"**Total K+E: Rp {total_ke:,.0f}**")
    st.divider()
    if abs(total_aset - total_ke) < 1:
        st.success("✅ Neraca Balance!")
    else:
        st.error(f"❌ Selisih: Rp {abs(total_aset-total_ke):,.0f}")

# ========================
# JURNAL PENUTUP
# ========================
def halaman_jurnal_penutup(data, akun, t):
    st.header("📝 Jurnal Penutup")
    st.caption("Per 30 April 2026")
    saldo = hitung_saldo(data, akun)
    total_p = sum(saldo[k]["kredit"] - saldo[k]["debet"]
        for k in saldo if k.startswith("4-"))
    total_b = sum(saldo[k]["debet"] - saldo[k]["kredit"]
        for k in saldo if k.startswith("5-"))
    laba = total_p - total_b
    rows = []
    for kode, nama in akun.items():
        if kode.startswith("4-"):
            nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
            if nilai > 0:
                rows.append({
                    "Keterangan": f"Menutup {nama}",
                    "Akun Debet": nama,
                    "Akun Kredit": "Ikhtisar Laba Rugi",
                    "Nominal": f"Rp {nilai:,.0f}"
                })
    for kode, nama in akun.items():
        if kode.startswith("5-"):
            nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
            if nilai > 0:
                rows.append({
                    "Keterangan": f"Menutup {nama}",
                    "Akun Debet": "Ikhtisar Laba Rugi",
                    "Akun Kredit": nama,
                    "Nominal": f"Rp {nilai:,.0f}"
                })
    if laba >= 0:
        rows.append({
            "Keterangan": "Laba ke Modal",
            "Akun Debet": "Ikhtisar Laba Rugi",
            "Akun Kredit": "Modal Kakak & Adik",
            "Nominal": f"Rp {laba:,.0f}"
        })
    else:
        rows.append({
            "Keterangan": "Rugi ke Modal",
            "Akun Debet": "Modal Kakak & Adik",
            "Akun Kredit": "Ikhtisar Laba Rugi",
            "Nominal": f"Rp {abs(laba):,.0f}"
        })
    for kode, nama in akun.items():
        if kode.startswith("3-") and "Prive" in nama:
            nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
            if nilai > 0:
                rows.append({
                    "Keterangan": f"Menutup {nama}",
                    "Akun Debet": "Modal",
                    "Akun Kredit": nama,
                    "Nominal": f"Rp {nilai:,.0f}"
                })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ========================
# EKSPOR EXCEL
# ========================
def halaman_ekspor(data, akun, t):
    st.header("📁 Ekspor Excel")
    if not data:
        st.warning("⚠️ Belum ada transaksi!")
        return
    saldo = hitung_saldo(data, akun)

    rows_j = buat_rows_jurnal(data, akun)

    rows_ns = []
    total_d = total_k = 0
    for kode, nama in akun.items():
        d = saldo[kode]["debet"]
        k = saldo[kode]["kredit"]
        if d > 0 or k > 0:
            sd = d - k if d > k else 0
            sk = k - d if k > d else 0
            rows_ns.append({
                "Kode": kode, "Nama Akun": nama,
                "Debet": sd, "Kredit": sk
            })
            total_d += sd
            total_k += sk
    rows_ns.append({
        "Kode": "", "Nama Akun": "TOTAL",
        "Debet": total_d, "Kredit": total_k
    })

    rows_lr = []
    total_p = total_b = 0
    for kode, nama in akun.items():
        if kode.startswith("4-"):
            nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
            if nilai > 0:
                rows_lr.append({
                    "Keterangan": nama, "Pendapatan": nilai, "Beban": 0})
                total_p += nilai
    for kode, nama in akun.items():
        if kode.startswith("5-"):
            nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
            if nilai > 0:
                rows_lr.append({
                    "Keterangan": nama, "Pendapatan": 0, "Beban": nilai})
                total_b += nilai
    laba = total_p - total_b
    rows_lr.append({
        "Keterangan": "LABA BERSIH" if laba >= 0 else "RUGI BERSIH",
        "Pendapatan": 0, "Beban": abs(laba)
    })

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        pd.DataFrame(rows_j).to_excel(
            writer, sheet_name="Jurnal Umum", index=False)
        pd.DataFrame(rows_ns).to_excel(
            writer, sheet_name="Neraca Saldo", index=False)
        pd.DataFrame(rows_lr).to_excel(
            writer, sheet_name="Laba Rugi", index=False)
    buffer.seek(0)

    st.success("✅ File siap didownload!")
    st.download_button(
        label="📥 Download Laporan Excel",
        data=buffer,
        file_name="SICABE_Laporan_Keuangan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ========================
# KELOLA AKUN
# ========================
def halaman_kelola_akun(akun, t):
    st.header("✏️ Kelola Akun")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rename Akun")
        kode_pilih = st.selectbox("Pilih akun:",
            options=list(akun.keys()),
            format_func=lambda x: f"{x} - {akun[x]}")
        nama_baru = st.text_input("Nama baru:", value=akun[kode_pilih])
        if st.button("✅ Simpan"):
            akun[kode_pilih] = nama_baru
            simpan_akun(akun)
            st.success("✅ Berhasil direname!")
            st.rerun()
    with col2:
        st.subheader("📋 Semua Akun")
        rows = [{"Kode": k, "Nama Akun": v} for k, v in akun.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ========================
# PENGATURAN
# ========================
def halaman_pengaturan(t):
    st.header("⚙️ Pengaturan Tema")
    tema_baru = st.selectbox("🎨 Pilih Tema:",
        options=list(TEMA.keys()),
        index=list(TEMA.keys()).index(st.session_state.tema))
    cols = st.columns(len(TEMA))
    for i, (nama_tema, warna) in enumerate(TEMA.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background:{warna["bg"]};
            border:2px solid {warna["accent"]};
            border-radius:8px; padding:8px; text-align:center;'>
            <p style='color:{warna["accent"]}; font-weight:bold;
            margin:0; font-size:11px;'>{nama_tema}</p>
            </div>""", unsafe_allow_html=True)
    if st.button("✅ Terapkan Tema", use_container_width=True):
        st.session_state.tema = tema_baru
        st.success(f"✅ Tema '{tema_baru}' diterapkan!")
        st.rerun()