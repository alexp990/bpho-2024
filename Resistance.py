import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def k_factor(C_d, rho, cs_area, m):
    return (0.5 * C_d * rho * cs_area) / m

def with_air_resistance(v0, h, C_d, rho, cs_area, m, angle):

    theta = np.deg2rad(angle)

    k = k_factor(C_d, rho, cs_area, m)
    vx0 = v0 * np.cos(np.radians(angle))
    vy0 = v0 * np.sin(np.radians(angle))
    x, y, vx, vy, t = [0], [h], [vx0], [vy0], [0]
    dt = 1/1000

    while y[-1] >= 0:
        t.append(t[-1] + dt)
        v = np.sqrt(vx[-1]**2 + vy[-1]**2)

        ax = - (vx[-1] / v) * k * v**2
        ay = -g - (vy[-1] / v) * k * v**2

        x.append(x[-1] + vx[-1] * dt + 0.5 * ax * dt**2)
        y.append(y[-1] + vy[-1] * dt + 0.5 * ay * dt**2)

        vx.append(vx[-1] + ax * dt)
        vy.append(vy[-1] + ay * dt)

    return x, y#, vx, vy, t

def without_air_resistance(v0, h, angle):
    theta = np.radians(angle) 
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)
    
    x, y, v, vx, vy, t = [0], [h], [v0], [vx0], [vy0], [0]

    while y[-1] >= 0:

        t.append(t[-1] + dt)

        x.append(vx[-1] * t[-1])
        y.append(h + vy[-1] * t[-1] - 0.5 * g * t[-1]**2)

        vx.append(vx0)
        vy.append(vy0 - g * t[-1])

        v.append(np.sqrt(vx[-1]**2 + vy[-1]**2))

    return x, y#, v, vx, vy, t
   
g = 9.81  # acceleration due to gravity (m/s^2)
C_d = 0.1  # Drag coefficient
rho = 1  # Air density (kg/m^3)
cs_area = 0.007854  # Cross-sectional area (m^2)
m = 0.1  # Object mass (kg)
dt = 0.01  # Time step (s)
v0 = 20  # Initial speed (m/s)
angle = 30  # Launch angle (degrees)
h = 2

x_no_air, y_no_air = without_air_resistance(v0, h, angle)
x_with_air, y_with_air = with_air_resistance(v0, h, C_d, rho, cs_area, m, angle)

plt.figure(figsize=(10, 6))
plt.plot(x_no_air, y_no_air, label='Without Air Resistance')
plt.plot(x_with_air, y_with_air, label='With Air Resistance')
plt.title('Projectile Trajectories with and without Air Resistance')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.legend()
plt.grid(True)
plt.show()






        





