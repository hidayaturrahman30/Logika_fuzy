import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. OPERATOR T-NORM (AND / IRISAN)
# ==========================================================
def tnorm_min(mu_a, mu_b):
    """Zadeh Min: min(A, B)"""
    return np.minimum(mu_a, mu_b)

def tnorm_product(mu_a, mu_b):
    """Algebraic Product: A * B"""
    return mu_a * mu_b

def tnorm_bounded_diff(mu_a, mu_b):
    """Bounded Difference: max(0, A + B - 1)"""
    return np.maximum(0.0, mu_a + mu_b - 1.0)

# ==========================================================
# 2. OPERATOR T-CONORM (OR / GABUNGAN)
# ==========================================================
def tconorm_max(mu_a, mu_b):
    """Zadeh Max: max(A, B)"""
    return np.maximum(mu_a, mu_b)

def tconorm_algebraic_sum(mu_a, mu_b):
    """Algebraic Sum: A + B - (A * B)"""
    return mu_a + mu_b - (mu_a * mu_b)

def tconorm_bounded_sum(mu_a, mu_b):
    """Bounded Sum: min(1, A + B)"""
    return np.minimum(1.0, mu_a + mu_b)

# ==========================================================
# 3. OPERATOR KOMPLEMEN (NOT)
# ==========================================================
def fuzzy_not(mu):
    """Zadeh Complement: 1 - mu"""
    return 1.0 - mu

# ==========================================================
# 4. DEFINISI HIMPUNAN FUZZY
# ==========================================================
x = np.linspace(0, 100, 500)

# Himpunan A: Ketersediaan Bandwidth Cukup — Segitiga [30, 60, 90]
mu_a = np.maximum(0.0,
    np.minimum(
        (x - 30.0) / (60.0 - 30.0),
        (90.0 - x) / (90.0 - 60.0)
    )
)

# Himpunan B: Packet Loss Rendah — Trapesium [40, 55, 75, 95]
mu_b = np.maximum(0.0,
    np.minimum(
        np.minimum((x - 40.0) / (55.0 - 40.0), 1.0),
        np.minimum(1.0, (95.0 - x) / (95.0 - 75.0))
    )
)

# ==========================================================
# 5. PENGUJIAN NILAI TERTENTU
# ==========================================================
def hitung_semua(x_val):
    a = np.interp(x_val, x, mu_a)
    b = np.interp(x_val, x, mu_b)
    return {
        "μA": round(a, 3),
        "μB": round(b, 3),
        "Min": round(tnorm_min(a, b), 3),
        "Product": round(tnorm_product(a, b), 3),
        "Max": round(tconorm_max(a, b), 3),
        "AlgSum": round(tconorm_algebraic_sum(a, b), 3),
        "NotA": round(fuzzy_not(a), 3),
        "NotB": round(fuzzy_not(b), 3)
    }

print("=== Hasil Pengujian ===")
for nilai in [35, 50, 65, 80]:
    res = hitung_semua(nilai)
    print(f"x = {nilai:3d} | μA={res['μA']:.3f} μB={res['μB']:.3f} | "
          f"Min={res['Min']:.3f} Prod={res['Product']:.3f} | "
          f"Max={res['Max']:.3f} Sum={res['AlgSum']:.3f} | "
          f"¬A={res['NotA']:.3f} ¬B={res['NotB']:.3f}")

# ==========================================================
# 6. VISUALISASI
# ==========================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

axes[0,0].plot(x, mu_a, label='A: Bandwidth Cukup', color='#1f77b4', linewidth=2.5)
axes[0,0].plot(x, mu_b, label='B: Packet Loss Rendah', color='#ff7f0e', linewidth=2.5)
axes[0,0].plot(x, fuzzy_not(mu_a), label='¬A (Komplemen)', color='gray', linestyle='--')
axes[0,0].set_title('Himpunan A, B, dan Komplemen')
axes[0,0].set_ylim(-0.05, 1.1)
axes[0,0].grid(True, linestyle=':')
axes[0,0].legend()

axes[0,1].plot(x, tnorm_min(mu_a, mu_b), label='Zadeh Min', color='#2ca02c', linewidth=2.5)
axes[0,1].plot(x, tnorm_product(mu_a, mu_b), label='Algebraic Product', color='#d62728', linestyle='-.')
axes[0,1].plot(x, tnorm_bounded_diff(mu_a, mu_b), label='Bounded Diff', color='#9467bd', linestyle=':')
axes[0,1].set_title('Operasi Intersection (AND)')
axes[0,1].set_ylim(-0.05, 1.1)
axes[0,1].grid(True, linestyle=':')
axes[0,1].legend()

axes[1,0].plot(x, tconorm_max(mu_a, mu_b), label='Zadeh Max', color='#2ca02c', linewidth=2.5)
axes[1,0].plot(x, tconorm_algebraic_sum(mu_a, mu_b), label='Algebraic Sum', color='#d62728', linestyle='-.')
axes[1,0].plot(x, tconorm_bounded_sum(mu_a, mu_b), label='Bounded Sum', color='#9467bd', linestyle=':')
axes[1,0].set_title('Operasi Union (OR)')
axes[1,0].set_ylim(-0.05, 1.1)
axes[1,0].grid(True, linestyle=':')
axes[1,0].legend()

axes[1,1].fill_between(x, tnorm_min(mu_a, mu_b), alpha=0.4, label='A ∩ B (Min)')
axes[1,1].plot(x, tconorm_max(mu_a, mu_b), label='A ∪ B (Max)', linewidth=2)
axes[1,1].plot(x, mu_a, color='#1f77b4', linestyle=':', alpha=0.7)
axes[1,1].plot(x, mu_b, color='#ff7f0e', linestyle=':', alpha=0.7)
axes[1,1].set_title('Irisan vs Gabungan Standar')
axes[1,1].set_ylim(-0.05, 1.1)
axes[1,1].grid(True, linestyle=':')
axes[1,1].legend()

plt.tight_layout()
plt.savefig('hasil_operasi_fuzzy.png', dpi=300)
plt.show()
