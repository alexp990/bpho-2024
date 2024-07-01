import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

g = 9.81  # acceleration due to gravity (m/s^2)
C_d = 0.47  # Drag coefficient
rho = 1.225  # Air density (kg/m^3)
cs_area = 0.014  # Cross-sectional area (m^2)
m = 0.5  # Object mass (kg)
dt = 0.01  # Time step (s)
v0 = 100.0  # Initial speed (m/s)
angle = 45.0  # Launch angle (degrees)

def air_resistance_factor(C_d, rho, cs_area, m):
    return (0.5 * C_d * rho * cs_area) / m

def update_plot(val):
    k = air_resistance_factor(slider_C_d.val, rho, slider_cs_area.val, slider_mass.val)
    v0 = slider_v0.val
    angle = slider_angle.val
    

    vx0 = v0 * np.cos(np.radians(angle))
    vy0 = v0 * np.sin(np.radians(angle))
    
    x, y, vx, vy, t = [x0], [y0], [vx0], [vy0], [0]
    
    # Simulation loop
    while y[-1] >= 0:
        v = np.sqrt(vx[-1]**2 + vy[-1]**2)
        ax_val = - (vx[-1] / v) * k * v**2
        ay_val = -g - (vy[-1] / v) * k * v**2
        
        xn = x[-1] + vx[-1] * dt + 0.5 * ax_val * dt**2
        yn = y[-1] + vy[-1] * dt + 0.5 * ay_val * dt**2
        
        vxn = vx[-1] + ax_val * dt
        vyn = vy[-1] + ay_val * dt
        
        x.append(xn)
        y.append(yn)
        vx.append(vxn)
        vy.append(vyn)
        t.append(t[-1] + dt)
    
    ax.clear()
    ax.plot(x, y)
    ax.set_title('Projectile Motion with Air Resistance')
    ax.set_xlabel('Horizontal Displacement (m)')
    ax.set_ylabel('Vertical Displacement (m)')
    ax.grid(True)
    fig.canvas.draw_idle()

x0 = 0.0  # initial x position (m)
y0 = 0.0  # initial y position (m)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)

ax_v0 = plt.axes([0.1, 0.25, 0.8, 0.03])
ax_angle = plt.axes([0.1, 0.20, 0.8, 0.03])
ax_C_d = plt.axes([0.1, 0.15, 0.8, 0.03])
ax_cs_area = plt.axes([0.1, 0.10, 0.8, 0.03])
ax_mass = plt.axes([0.1, 0.05, 0.8, 0.03])

slider_v0 = Slider(ax_v0, 'Initial Speed (v0)', 10, 200, valinit=v0)
slider_angle = Slider(ax_angle, 'Launch Angle', 0, 90, valinit=angle)
slider_C_d = Slider(ax_C_d, 'Drag Coefficient (C_d)', 0.1, 1.0, valinit=C_d)
slider_cs_area = Slider(ax_cs_area, 'Cross Sectional Area (cs_area)', 0.001, 0.05, valinit=cs_area)
slider_mass = Slider(ax_mass, 'Mass (m)', 0.1, 10, valinit=m)

slider_v0.on_changed(update_plot)
slider_angle.on_changed(update_plot)
slider_C_d.on_changed(update_plot)
slider_cs_area.on_changed(update_plot)
slider_mass.on_changed(update_plot)

update_plot(0)

plt.show()
