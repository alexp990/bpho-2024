print("Loading libraries...")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
print("Loaded libraries")

def projectile_motion(g, X, Y, step, h):
    u_min = np.sqrt(g) * np.sqrt(Y + np.sqrt(X**2 + Y**2)) 
    print(f"Minimum starting force u is {u_min}N")

    user_u = float(input(f"Enter your desired starting force u (must be above {u_min}N): "))

    a_m = g / (2 * u_min**2) * X**2
    b_m = -1 * X
    c_m = Y - h + (g * X**2) / (2 * u_min**2)

    a_u = g / (2 * user_u**2) * X**2
    b_u = -1 * X
    c_u = Y - h + (g * X**2) / (2 * user_u**2)

    theta_rad_min_u = np.arctan((-b_m + np.sqrt(b_m**2 - 4*a_m*c_m)) / (2*a_m)) 
    theta_deg_min_u = np.rad2deg(theta_rad_min_u)
    print(f"Minimum u theta is {theta_deg_min_u} degrees") 

    theta_rad_user_u_high = np.arctan((-b_u + np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
    theta_deg_user_u_high = np.rad2deg(theta_rad_user_u_high)
    print(f"User u theta (high ball) is {theta_deg_user_u_high} degrees") 

    theta_rad_user_u_low = np.arctan((-b_u - np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
    theta_deg_user_u_low = np.rad2deg(theta_rad_user_u_low)
    print(f"User u theta (low ball) is {theta_deg_user_u_low} degrees") 

    alpha = 2*g*h / user_u**2
    theta_rad_max_range = 1 / np.sqrt(2 + alpha)

    range_min_u = u_min**2 / g * (np.sin(theta_rad_min_u) * np.cos(theta_rad_min_u) + np.cos(theta_rad_min_u) * np.sqrt(np.square(np.sin(theta_rad_min_u)) + (2 * g * h) / (np.square(u_min))))

    dx = range_min_u / step

    x_a_min = (u_min**2 / g) * np.sin(theta_rad_min_u) * np.cos(theta_rad_min_u)
    y_a_min = h + (u_min**2 / (2 * g)) * ((np.sin(theta_rad_min_u))**2)

    x_a_high = (user_u**2 / g) * np.sin(theta_rad_user_u_high) * np.cos(theta_rad_user_u_high)
    y_a_high = h + (user_u**2 / (2 * g)) * ((np.sin(theta_rad_user_u_high))**2)

    if theta_deg_user_u_low <= 0:
        y_a_low = h
        x_a_low = 0
    elif h < Y:
        y_a_low = Y
        x_a_low = X
    else:
        y_a_low = h + (user_u**2 / (2 * g)) * ((np.sin(theta_rad_user_u_low))**2)
        x_a_low = (user_u**2 / g) * np.sin(theta_rad_user_u_low) * np.cos(theta_rad_user_u_low)

    x_positions_min_u = [0]
    y_positions_min_u = [h]

    x_positions_user_u_high = [0]
    y_positions_user_u_high = [h]

    x_positions_user_u_low = [0]
    y_positions_user_u_low = [h]

    x_positions_max_range = [0]
    y_positions_max_range = [h]

    x = 0

    while True:
        x += dx
        y_min_u = h + x * np.tan(theta_rad_min_u) - (g / (2 * u_min**2)) * (1 + np.tan(theta_rad_min_u)**2) * x**2
        if y_min_u <= 0:
            break
        x_positions_min_u.append(x)
        y_positions_min_u.append(y_min_u)

    x = 0

    while True:
        x += dx
        y_high = h + x * np.tan(theta_rad_user_u_high) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_high)**2) * x**2
        if y_high <= 0:
            break
        x_positions_user_u_high.append(x)
        y_positions_user_u_high.append(y_high)

    x = 0

    while True:
        x += dx
        y_low = h + x * np.tan(theta_rad_user_u_low) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_low)**2) * x**2
        if y_low <= 0:
            break
        x_positions_user_u_low.append(x)
        y_positions_user_u_low.append(y_low)

    x_positions_bounding = [0]
    y_positions_bounding = [(user_u**2 / (2 * g)) - (g / (2 * user_u**2)) * 0**2]

    x = 0

    while True:
        x += dx
        y_bound = (user_u**2 / (2 * g)) - (g / (2 * user_u**2)) * x**2
        x_positions_bounding.append(x)
        y_positions_bounding.append(y_bound)
        if y_bound <= 0:
            break

    x = 0

    while True:
        x += dx
        y_max_r = h + x * np.tan(theta_rad_max_range) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_max_range)**2) * x**2
        x_positions_max_range.append(x)
        y_positions_max_range.append(y_max_r)
        if y_max_r <= 0:
            break


    return (
        np.array(x_positions_min_u), np.array(y_positions_min_u), x_a_min, y_a_min,
        np.array(x_positions_user_u_high), np.array(y_positions_user_u_high), x_a_high, y_a_high,
        np.array(x_positions_user_u_low), np.array(y_positions_user_u_low), x_a_low, y_a_low,
        np.array(x_positions_bounding), np.array(y_positions_bounding), 
        np.array(x_positions_max_range), np.array(y_positions_max_range),
        user_u, 
        g
    )

"""def toggle_labels(event, text_objects):
    visibility = not text_objects[0].get_visible()
    for text in text_objects:
        text.set_visible(visibility)
    plt.draw()"""

step = 1000  
g = 9.81
h = float(input("Enter starting height in meters"))
X = float(input("Enter the X coordinate of the target point: "))
Y = float(input("Enter the Y coordinate of the target point: "))

x_positions_min_u, y_positions_min_u, x_a_min, y_a_min, x_positions_user_u_high, y_positions_user_u_high, x_a_high, y_a_high, x_positions_user_u_low, y_positions_user_u_low, x_a_low, y_a_low, x_positions_bounding, y_positions_bounding, x_positions_max_range, y_positions_max_range, user_u, g = projectile_motion(g, X, Y, step, h)

fig, ax = plt.subplots()

font = FontProperties()
font.set_family('sans-serif')
font.set_name('Arial')
font.set_size(12)

ax.plot(x_positions_min_u, y_positions_min_u, label='Min U')


ax.plot(x_positions_user_u_high, y_positions_user_u_high, label='High')


ax.plot(x_positions_user_u_low, y_positions_user_u_low, label='Low')


ax.plot(x_positions_bounding, y_positions_bounding, label='Bounding Parabola')

ax.plot(x_positions_max_range, y_positions_max_range, label='Max range')

ax.plot(X, Y, marker='.', label=f'Target {X}, {Y}')


ax.set_title(f'Projectile Motion, user_u={user_u}N,  Target={X}, {Y},  g={g}m/s^2, h={h}m', fontsize=14)
ax.set_xlabel('Horizontal Displacement (m)', fontsize=14)
ax.set_ylabel('Vertical Displacement (m)', fontsize=14)
ax.grid(True, linestyle='--', linewidth=0.5)
ax.legend()


plt.show()
