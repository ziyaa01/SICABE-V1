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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            logo = Image.open("logoo.png")
            st.image(logo, width=180, use_container_width=False)
        except:
            st.title("🌶️")

        st.title("SICABE")
        st.caption("Sistem Informasi Manajemen Cabai")
        st.divider()

        tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Daftar Akun Baru", "❓ Lupa Password"])

        with tab1:
            username = st.text_input("👤 Username", key="login_user")
            password = st.text_input(
                "🔒 Password", type="password", key="login_pass")
            if st.button("🔑 Login",
                use_container_width=True, key="btn_login"):
                if not username or not password:
                    st.error("❌ Username dan password harus diisi!")
                else:
                    users = load_users()
                    if username not in users:
                        st.error("❌ Username tidak ditemukan!")
                    else:
                        user_data = users[username]
                        if isinstance(user_data, dict):
                            password_asli = user_data.get("password", "")
                        else:
                            password_asli = user_data

                    if password_asli != password_asli:
                        st.error("❌ Password salah! Coba lagi.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"✅ Selamat datang, {username}!")
                        st.rerun()

        with tab2:
            st.subheader("Buat Akun Baru")
            new_user = st.text_input(
                "👤 Username Baru", key="reg_user")
            new_email = st.text_input("📧 Email")
            new_pass = st.text_input(
                "🔒 Password Baru",
                type="password", key="reg_pass")
            new_pass2 = st.text_input(
                "🔒 Konfirmasi Password",
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
                        st.error(
                            "❌ Konfirmasi password tidak cocok!")
                    elif len(new_pass) < 6:
                        st.error(
                            "❌ Password minimal 6 karakter!")
                    else:
                        users[new_user] = {"password": new_pass, "email": new_email}
                        simpan_users(users)
                        st.success(
                            f"✅ Akun '{new_user}' berhasil dibuat! "
                            f"Silakan login.")
            
        with tab3:
            st.subheader("Lupa Password")
            lupa_user = st.text_input("👤 Username", key="lupa_user")
            lupa_email = st.text_input("📧 Email Terdaftar", key="lupa_email")
    
            if st.button("🔍 Cek Password", use_container_width=True, key="btn_lupa"):
                if not lupa_user or not lupa_email:
                    st.error("❌ Username dan Email harus diisi!")
                else:
                    users = load_users()
                    if lupa_user not in users:
                        st.error("❌ Username tidak ditemukan!")
                    else:
                        user_data = users[lupa_user]

                        if isinstance(user_data, dict):
                            email_terdaftar = user_data.get("email", "")
                            password_lama = user_data.get("password", "")
                        else:
                            email_terdaftar = ""
                            password_lama = user_data
                
                        if lupa_email == email_terdaftar:
                            st.info(f"🔑 Password Anda adalah: **{password_lama}**")
                        else:
                            st.error("❌ Email yang Anda masukkan salah atau tidak cocok!")

# ========================
# HEADER
# ========================
def tampilkan_header():
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        st.image("logoo.png", width=130, use_container_width=False)

    with col2:
        st.title("SICABE")
        st.caption(
            f"Sistem Informasi Manajemen Cabai |  👤 {st.session_state.username}")
        
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    st.divider()

# ========================
# DASHBOARD
# ========================
def halaman_dashboard(data, akun):
    st.header("🏠 Dashboard")
    try:
        import transaksi as tr_modul
        data_penyesuaian = tr_modul.load_penyesuaian()
        data_total_dashboard = data + data_penyesuaian
    except:
        data_total_dashboard = data

    saldo = hitung_saldo(data_total_dashboard, akun)
    total_p = sum(
        saldo[k]["kredit"] - saldo[k]["debet"]
        for k in saldo if k.startswith("4-"))
    total_b = sum(
        saldo[k]["debet"] - saldo[k]["kredit"]
        for k in saldo if k.startswith("5-"))
    laba = total_p - total_b

    st.write("")
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
    with col2:
        st.metric("💰 Total Pendapatan", f"Rp {total_p:,.0f}")
    with col3:
        st.metric("💸 Total Beban", f"Rp {total_b:,.0f}")
    with col4:
        st.metric(
            "📈 Laba Bersih" if laba >= 0 else "📉 Rugi Bersih",
            f"Rp {abs(laba):,.0f}")
    st.write("")
    st.info(
        f"📊 Total transaksi: {len(data)}"
        f"  |  Periode: Januari – April 2026")

    st.divider()
    st.subheader("📌 Panduan Pencatatan Transaksi")

    panduan = [
        ("🌱 Beli bibit/benih",
         "Debet: Persediaan Bibit | Kredit: Kas"),
        ("🌿 Beli pupuk",
         "Debet: Persediaan Pupuk | Kredit: Kas"),
        ("🐛 Beli pestisida/obat hama",
         "Debet: Beban Pestisida | Kredit: Kas"),
        ("👷 Bayar upah pekerja",
         "Debet: Beban Tenaga Kerja | Kredit: Kas"),
        ("🌶️ Terima uang hasil jual cabai",
         "Debet: Kas | Kredit: Pendapatan Penjualan Cabai"),
        ("💧 Pakai pupuk dari stok",
         "Debet: Beban Pupuk | Kredit: Persediaan Pupuk"),
        ("🏦 Setor modal awal usaha",
         "Debet: Kas | Kredit: Modal Pemilik"),
        ("💸 Bayar bagi hasil ke pemilik lahan",
         "Debet: Beban Bagi Hasil | Kredit: Kas"),
        ("⚙️ Penyesuaian Irigasi Drip (Akhir Bulan)", 
         "Debet: Beban Penyusutan Alat | Kredit: Akumulasi Penyusutan Alat. [LOGIKA]: Alat drip 1 juta kamu disusutkan selama 3 tahun (36 bulan) karena rawan rusak/mampet di lahan. Sistem otomatis memotong Rp 27.778 setiap akhir bulan agar pengeluaran kebun adil dan laporan bulanan tidak langsung rugi besar di awal."),
        ("🔒 Jurnal Penutup (Akhir Periode Panen)", 
         "meriset kembali semua isi Pendapatan & Beban ke Rp 0. [LOGIKA]: Karena panen cabai terjadi seminggu 2 kali selama berbulan-bulan, biarkan menu ini JANGAN diklik dulu selama masa panen aktif. Begitu seluruh gelombang panen selesai total dan lahan mau dibongkar untuk bibit baru, barulah klik menu ini untuk meriset kalkulator ke Rp 0 agar untung-rugi musim berikutnya tidak tercampur hasil lama.")
    ]

    with st.container(border=True):
        st.write(
            "**Panduan singkat pencatatan transaksi kebun cabai:**")
        for judul, detail in panduan:
            st.write(f"**{judul}**")
            st.caption(f"→ {detail}")
            st.write("")

    st.divider()
    st.subheader("📝 Catatan")
    catatan_lama = ""
    try:
        with open("catatan.txt", "r") as f:
            catatan_lama = f.read()
    except:
        pass
    catatan = st.text_area(
        "Tulis catatan di sini...",
        value=catatan_lama,
        height=150,
        placeholder="Contoh: Musim tanam dimulai Januari 2026...")
    if st.button("💾 Simpan Catatan"):
        with open("catatan.txt", "w") as f:
            f.write(catatan)
        st.success("✅ Catatan tersimpan!")

# ========================
# INPUT TRANSAKSI
# ========================
def halaman_input_transaksi(data, akun):
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
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Debet", f"Rp {total_d:,.0f}")
        col2.metric("Total Kredit", f"Rp {total_k:,.0f}")
        col3.metric("Selisih", f"Rp {abs(total_d-total_k):,.0f}")
        if total_d == total_k and total_d > 0:
            st.success("✅ Balance!")
        elif total_d > 0 or total_k > 0:
            st.error("❌ Tidak balance!")

        submit = st.form_submit_button(
            "💾 Catat Transaksi", use_container_width=True)
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
                        "debet": (debets if len(debets) > 1
                                  else debets[0]["kode"]),
                        "kredit": (kredits if len(kredits) > 1
                                   else kredits[0]["kode"]),
                        "nominal": (total_d
                                    if len(debets) == 1 else 0)
                    }
                data.append(tr_baru)
                simpan_transaksi(data)
                st.session_state.jml_d = 1
                st.session_state.jml_k = 1
                st.success("✅ Transaksi berhasil dicatat!")
                st.rerun()

# ========================
# BUAT ROWS JURNAL
# ========================
def buat_rows_jurnal(data, akun):
    rows = []
    for tr in data:
        tanggal = tr["tanggal"]
        keterangan = tr.get("keterangan", "")
        ref = tr["id"]

        if isinstance(tr["debet"], list):
            for j, d in enumerate(tr["debet"]):
                rows.append({
                    "Tanggal": tanggal if j == 0 else "",
                    "Nama Akun / Keterangan": get_nama(
                        d["kode"], akun),
                    "Ref": ref if j == 0 else "",
                    "Debet": f"Rp {d['nominal']:,.0f}",
                    "Kredit": ""
                })
        else:
            rows.append({
                "Tanggal": tanggal,
                "Nama Akun / Keterangan": get_nama(
                    tr["debet"], akun),
                "Ref": ref,
                "Debet": f"Rp {tr['nominal']:,.0f}",
                "Kredit": ""
            })

        if isinstance(tr["kredit"], list):
            for k in tr["kredit"]:
                rows.append({
                    "Tanggal": "",
                    "Nama Akun / Keterangan": (
                        f"          {get_nama(k['kode'], akun)}"),
                    "Ref": "",
                    "Debet": "",
                    "Kredit": f"Rp {k['nominal']:,.0f}"
                })
        else:
            rows.append({
                "Tanggal": "",
                "Nama Akun / Keterangan": (
                    f"          {get_nama(tr['kredit'], akun)}"),
                "Ref": "",
                "Debet": "",
                "Kredit": f"Rp {tr['nominal']:,.0f}"
            })

        rows.append({
            "Tanggal": "",
            "Nama Akun / Keterangan": f"({keterangan})",
            "Ref": "", "Debet": "", "Kredit": ""
        })

        rows.append({
            "Tanggal": "",
            "Nama Akun / Keterangan": "",
            "Ref": "", "Debet": "", "Kredit": ""
        })
    return rows

# ========================
# JURNAL UMUM
# ========================
def halaman_jurnal_umum(data, akun):
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

    st.divider()
    st.subheader("🗑️ Hapus Transaksi")
    hapus_idx = st.selectbox(
        "Pilih transaksi:",
        options=range(len(data)),
        format_func=lambda i: (
            f"{data[i]['id']} | {data[i]['tanggal']}"
            f" | {data[i]['keterangan']}"))
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
def halaman_buku_besar(data, akun):
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
                            "Debet": (f"Rp {dv:,.0f}"
                                      if dv > 0 else "-"),
                            "Kredit": (f"Rp {kv:,.0f}"
                                       if kv > 0 else "-"),
                        })
                if rows:
                    st.dataframe(
                        pd.DataFrame(rows),
                        use_container_width=True)

