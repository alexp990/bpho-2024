import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def projectile_motion(h, u, theta, step, g=9.81):
    theta_rad = np.deg2rad(theta)
    range = (u**2 / g) * (np.sin(2 * theta_rad) + np.sqrt(np.sin(2 * theta_rad)**2 + 2 * g * h / u**2))
    tof = range / (u * np.cos(theta_rad))
    t = np.linspace(0, tof, step)
    x = u * np.cos(theta_rad) * t
    y = h + u * np.sin(theta_rad) * t - 0.5 * g * t**2
    return x, y

def generate_surface(h, u_values, theta_values, step):
    U, Theta = np.meshgrid(u_values, theta_values)
    X, Y = np.meshgrid(np.zeros_like(u_values), np.zeros_like(theta_values))
    for i in range(len(u_values)):
        for j in range(len(theta_values)):
            x, y = projectile_motion(h, u_values[i], theta_values[j], step)
            X[j, i] = x[-1]  
            Y[j, i] = y.max()  
    return U, Theta, X, Y

#Params
h = float(input("Enter initial height of object: ")) 
u_values = np.linspace(1, 100, 50)  
theta_values = np.linspace(0, 90, 50)  
step = 10000  


U, Theta, X, Y = generate_surface(h, u_values, theta_values, step)


fig = plt.figure(figsize=(15, 5))


ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(U, Theta, X, cmap='inferno')
ax1.set_title('Projectile Motion Range')
ax1.set_xlabel('Initial Velocity (m/s)')
ax1.set_ylabel('Launch Angle (degrees)')
ax1.set_zlabel('Range (m)')

ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(U, Theta, Y, cmap='magma')
ax2.set_title('Projectile Motion Maximum Height')
ax2.set_xlabel('Initial Velocity (m/s)')
ax2.set_ylabel('Launch Angle (degrees)')
ax2.set_zlabel('Maximum Height (m)')

plt.tight_layout()
plt.show()
