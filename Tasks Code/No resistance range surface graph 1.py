import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(h, u, g=9.81):
    theta_max_range = np.arcsin(1 / np.sqrt(2 + (2 * g * h) / u**2))
    max_range = (u**2 / g) * (1 + np.sqrt(1 + 2 * g * h / u**2))
    max_height = h + (u * np.sin(theta_max_range))**2 / (2 * g)
    return max_range, np.rad2deg(theta_max_range), max_height

def Rg_u2(theta, alpha):
    theta_rad = np.radians(theta)
    return np.sin(theta_rad) * np.cos(theta_rad) + np.cos(theta_rad) * np.sqrt(np.sin(theta_rad)**2 + alpha)

u_values = np.linspace(1, 50, 1000)
h_values = np.linspace(0, 50, 1000)
theta_values = np.linspace(0, 90, 500)
alpha_values = range(11)

max_range = np.zeros((len(h_values), len(u_values)))
launch_elevation = np.zeros((len(h_values), len(u_values)))
Rg_u2_values = np.zeros((len(h_values), len(u_values)))

for i, u in enumerate(u_values):
    for j, h in enumerate(h_values):
        R, theta, H = projectile_motion(h, u)
        max_range[j, i] = R
        launch_elevation[j, i] = theta
        Rg_u2_values[j, i] = R * 9.81 / u**2

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

#Max range heatmap
im1 = axs[0, 0].imshow(max_range, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
axs[0, 0].set_title('Max Range (m)')
axs[0, 0].set_xlabel('Initial Velocity u (m/s)')
axs[0, 0].set_ylabel('Initial Height h (m)')
fig.colorbar(im1, ax=axs[0, 0])
axs[0, 0].text(0.05, 0.95, r'$R = \frac{u^2}{g} + \sqrt{1 + \frac{2gh}{u^2}}$', 
                transform=axs[0, 0].transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

#Theta heatmap
im2 = axs[0, 1].imshow(launch_elevation, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo')
axs[0, 1].set_title('Theta (degrees)')
axs[0, 1].set_xlabel('Initial Velocity u (m/s)')
axs[0, 1].set_ylabel('Initial Height h (m)')
fig.colorbar(im2, ax=axs[0, 1])
axs[0, 1].text(0.05, 0.95, r'$\theta_{max} = \arcsin \left( \frac{1}{\sqrt{2 + \frac{2gh}{u^2}}} \right)$', 
                transform=axs[0, 1].transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

#Rg/u² heatmap
im3 = axs[1, 1].imshow(Rg_u2_values, extent=[u_values.min(), u_values.max(), h_values.min(), h_values.max()], origin='lower', aspect='auto', cmap='turbo', vmin=0, vmax=10)
axs[1, 1].set_title('Rg/u²')
axs[1, 1].set_xlabel('Initial Velocity u (m/s)')
axs[1, 1].set_ylabel('Initial Height h (m)')
fig.colorbar(im3, ax=axs[1, 1])
axs[1, 1].text(0.05, 0.95, r'$\frac{Rg}{u^2} = \sqrt{1 + \frac{2gh}{u^2}}$', 
                transform=axs[1, 1].transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

#Alpha graph 
for alpha in alpha_values:
    Rg_u2_theta_values = Rg_u2(theta_values, alpha)
    axs[1, 0].plot(theta_values, Rg_u2_theta_values, label=rf'$\alpha$ = {alpha}')
axs[1, 0].set_title('Rg/u² vs Theta')
axs[1, 0].set_xlabel('Theta (degrees)')
axs[1, 0].set_ylabel('Rg/u²')
axs[1, 0].grid(True)
axs[1, 0].legend()
axs[1, 0].text(0.05, 0.95, r'$\frac{Rg}{u^2} = \sin \theta \cos \theta + \cos \theta \sqrt{\sin^2 \theta + \alpha}$', 
                transform=axs[1, 0].transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
axs[1, 0].text(0.05, 0.80, r'$\alpha = \frac{2gh}{u^2}$', 
                transform=axs[1, 0].transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
axs[1, 0].text(0.05, 0.65, r'$\sin \theta_{max} = \frac{1}{\sqrt{2 + \alpha}}$', 
                transform=axs[1, 0].transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
axs[1, 0].annotate('Range has a maximum value\nas theta is varied.',
                    xy=(45, 0.25),
                    fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7),
                    horizontalalignment='center', verticalalignment='center')


plt.tight_layout()
plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()