# ========================
# NERACA SALDO
# ========================
def halaman_neraca_saldo(
        data, akun,
        judul="Neraca Saldo", caption=""):
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
                "Kode": kode,
                "Nama Akun": nama,
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
def halaman_jurnal_penyesuaian(data, akun):
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
                    format_func=lambda x: (
                        f"{x} - {get_nama(x, akun)}"),
                    key=f"dp_{i}")
                nom_d = st.number_input(
                    f"Nominal {i+1}",
                    min_value=0, step=1000,
                    key=f"ndp_{i}")
                debets_p.append({
                    "kode": kode_d, "nominal": nom_d})

        with col_k:
            st.subheader("📥 Akun Kredit")
            for i in range(st.session_state.jml_kp):
                kode_k = st.selectbox(
                    f"Akun Kredit {i+1}",
                    options=list(akun.keys()),
                    format_func=lambda x: (
                        f"{x} - {get_nama(x, akun)}"),
                    key=f"kp_{i}")
                nom_k = st.number_input(
                    f"Nominal {i+1}",
                    min_value=0, step=1000,
                    key=f"nkp_{i}")
                kredits_p.append({
                    "kode": kode_k, "nominal": nom_k})

        total_dp = sum(d["nominal"] for d in debets_p)
        total_kp = sum(k["nominal"] for k in kredits_p)
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Debet", f"Rp {total_dp:,.0f}")
        col2.metric("Total Kredit", f"Rp {total_kp:,.0f}")
        col3.metric("Selisih",
            f"Rp {abs(total_dp-total_kp):,.0f}")
        if total_dp == total_kp and total_dp > 0:
            st.success("✅ Balance!")

        sub_p = st.form_submit_button(
            "💾 Simpan Penyesuaian",
            use_container_width=True)
        if sub_p:
            if not ket_p:
                st.error("❌ Keterangan harus diisi!")
            elif total_dp != total_kp or total_dp == 0:
                st.error(
                    "❌ Total debet harus sama dengan kredit!")
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
                        "debet": (debets_p
                                  if len(debets_p) > 1
                                  else debets_p[0]["kode"]),
                        "kredit": (kredits_p
                                   if len(kredits_p) > 1
                                   else kredits_p[0]["kode"]),
                        "nominal": (total_dp
                                    if len(debets_p) == 1
                                    else 0)
                    }
                penyesuaian.append(p_baru)
                simpan_penyesuaian(penyesuaian)
                st.session_state.jml_dp = 1
                st.session_state.jml_kp = 1
                st.success("✅ Penyesuaian disimpan!")
                st.rerun()

    if penyesuaian:
        st.divider()
        st.subheader("📋 Daftar Jurnal Penyesuaian")
        rows = buat_rows_jurnal(penyesuaian, akun)
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            height=400)

        existing_ket = [tr.get("keterangan") for tr in data]
        sudah = all(
            p["keterangan"] in existing_ket
            for p in penyesuaian)
        st.success("Semua jurnal penyesuaian berhasil disimpan di sistem!")

        st.divider()
        st.subheader("🗑️ Hapus Penyesuaian")
        hapus_p = st.selectbox(
            "Pilih:",
            range(len(penyesuaian)),
            format_func=lambda i: (
                f"{penyesuaian[i]['id']}"
                f" | {penyesuaian[i]['keterangan']}"))
        if st.button("🗑️ Hapus"):
            penyesuaian.pop(hapus_p)
            simpan_penyesuaian(penyesuaian)
            st.success("✅ Dihapus!")
            st.rerun()
    else:
        st.info("Belum ada jurnal penyesuaian.")

