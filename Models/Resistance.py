import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

def k_factor(C_d, rho, cs_area, m):
    return ((0.5 * C_d * rho * cs_area) / m)

def with_air_resistance(v0, h, C_d, rho, cs_area, m, angle):

    theta = np.deg2rad(angle)

    k = k_factor(C_d, rho, cs_area, m)
    print(k)
    vx0 = v0 * np.cos(np.radians(angle))
    vy0 = v0 * np.sin(np.radians(angle))
    x, y, vx, vy, t = [0], [h], [vx0], [vy0], [0]
    dt = 1/1000

    while y[-1] >= 0:
        t.append(t[-1] + dt)
        v = np.sqrt(vx[-1]**2 + vy[-1]**2)

        ax = -(vx[-1] / v) * k * v**2
        ay = -g - (vy[-1] / v) * k * v**2

        x.append(x[-1] + vx[-1] * dt + 0.5 * ax * dt**2)
        y.append(y[-1] + vy[-1] * dt + 0.5 * ay * dt**2)

        vx.append(vx[-1] + ax * dt)
        vy.append(vy[-1] + ay * dt)

    return x, y, v, vx, vy, t

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

    return x, y, v, vx, vy, t
   
g = 9.81  # acceleration due to gravity (m/s^2)
C_d = 0.1  # Drag coefficient
rho = 1  # Air density (kg/m^3)
cs_area = 0.007854  # Cross-sectional area (m^2)
m = 0.1  # Object mass (kg)
dt = 0.01  # Time step (s)
v0 = 20  # Initial speed (m/s)
angle = 30  # Launch angle (deg)
h = 2 #Initial height

xnr, ynr, vnr, vxnr, vynr, tnr  = without_air_resistance(v0, h, angle)
xr, yr, vr, vxr, vyr, tr = with_air_resistance(v0, h, C_d, rho, cs_area, m, angle)


fig, ax = plt.subplots(2, 2, figsize=(15, 10))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# XY Plot
ax[0, 0].plot(xnr, ynr, label='No air R', linestyle='-', color='blue')
ax[0, 0].plot(xr, yr, label='Air R', linestyle='--', color='red')
ax[0, 0].set_xlabel('Distance (m)')
ax[0, 0].set_ylabel('Height (m)')
ax[0, 0].set_title('X vs Y')
ax[0, 0].legend()
ax[0, 0].grid(True)

# TY Plot
ax[0, 1].plot(tnr, ynr, label='No air R', linestyle='-', color='blue')
ax[0, 1].plot(tr, yr, label='Air R', linestyle='--', color='red')
ax[0, 1].set_xlabel('Time (s)')
ax[0, 1].set_ylabel('Height (m)')
ax[0, 1].set_title('Y vs T')
ax[0, 1].legend()
ax[0, 1].grid(True)

# TVX Plot
ax[1, 0].plot(tnr, vxnr, label='No air R', linestyle='-', color='blue')
ax[1, 0].plot(tr, vxr, label='Air R', linestyle='--', color='red')
ax[1, 0].set_xlabel('Time (s)')
ax[1, 0].set_ylabel('Velocity in X (m/s)')
ax[1, 0].set_title('VX vs T')
ax[1, 0].legend()
ax[1, 0].grid(True)

# TVY Plot
ax[1, 1].plot(tnr, vynr, label='No air R', linestyle='-', color='blue')
ax[1, 1].plot(tr, vyr, label='Air R', linestyle='--', color='red')
ax[1, 1].set_xlabel('Time (s)')
ax[1, 1].set_ylabel('Velocity in Y (m/s)')
ax[1, 1].set_title('VY vs T')
ax[1, 1].legend()
ax[1, 1].grid(True)

plt.show()
