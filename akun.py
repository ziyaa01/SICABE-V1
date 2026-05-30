import json
import os

AKUN_DEFAULT = {
    "1-001": "Kas",
    "1-002": "Piutang Usaha",
    "1-003": "Persediaan Bibit",
    "1-004": "Persediaan Pupuk",
    "1-005": "Persediaan Pestisida",
    "1-006": "Perlengkapan Kebun - Bambu/Ajir",
    "1-007": "Perlengkapan Kebun - Plastik Mulsa",
    "1-008": "Aset Tetap - Irigasi Drip",
    "1-009": "Akumulasi Penyusutan Irigasi",
    "2-001": "Utang Usaha",
    "2-002": "Utang Bagi Hasil",
    "3-001": "Modal Kakak",
    "3-002": "Modal Adik",
    "3-003": "Prive Kakak",
    "3-004": "Prive Adik",
    "3-005": "Ikhtisar Laba Rugi",
    "4-001": "Pendapatan Penjualan Cabai",
    "5-001": "Beban Tenaga Kerja - Olah Lahan",
    "5-002": "Beban Tenaga Kerja - Penanaman",
    "5-003": "Beban Pupuk",
    "5-004": "Beban Perawatan - Upah Lepas",
    "5-005": "Beban Pestisida",
    "5-006": "Beban Upah Panen",
    "5-007": "Beban Bagi Hasil",
    "5-008": "Beban Penyusutan Irigasi",
}

AKUN_FILE = "akun_custom.json"

def load_akun():
    if os.path.exists(AKUN_FILE):
        with open(AKUN_FILE, "r") as f:
            return json.load(f)
    return dict(AKUN_DEFAULT)

def simpan_akun(data):
    with open(AKUN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_nama(kode, akun):
    return akun.get(kode, kode)