# ========================
# BUKU BESAR SETELAH PENYESUAIAN
# ========================
def halaman_buku_besar_setelah_penyesuaian(data, akun):
    st.header("📚 Buku Besar")
    st.caption("Otomatis dari Jurnal Penyesuaian")

    data_gabungan = data + load_penyesuaian()
    
    saldo = hitung_saldo(data_gabungan, akun)

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
                for tr in data_gabungan:
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
                            "Debet": (f"Rp {dv:,.0f}"
                                      if dv > 0 else "-"),
                            "Kredit": (f"Rp {kv:,.0f}"
                                       if kv > 0 else "-"),
                        })
                if rows:
                    st.dataframe(
                        pd.DataFrame(rows),
                        use_container_width=True)
                    
# ========================
# NERACA SALDO SETELAH PENYESUAIAN
# ========================
def halaman_neraca_saldo(
        data, akun,
        judul="Neraca Saldo Setelah Penyesuaian", caption=""):
    st.header(f"⚖️ {judul}")
    if caption:
        st.caption(caption)
        if "Setelah" in judul or "Disesuaikan" in judul:  
            try:
                import transaksi as tr_modul
                data_penyesuaian = tr_modul.load_penyesuaian()
                data_total_nsd = data + data_penyesuaian
            except:
                data_total_nsd = data
            saldo = hitung_saldo(data_total_nsd, akun)
        else:
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
                "Kode": kode,
                "Nama Akun": nama,
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
# LAPORAN LABA RUGI
# ========================
def halaman_laba_rugi(data, akun):
    st.header("📊 Laporan Laba Rugi")
    st.caption("Periode: Januari – April 2026")
    try:
        import transaksi as tr_modul
        data_penyesuaian = tr_modul.load_penyesuaian()
        data_total_lr = data + data_penyesuaian
    except:
        data_total_lr = data
    saldo = hitung_saldo(data_total_lr, akun)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💰 Pendapatan")
        total_p = 0
        for kode, nama in akun.items():
            if kode.startswith("4-"):
                nilai = (saldo[kode]["kredit"]
                         - saldo[kode]["debet"])
                if nilai > 0:
                    st.write(f"• {nama}: **Rp {nilai:,.0f}**")
                    total_p += nilai
        st.write(f"**Total Pendapatan: Rp {total_p:,.0f}**")
    with col2:
        st.subheader("💸 Beban")
        total_b = 0
        for kode, nama in akun.items():
            if kode.startswith("5-"):
                nilai = (saldo[kode]["debet"]
                         - saldo[kode]["kredit"])
                if nilai > 0:
                    st.write(f"• {nama}: **Rp {nilai:,.0f}**")
                    total_b += nilai
        st.write(f"**Total Beban: Rp {total_b:,.0f}**")
    st.divider()
    laba = total_p - total_b
    if laba >= 0:
        st.success(f"✅ LABA BERSIH: Rp {laba:,.0f}")
    else:
        st.error(f"❌ RUGI BERSIH: Rp {abs(laba):,.0f}")

