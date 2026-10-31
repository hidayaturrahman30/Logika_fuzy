import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Grid input
x1_range = np.linspace(0, 10, 30)
x2_range = np.linspace(0, 100, 30)
X1, X2 = np.meshgrid(x1_range, x2_range)
Z_out = np.zeros_like(X1)

# Hitung output inferensi untuk setiap titik grid (X1[i, j], X2[i, j])
for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        Z_out[i, j] = evaluasi_sistem_fuzzy(X1[i, j], X2[i, j])

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X1, X2, Z_out, cmap='viridis', edgecolor='none', alpha=0.9)
ax.set_xlabel('Input 1')
ax.set_ylabel('Input 2')
ax.set_zlabel('Output Keputusan')
ax.set_title('Decision Surface Plot Sistem Fuzzy', fontweight='bold')
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig('decision_surface.png', dpi=300)
plt.show()
