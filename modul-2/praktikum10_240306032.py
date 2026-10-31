import numpy as np

# ==========================================================
# 1. IMPLEMENTASI SISTEM SUGENO (ORDE 0 DAN ORDE 1)
# ==========================================================
def hitung_sugeno(alphas, z_values):
    """
    alphas: list firing strength [alpha_1, alpha_2, ...]
    z_values: list output tegas aturan [z_1, z_2, ...]
    """
    alphas = np.array(alphas)
    z_values = np.array(z_values)
    
    total_alpha = np.sum(alphas)
    if total_alpha == 0:
        return 0.0
    return np.sum(alphas * z_values) / total_alpha


# ==========================================================
# 2. IMPLEMENTASI SISTEM TSUKAMOTO
# ==========================================================
def invers_monoton_naik(alpha, a, b):
    """z = a + alpha * (b - a)"""
    return a + alpha * (b - a)


def invers_monoton_turun(alpha, a, b):
    """z = b - alpha * (b - a)"""
    return b - alpha * (b - a)


def hitung_tsukamoto(alphas, fungsi_invers_list):
    """
    fungsi_invers_list: list lambda fungsi invers untuk setiap aturan
    """
    z_values = [func(alpha) for alpha, func in zip(alphas, fungsi_invers_list)]
    return hitung_sugeno(alphas, z_values), z_values


# ==========================================================
# 3. PENGUJIAN DAN KOMPARASI KASUS
# ==========================================================
alphas_kasus = [0.2, 0.4, 0.2, 0.6]

# A. Sugeno Orde 0
z_sugeno0 = [2.0, 4.0, 5.0, 8.0]
hasil_sugeno0 = hitung_sugeno(alphas_kasus, z_sugeno0)

# B. Sugeno Orde 1: z = 0.05*Target + 0.3*Lembur + c
# Misal untuk input Target=80, Lembur=10:
# R1: z1 = 0.03*80 + 0.1*10 + 0.5 = 2.4 + 1.0 + 0.5 = 3.9
# R2: z2 = 0.04*80 + 0.2*10 + 1.0 = 3.2 + 2.0 + 1.0 = 6.2
# R3: z3 = 0.05*80 + 0.1*10 + 1.5 = 4.0 + 1.0 + 1.5 = 6.5
# R4: z4 = 0.06*80 + 0.3*10 + 2.0 = 4.8 + 3.0 + 2.0 = 9.8
z_sugeno1 = [3.9, 6.2, 6.5, 9.8]
hasil_sugeno1 = hitung_sugeno(alphas_kasus, z_sugeno1)

# C. Tsukamoto
fungsi_tsukamoto = [
    lambda a: invers_monoton_naik(a, 2.0, 10.0),
    lambda a: invers_monoton_naik(a, 2.0, 10.0),
    lambda a: invers_monoton_naik(a, 2.0, 10.0),
    lambda a: invers_monoton_naik(a, 2.0, 10.0),
]
hasil_tsukamoto, z_tsuka_values = hitung_tsukamoto(alphas_kasus, fungsi_tsukamoto)

# Cetak Hasil
print("=" * 65)
print("HASIL KOMPARASI METODE SUGENO DAN TSUKAMOTO")
print("=" * 65)
print(f"1. Sugeno Orde 0       : Rp {hasil_sugeno0:.3f} Juta")
print(f"2. Sugeno Orde 1       : Rp {hasil_sugeno1:.3f} Juta")
print(f"3. Tsukamoto           : Rp {hasil_tsukamoto:.3f} Juta (z_rules: {[round(z, 2) for z in z_tsuka_values]})")
print("=" * 65)