# ========================
# NERACA
# ========================
def halaman_neraca(data, akun):
    st.header("🏦 Neraca")
    st.caption("Per 30 April 2026")
    try:
        import transaksi as tr_modul
        data_penyesuaian = tr_modul.load_penyesuaian()
        data_total_neraca = data + data_penyesuaian
    except:
        data_total_neraca = data
    saldo = hitung_saldo(data_total_neraca, akun)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 ASET")
        total_aset = 0
        for kode, nama in akun.items():
            if kode.startswith("1-"):
                if "akumulasi penyusutan" in nama or saldo[kode]["kredit"]>saldo[kode]["debet"]:
                    nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
                    total_aset -= nilai
                    st.write(f". {kode} - {nama}: -Rp {nilai:,.0f}")
                else:
                    nilai = (saldo[kode]["debet"]
                         - saldo[kode]["kredit"])
                    total_aset += nilai 
                    st.write(f"• {kode} - {nama}: Rp {nilai:,.0f}")         
        
    with col2:
        st.subheader("💼 KEWAJIBAN")
        total_ke = 0
        for kode, nama in akun.items():
            if kode.startswith("2-"):
                nilai = (saldo[kode]["kredit"]
                         - saldo[kode]["debet"])
                if nilai > 0:
                    st.write(
                        f"• {kode} - {nama}:"
                        f" **Rp {nilai:,.0f}**")
                    total_ke += nilai
                    
        st.subheader("💼 EKUITAS")
        for kode, nama in akun.items():
            if kode.startswith("3-"):
                nilai = (saldo[kode]["kredit"]
                         - saldo[kode]["debet"])
                if nilai != 0:
                    st.write(
                        f"• {kode} - {nama}:"
                        f" **Rp {abs(nilai):,.0f}**")
                    total_ke += nilai          

        total_pendapatan = 0
        total_beban = 0
        for kode in akun:
            if kode.startswith("4-"): # Pendapatan
                total_pendapatan += (saldo[kode]["kredit"] - saldo[kode]["debet"])
            elif kode.startswith("5-"): # Beban
                total_beban += (saldo[kode]["debet"] - saldo[kode]["kredit"])
        
        laba_neto = total_pendapatan - total_beban
        
        if laba_neto != 0:
            st.write(f"• 3-005 - Ikhtisar Laba Rugi: **Rp {laba_neto:,.0f}**")
            total_ke += laba_neto
        
        st.write(f"**Total K+E: Rp {total_ke:,.0f}**")     
    st.divider()
    if abs(total_aset - total_ke) < 1:
        st.success("✅ Neraca Balance!")
    else:
        st.error(
            f"❌ Selisih: Rp {abs(total_aset-total_ke):,.0f}")

