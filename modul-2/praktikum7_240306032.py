import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. DEFINISI FUNGSI KEANGGOTAAN SEGI TIGA & TRAPESIUM
# ==========================================================
def trimf(x, params):
    """Fungsi keanggotaan segitiga [a, b, c]"""
    a, b, c = params
    y = np.zeros_like(x)
    idx1 = (x > a) & (x <= b)
    if np.any(idx1) and b != a:
        y[idx1] = (x[idx1] - a) / (b - a)
    idx2 = (x > b) & (x < c)
    if np.any(idx2) and c != b:
        y[idx2] = (c - x[idx2]) / (c - b)
    return np.clip(y, 0.0, 1.0)


# ==========================================================
# 2. DEFINISI DOMAIN DAN SEMESTA
# ==========================================================
# Domain Output: Besaran Diskon [0 - 30%]
z = np.linspace(0, 30, 300)

mf_diskon_kecil = trimf(z, [0, 5, 12])
mf_diskon_sedang = trimf(z, [8, 15, 22])
mf_diskon_besar = trimf(z, [18, 25, 30])


# ==========================================================
# 3. SIMULASI NILAI FIRING STRENGTH DARI ATURAN
# ==========================================================
# Misal hasil evaluasi aturan menghasilkan:
alpha_kecil = 0.00
alpha_sedang = 0.20
alpha_besar = 0.75

# Implikasi (Mamdani Min)
imp_kecil = np.minimum(alpha_kecil, mf_diskon_kecil)
imp_sedang = np.minimum(alpha_sedang, mf_diskon_sedang)
imp_besar = np.minimum(alpha_besar, mf_diskon_besar)

# Agregasi (Max)
agregasi = np.maximum(imp_kecil, np.maximum(imp_sedang, imp_besar))


# ==========================================================
# 4. DEFUZZIFIKASI CENTROID (DISKRIT)
# ==========================================================
def defuzzifikasi_centroid(x_vals, mu_vals):
    total_mu = np.sum(mu_vals)
    if total_mu == 0:
        return 0.0
    return np.sum(x_vals * mu_vals) / total_mu

z_crisp = defuzzifikasi_centroid(z, agregasi)


# ==========================================================
# 5. VISUALISASI PIPELINE FIS
# ==========================================================
plt.figure(figsize=(12, 6))

plt.plot(z, mf_diskon_kecil, 'g--', label='MF Kecil', alpha=0.5)
plt.plot(z, mf_diskon_sedang, 'b--', label='MF Sedang', alpha=0.5)
plt.plot(z, mf_diskon_besar, 'r--', label='MF Besar', alpha=0.5)

# Gambar kurva terpotong & area agregasi
plt.fill_between(z, 0, agregasi, color='purple', alpha=0.35, label='Daerah Agregasi Fuzzy')
plt.plot(z, agregasi, color='purple', linewidth=2.5)

# Garis titik berat hasil defuzzifikasi
plt.axvline(x=z_crisp, color='black', linewidth=2.5, linestyle='-', 
            label=f'Crisp Output (Centroid = {z_crisp:.2f}%)')
plt.scatter([z_crisp], [0], color='black', s=80, zorder=6)

plt.title('Arsitektur FIS: Hasil Implikasi, Agregasi, dan Defuzzifikasi Centroid', fontsize=13, fontweight='bold')
plt.xlabel('Besaran Diskon (%)', fontsize=11)
plt.ylabel('Derajat Keanggotaan μ(z)', fontsize=11)
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

plt.savefig('pipeline_fis_agregasi_defuzzifikasi.png', dpi=300)
plt.show()

print(f"Keputusan Akhir Sistem FIS:")
print(f" - Rekomendasi Diskon: {z_crisp:.2f}%")
