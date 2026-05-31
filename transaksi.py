import json
import os
import streamlit as st

def get_filename(jenis):
    username = st.session_state.get("username", "default")
    if username and username != "default" and username != "":
        return f"data_{jenis}_{username}.json"
    return f"data_{jenis}.json"

def load_transaksi():
    filename = get_filename("transaksi")
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    data = sorted(data, key=lambda x: x.get("tanggal", ""))
                return data
            except:
                return []
    return []

def simpan_transaksi(data):
    filename = get_filename("transaksi")
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def load_penyesuaian():
    filename = get_filename("penyesuaian")
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def simpan_penyesuaian(data):
    filename = get_filename("penyesuaian")
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def hitung_saldo(data, akun):
    saldo = {kode: {"debet": 0, "kredit": 0} for kode in akun}
    for tr in data:
        if isinstance(tr["debet"], list):
            for d in tr["debet"]:
                if d["kode"] in saldo:
                    saldo[d["kode"]]["debet"] += d["nominal"]
        else:
            if tr["debet"] in saldo:
                saldo[tr["debet"]]["debet"] += tr["nominal"]
        if isinstance(tr["kredit"], list):
            for k in tr["kredit"]:
                if k["kode"] in saldo:
                    saldo[k["kode"]]["kredit"] += k["nominal"]
        else:
            if tr["kredit"] in saldo:
                saldo[tr["kredit"]]["kredit"] += tr["nominal"]
    return saldo

def get_buku_besar_setelah_penyesuaian(data_umum, data_penyesuaian, akun_target):
    saldo_sebelum = hitung_saldo(data_umum, [akun_target])
    debet_awal = saldo_sebelum[akun_target]["debet"]
    kredit_awal = saldo_sebelum[akun_target]["kredit"]
    saldo_neto_awal = debet_awal - kredit_awal
    
    buku_besar_ajp = [
        {
            "tanggal": "30 April 2026",
            "keterangan": "Saldo Awal Sebelum Penyesuaian",
            "debet": debet_awal if saldo_neto_awal >= 0 else 0,
            "kredit": kredit_awal if saldo_neto_awal < 0 else 0,
            "saldo": abs(saldo_neto_awal)
        }
    ]
    
    for tr in data_penyesuaian:
        if "debet" in tr and isinstance(tr["debet"], list):
            for d in tr["debet"]:
                if d["kode"] == akun_target:
                    buku_besar_ajp.append({
                        "tanggal": "30 April 2026",
                        "keterangan": tr.get("keterangan", "Penyesuaian"),
                        "debet": d["nominal"],
                        "kredit": 0,
                        "saldo": 0
                    })
        if "kredit" in tr and isinstance(tr["kredit"], list):
            for k in tr["kredit"]:
                if k["kode"] == akun_target:
                    buku_besar_ajp.append({
                        "tanggal": "30 April 2026",
                        "keterangan": tr.get("keterangan", "Penyesuaian"),
                        "debet": 0,
                        "kredit": k["nominal"],
                        "saldo": 0
                    })
    return buku_besar_ajp