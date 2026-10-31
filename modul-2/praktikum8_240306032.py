import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# ==========================================================
# 1. DEFINISI SEMESTA DAN BENTUK KURVA AGREGASI
# ==========================================================
# Semesta output: Tingkat Risiko Keamanan TI [0 - 100%]
z = np.linspace(0, 100, 1000)

# Bentuk fungsi keanggotaan output
mf_rendah = fuzz.trapmf(z, [0, 0, 20, 40])
mf_sedang = fuzz.trimf(z, [30, 50, 70])
mf_tinggi = fuzz.trapmf(z, [60, 80, 100, 100])

# Simulasi Firing Strength dari aturan
alpha_rendah = 0.3
alpha_sedang = 0.7
alpha_tinggi = 0.5

# Implikasi Min
imp_rendah = np.fmin(alpha_rendah, mf_rendah)
imp_sedang = np.fmin(alpha_sedang, mf_sedang)
imp_tinggi = np.fmin(alpha_tinggi, mf_tinggi)

# Agregasi Max
agregasi = np.fmax(imp_rendah, np.fmax(imp_sedang, imp_tinggi))


# ==========================================================
# 2. PERHITUNGAN 5 METODE DEFUZZIFIKASI DENGAN SCIKIT-FUZZY
# ==========================================================
defuzz_methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
hasil_defuzz = {}

for method in defuzz_methods:
    val = fuzz.defuzz(z, agregasi, method)
    hasil_defuzz[method] = val


# ==========================================================
# 3. MENAMPILKAN HASIL DAN VISUALISASI
# ==========================================================
print("=" * 60)
print("HASIL KOMPARASI METODE DEFUZZIFIKASI MAMDANI")
print("=" * 60)
for m, v in hasil_defuzz.items():
    print(f" - Metode {m.upper():<10} : {v:.3f}%")
print("=" * 60)

plt.figure(figsize=(12, 6.5))
plt.plot(z, agregasi, 'b', linewidth=2.5, label='Kurva Agregasi Fuzzy')
plt.fill_between(z, 0, agregasi, color='skyblue', alpha=0.4)

colors = {
    'centroid': 'red',
    'bisector': 'purple',
    'mom': 'black',
    'som': 'green',
    'lom': 'orange'
}

for method, val in hasil_defuzz.items():
    plt.axvline(x=val, color=colors[method], linestyle='--', linewidth=2, 
                label=f'{method.upper()} ({val:.2f})')
    # Ambil nilai mu pada titik tersebut
    idx = np.abs(z - val).argmin()
    plt.scatter([val], [agregasi[idx]], color=colors[method], s=60, zorder=6)

plt.title('Perbandingan 5 Metode Defuzzifikasi pada Metode Mamdani', fontsize=13, fontweight='bold')
plt.xlabel('Tingkat Risiko Keamanan (%)', fontsize=11)
plt.ylabel('Derajat Keanggotaan μ(z)', fontsize=11)
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right', fontsize=10)
plt.tight_layout()

plt.savefig('komparasi_metode_defuzzifikasi.png', dpi=300)
plt.show()
