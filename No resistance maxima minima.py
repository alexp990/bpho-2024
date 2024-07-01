import numpy as np
import matplotlib.pyplot as plt

def r(u, g, theta, t):
    return np.sqrt(u**2 * t**2 - g * t**3 * u * np.sin(theta) + 0.25 * g**2 * t**4)

def compute_t_min(u, g, theta):
    # Calculate t_min value
    discriminant = (9 * u**2 * np.sin(theta)**2) / (4 * g**2) - (2 * u**2) / (g**2)
    if discriminant < 0:
        return None  # If discriminant is negative, return None
    term = np.sqrt(discriminant)
    t2 = (3 * u * np.sin(theta)) / (2 * g) - term
    
    # Return the positive t2
    if t2 > 0:
        return t2
    else:
        return None  

def compute_t_max(u, g, theta):
    # Calculate t_max value
    discriminant = (9 * u**2 * np.sin(theta)**2) / (4 * g**2) - (2 * u**2) / (g**2)
    if discriminant < 0:
        return None  # If discriminant is negative, return None
    term = np.sqrt(discriminant)
    t1 = (3 * u * np.sin(theta)) / (2 * g) + term
    
    # Return the positive t1
    if t1 > 0:
        return t1
    else:
        return None 

def projectile_motion(u, g, theta, t):
    x = u * t * np.cos(theta)
    y = u * t * np.sin(theta) - 0.5 * g * t**2
    return x, y

u = float(input("Enter input velocity u in m/s: "))
g = float(input("Enter g in m/s²: "))
h = 0
dt = 1/1000

theta_degrees = np.arange(45, 90, 5)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

for theta_deg in theta_degrees:
    theta = np.deg2rad(theta_deg)
    range = u**2/g * (np.sin(theta)*np.cos(theta) + np.cos(theta)*np.sqrt(np.square(np.sin(theta)) + (2*g*h)/(np.square(u))))
    tof = range / (u*np.cos(theta))
    ts = np.arange(0, tof, dt)
    range_values = r(u, g, theta, ts)
    
    t_max = compute_t_max(u, g, theta)
    t_min = compute_t_min(u, g, theta)

    if t_max is not None and t_min is not None:
        range_max = r(u, g, theta, t_max) 
        range_min = r(u, g, theta, t_min) 

        ax1.scatter([t_max], [range_max], color='blue', zorder=3, s=15, marker='X')
        ax1.scatter([t_min], [range_min], color='red', zorder=3, s=15, marker='X')

    ax1.plot(ts, range_values, label=f'θ = {theta_deg}°')

ax1.legend()
ax1.set_title("Range vs Time")
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Range (m)')
ax1.grid(True)

for theta_deg in theta_degrees:
    theta = np.deg2rad(theta_deg)
    range = u**2/g * (np.sin(theta)*np.cos(theta) + np.cos(theta)*np.sqrt(np.square(np.sin(theta)) + (2*g*h)/(np.square(u))))
    tof = range / (u*np.cos(theta))
    ts = np.arange(0, tof, dt)

    x_positions = []
    y_positions = []

    for t in ts:
        x, y = projectile_motion(u, g, theta, t)
        x_positions.append(x)
        y_positions.append(y)

    t_max = compute_t_max(u, g, theta)
    t_min = compute_t_min(u, g, theta)

    if t_max is not None and t_min is not None:
        x_max, y_max = projectile_motion(u, g, theta, t_max)
        x_min, y_min = projectile_motion(u, g, theta, t_min)
        ax2.scatter([x_max], [y_max], color='blue', zorder=3, s=15, marker='X')
        ax2.scatter([x_min], [y_min], color='red', zorder=3, s=15, marker='X')

    ax2.plot(x_positions, y_positions, label=f'θ = {theta_deg}°')

ax2.set_title("Displacement")
ax2.set_xlabel('x displacement (m)')
ax2.set_ylabel('y displacement (m)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