# ========================
# JURNAL PENUTUP
# ========================
def halaman_jurnal_penutup(data, akun):
    st.header("📝 Jurnal Penutup")
    st.caption("Per 30 April 2026")
    data_gabungan = data + load_penyesuaian()
    saldo = hitung_saldo(data_gabungan, akun)
    total_p = sum(saldo[k]["kredit"] - saldo[k]["debet"] for k in saldo if k.startswith("4-"))
    total_b = sum(saldo[k]["debet"] - saldo[k]["kredit"] for k in saldo if k.startswith("5-"))
    laba = total_p - total_b
    rows = []
    
    for kode, nama in akun.items():
        if kode.startswith("4-"):
            nilai = saldo[kode]["kredit"] - saldo[kode]["debet"]
            if nilai > 0:
                rows.append({"Tanggal": "2026-04-30", "Keterangan": nama, "Debet": nilai, "Kredit": 0})
                rows.append({"Tanggal": "2026-04-30", "Keterangan": "   Ikhtisar Laba Rugi", "Debet": 0, "Kredit": nilai})
                
    for kode, nama in akun.items():
        if kode.startswith("5-"):
            nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
            if nilai > 0:
                rows.append({"Tanggal": "2026-04-30", "Keterangan": "Ikhtisar Laba Rugi", "Debet": nilai, "Kredit": 0})
                rows.append({"Tanggal": "2026-04-30", "Keterangan": f"   {nama}", "Debet": 0, "Kredit": nilai})
                
    if laba >= 0:
        if laba > 0:
            rows.append({"Tanggal": "2026-04-30", "Keterangan": "Ikhtisar Laba Rugi", "Debet": laba, "Kredit": 0})
            rows.append({"Tanggal": "2026-04-30", "Keterangan": "   Modal Kakak & Adik", "Debet": 0, "Kredit": laba})
    else:
        rows.append({"Tanggal": "2026-04-30", "Keterangan": "Modal Kakak & Adik", "Debet": abs(laba), "Kredit": 0})
        rows.append({"Tanggal": "2026-04-30", "Keterangan": "   Ikhtisar Laba Rugi", "Debet": 0, "Kredit": abs(laba)})
        
    for kode, nama in akun.items():
        if kode.startswith("3-") and "Prive" in nama:
            nilai = saldo[kode]["debet"] - saldo[kode]["kredit"]
            if nilai > 0:
                rows.append({"Tanggal": "2026-04-30", "Keterangan": "Modal Kakak & Adik", "Debet": nilai, "Kredit": 0})
                rows.append({"Tanggal": "2026-04-30", "Keterangan": f"   {nama}", "Debet": 0, "Kredit": nilai})
                
    if rows:
        df_jp = pd.DataFrame(rows)
        def format_nol(val):
            if val == 0:
                return "-"
            else:
                return f"Rp {val:,.0f}"
        
        df_tampil = df_jp.style.format({"Debet": format_nol, "Kredit": format_nol})
        st.dataframe(df_tampil, use_container_width=True)
    else:
        st.info("Belum ada data jurnal penutup.")

