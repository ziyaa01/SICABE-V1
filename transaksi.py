import json
import os

TRANSAKSI_FILE = "data_transaksi.json"
PENYESUAIAN_FILE = "data_penyesuaian.json"

def load_transaksi():
    if os.path.exists(TRANSAKSI_FILE):
        with open(TRANSAKSI_FILE, "r") as f:
            return json.load(f)
    return []

def simpan_transaksi(data):
    with open(TRANSAKSI_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_penyesuaian():
    if os.path.exists(PENYESUAIAN_FILE):
        with open(PENYESUAIAN_FILE, "r") as f:
            return json.load(f)
    return []

def simpan_penyesuaian(data):
    with open(PENYESUAIAN_FILE, "w") as f:
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