import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# 1. FUNGSI KEANGGOTAAN — SEGITIGA
# ==================================================
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)

# ==================================================
# 2. FUNGSI KEANGGOTAAN — TRAPESIUM
# ==================================================
def trapezoidal(x, a, b, c, d):
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        if a == b:
            return 1.0
        return (x - a) / (b - a)
    if c == d:
        return 1.0
    return (d - x) / (d - c)

# ==================================================
# 3. DEFINISI SEMUA VARIABEL FUZZY
# ==================================================
variabel_fuzzy = {
    "Tingkat Kerusakan": {
        "domain": (0, 100),
        "Rendah":   {"tipe": "trapesium", "parameter": (0, 0, 20, 40)},
        "Sedang":   {"tipe": "segitiga",  "parameter": (30, 50, 70)},
        "Tinggi":   {"tipe": "trapesium", "parameter": (60, 80, 100, 100)}
    },
    "Jumlah Laporan": {
        "domain": (0, 100),
        "Sedikit":  {"tipe": "trapesium", "parameter": (0, 0, 20, 40)},
        "Sedang":   {"tipe": "segitiga",  "parameter": (30, 50, 70)},
        "Banyak":   {"tipe": "trapesium", "parameter": (60, 80, 100, 100)}
    },
    "Prioritas Perbaikan": {
        "domain": (0, 100),
        "Rendah":   {"tipe": "trapesium", "parameter": (0, 0, 25, 45)},
        "Sedang":   {"tipe": "segitiga",  "parameter": (35, 55, 75)},
        "Tinggi":   {"tipe": "trapesium", "parameter": (65, 80, 100, 100)}
    }
}

# ==================================================
# 4. FUNGSI PEMANGGIL KEANGGOTAAN
# ==================================================
def hitung_keanggotaan(x, tipe, parameter):
    if tipe == "segitiga":
        return triangular(x, *parameter)
    elif tipe == "trapesium":
        return trapezoidal(x, *parameter)

# ==================================================
# 5. PROSES FUZZIFIKASI
# ==================================================
def fuzzifikasi(input_dict):
    hasil = {}
    nk = input_dict["kerusakan"]
    hasil["Tingkat Kerusakan"] = {
        lbl: hitung_keanggotaan(nk, d["tipe"], d["parameter"])
        for lbl, d in variabel_fuzzy["Tingkat Kerusakan"].items()
        if lbl != "domain"
    }
    nl = input_dict["laporan"]
    hasil["Jumlah Laporan"] = {
        lbl: hitung_keanggotaan(nl, d["tipe"], d["parameter"])
        for lbl, d in variabel_fuzzy["Jumlah Laporan"].items()
        if lbl != "domain"
    }
    return hasil

# ==================================================
# 6. VISUALISASI GRAFIK
# ==================================================
def plot_variabel(nama_variabel, nama_file):
    data = variabel_fuzzy[nama_variabel]
    x = np.linspace(*data["domain"], 500)
    plt.figure(figsize=(8, 5))
    warna = {"Rendah": "#2ca02c", "Sedang": "#ff7f0e", "Tinggi": "#d62728",
              "Sedikit": "#2ca02c", "Banyak": "#d62728"}
    for lbl, d in data.items():
        if lbl == "domain":
            continue
        y = [hitung_keanggotaan(xi, d["tipe"], d["parameter"]) for xi in x]
        plt.plot(x, y, label=lbl, linewidth=2.5, color=warna.get(lbl, None))
    plt.title(f"Fungsi Keanggotaan — {nama_variabel}", fontsize=13, fontweight="bold")
    plt.xlabel(nama_variabel, fontsize=11)
    plt.ylabel("Derajat Keanggotaan μ(x)", fontsize=11)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, alpha=0.35, linestyle=":")
    plt.legend(loc="upper right", fontsize=10)
    plt.tight_layout()
    plt.savefig(nama_file, dpi=300)
    plt.show()

# ==================================================
# 7. DATA UJI — 5 Skenario
# ==================================================
data_uji = [
    {"kasus": "Ekstrem Bawah",        "kerusakan": 0,  "laporan": 0},
    {"kasus": "Kondisi Tengah",       "kerusakan": 50, "laporan": 50},
    {"kasus": "Batas Transisi Bawah", "kerusakan": 40, "laporan": 40},
    {"kasus": "Batas Transisi Atas",  "kerusakan": 60, "laporan": 60},
    {"kasus": "Ekstrem Atas",         "kerusakan": 100,"laporan": 100}
]

# ==================================================
# 8. TAMPILKAN HASIL FUZZIFIKASI
# ==================================================
print("="*60)
print("   SISTEM PRIORITAS PERBAIKAN FASILITAS — FUZZIFIKASI")
print("="*60)

for d in data_uji:
    h = fuzzifikasi({"kerusakan": d["kerusakan"], "laporan": d["laporan"]})
    print(f"\n📌 {d['kasus']}")
    print(f"   Kerusakan: {d['kerusakan']}%  |  Laporan: {d['laporan']}")
    kr = h["Tingkat Kerusakan"]
    lp = h["Jumlah Laporan"]
    print(f"   Kerusakan → Rendah: {kr['Rendah']:.2f}  |  Sedang: {kr['Sedang']:.2f}  |  Tinggi: {kr['Tinggi']:.2f}")
    print(f"   Laporan   → Sedikit: {lp['Sedikit']:.2f}  |  Sedang: {lp['Sedang']:.2f}  |  Banyak: {lp['Banyak']:.2f}")

# ==================================================
# 9. BUAT & SIMPAN GRAFIK
# ==================================================
print("\n" + "="*60)
print("📊 Membuat grafik...")
plot_variabel("Tingkat Kerusakan",   "grafik_tingkat_kerusakan.png")
plot_variabel("Jumlah Laporan",      "grafik_jumlah_laporan.png")
plot_variabel("Prioritas Perbaikan", "grafik_prioritas_perbaikan.png")
print("✅ Semua grafik telah disimpan!")