# ========================
# EKSPOR EXCEL
# ========================
def halaman_ekspor(data, akun):
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
            nilai = (saldo[kode]["kredit"]
                     - saldo[kode]["debet"])
            if nilai > 0:
                rows_lr.append({
                    "Keterangan": nama,
                    "Pendapatan": nilai, "Beban": 0})
                total_p += nilai
    for kode, nama in akun.items():
        if kode.startswith("5-"):
            nilai = (saldo[kode]["debet"]
                     - saldo[kode]["kredit"])
            if nilai > 0:
                rows_lr.append({
                    "Keterangan": nama,
                    "Pendapatan": 0, "Beban": nilai})
                total_b += nilai
    laba = total_p - total_b
    rows_lr.append({
        "Keterangan": (
            "LABA BERSIH" if laba >= 0 else "RUGI BERSIH"),
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
        mime=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"),
        use_container_width=True
    )

# ========================
# KELOLA AKUN
# ========================
def halaman_kelola_akun(akun):
    st.header("✏️ Kelola Akun")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rename Akun")
        kode_pilih = st.selectbox(
            "Pilih akun:",
            options=list(akun.keys()),
            format_func=lambda x: f"{x} - {akun[x]}")
        nama_baru = st.text_input(
            "Nama baru:", value=akun[kode_pilih])
        if st.button("✅ Simpan"):
            akun[kode_pilih] = nama_baru
            simpan_akun(akun)
            st.success("✅ Berhasil direname!")
            st.rerun()
    with col2:
        st.subheader("📋 Semua Akun")
        rows = [{"Kode": k, "Nama Akun": v}
                for k, v in akun.items()]
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True)