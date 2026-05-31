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