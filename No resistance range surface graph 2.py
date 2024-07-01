print("loading libraries...")
import numpy as np
import matplotlib.pyplot as plt
print("loaded libraries")

def projectile_motion(h, u, theta, g=9.81):
    theta_rad = np.deg2rad(theta)
    
    range_ = u**2/g * (np.sin(2*theta_rad) + np.sqrt(np.sin(theta_rad)**2 + 2*g*h/u**2))
    apogee = h + (u**2 * np.sin(theta_rad)**2) / (2*g)
    
    return range_, apogee


u_values = np.linspace(5, 50, 1000)  # Initial velocities from 5 to 50 m/s
h_values = np.linspace(0, 50, 1000)  # Initial heights from 0 to 100 m


U, H = np.meshgrid(u_values, h_values)


ranges = np.zeros_like(U)
apogees = np.zeros_like(U)


theta = 45  

for i in range(U.shape[0]):
    for j in range(U.shape[1 ]):
        ranges[i, j], apogees[i, j] = projectile_motion(H[i, j], U[i, j], theta)

plt.figure(figsize=(14, 6))

# Heatmap for range
plt.subplot(1, 2, 1)
plt.contourf(U, H, ranges, cmap='viridis')
plt.colorbar(label='Range (m)')
plt.title('Range Heatmap')
plt.xlabel('Initial Velocity (m/s)')
plt.ylabel('Initial Height (m)')

# Heatmap for Apogee
plt.subplot(1, 2, 2)
plt.contourf(U, H, apogees, cmap='viridis')
plt.colorbar(label='Apogee (m)')
plt.title('Apogee Heatmap')
plt.xlabel('Initial Velocity (m/s)')
plt.ylabel('Initial Height (m)')

plt.tight_layout()
plt.show()
