import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(h, u, theta, step, g=9.81):

    theta_rad = np.deg2rad(theta)
    range = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
    tof = range / (u * np.cos(theta_rad))
    dx = range / step

    x_a = (u**2 / g) * np.sin(theta_rad)*np.cos(theta_rad)
    y_a = h + (u**2 / (2 * g)) * ((np.sin(theta_rad))**2)

    x_positions = [0]
    y_positions = [h]

    x = 0

    while True:
        x = x + dx

        y = h + x*np.tan(theta_rad) - (g / (2 * u ** 2)) * (1 + np.tan(theta_rad) ** 2) * x ** 2

        x_positions.append(x)
        y_positions.append(y)

        if y <= 0:
            break

    
    
    return np.array(x_positions), np.array(y_positions), x_a, y_a

u = float(input("Enter initial velocity"))  # Initial velocity in m/s
theta = float(input("Enter initial angle in degrees"))  # Launch angle in degrees
step = 1000  
h = float(input("Enter initial height of object")) #Initial Height

x_positions, y_positions, x_a, y_a = projectile_motion(h, u, theta, step)

plt.plot(x_positions, y_positions)
plt.plot(x_a, y_a, marker='.', color='red', markersize=10)
plt.text(x_a, y_a, 'Appogee', fontsize=12, ha='right', va='bottom')
plt.title('Projectile Motion')
plt.xlabel('Horizontal Displacement (m)')
plt.ylabel('Vertical Displacement (m)')
plt.grid(True)
plt.show()
