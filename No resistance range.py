print("Loading libraries...")
import numpy as np
import matplotlib.pyplot as plt
print("loaded libraries")

def projectile_motion(h, u, theta, step, g=9.81):

    theta_rad = np.deg2rad(theta)
    theta_max_rad = np.arcsin(1 / np.sqrt(2 + 2*g*h/u**2))
    theta_max_deg = np.rad2deg(theta_max_rad)
    print(f"The theta for max displacement is {theta_max_deg}degrees")
    range = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
    range_max = u**2/g * (np.sin(theta_max_rad)*np.cos(theta_max_rad) + np.cos(theta_max_rad)*np.sqrt(np.square(np.sin(theta_max_rad)) + (2*g*h)/(np.square(u))))
    tof = range / (u * np.cos(theta_rad))
    dx = range / step

    x_a_u = (u**2 / g) * np.sin(theta_rad)*np.cos(theta_rad)
    y_a_u = h + (u**2 / (2 * g)) * ((np.sin(theta_rad))**2)

    x_a_m = (u**2 / g) * np.sin(theta_rad)*np.cos(theta_rad)
    y_a_m = h + (u**2 / (2 * g)) * ((np.sin(theta_rad))**2)

    x_positions_m = [0]
    y_positions_m = [h]

    x_positions_u = [0]
    y_positions_u = [h]

    x = 0

    while True:
        x = x + dx

        y = h + x*np.tan(theta_rad) - (g / (2 * u ** 2)) * (1 + np.tan(theta_rad) ** 2) * x ** 2
        y_l = h + x*np.tan(theta_max_rad) - (g / (2 * u ** 2)) * (1 + np.tan(theta_max_rad) ** 2) * x ** 2

        x_positions_m.append(x)
        y_positions_m.append(y_l)

        x_positions_u.append(x)
        y_positions_u.append(y)

        if y_l <= 0:
            break

    
    
    return np.array(x_positions_m), np.array(y_positions_m), x_a_m, y_a_m, np.array(x_positions_u), np.array(y_positions_u), x_a_u, y_a_u

u = float(input("Enter initial velocity"))  
theta = float(input("Enter initial angle in degrees"))  
step = 1000 
h = float(input("Enter initial height of object"))

x_positions_m, y_positions_m, x_a_m, y_a_m, x_positions_u, y_positions_u, x_a_u, y_a_u = projectile_motion(h, u, theta, step)


plt.plot(x_positions_m, y_positions_m)
plt.plot(x_a_m, y_a_m, marker='.', color='red', markersize=10)
plt.text(x_a_m, y_a_m, 'Max displacement appogee', fontsize=12, ha='right', va='bottom')

plt.plot(x_positions_u, y_positions_u)
plt.plot(x_a_u, y_a_u, marker='.', color='red', markersize=10)
plt.text(x_a_u, y_a_u, 'User theta displacement appogee', fontsize=12, ha='right', va='bottom')

plt.title('Projectile Motion')
plt.xlabel('Horizontal Displacement (m)')
plt.ylabel('Vertical Displacement (m)')

plt.grid(True)
plt.show()
