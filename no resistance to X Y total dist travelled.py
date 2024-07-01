print("Loading lobraries...")
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

    def range_func(theta_rad, u):
        range = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
        return range

    
    theta_rad_min_u = np.arctan((-b_m + np.sqrt(b_m**2 - 4*a_m*c_m)) / (2*a_m))
    theta_deg_min_u = np.rad2deg(theta_rad_min_u)
    range_min_u = range_func(theta_rad_min_u, u_min)
    print(range_min_u)
    print(f"Minimum u theta is {theta_deg_min_u} degrees")

    theta_rad_user_u_high = np.arctan((-b_u + np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u))
    theta_deg_user_u_high = np.rad2deg(theta_rad_user_u_high)
    range_high = range_func(theta_rad_user_u_high, user_u)
    print(range_high)
    print(f"User u theta (high ball) is {theta_deg_user_u_high} degrees")

    theta_rad_user_u_low = np.arctan((-b_u - np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u))
    theta_deg_user_u_low = np.rad2deg(theta_rad_user_u_low)
    range_low = range_func(theta_rad_user_u_low, user_u)
    print(range_low)
    print(f"User u theta (low ball) is {theta_deg_user_u_low} degrees")

    dx = X / step

    def trajectory_length(u, theta, range, g=9.81):

        def z_func(z):
            return 0.5 * np.log(np.abs(np.sqrt(1 + z**2) + z)) + 0.5 * z * np.sqrt(1 + z**2)
        
        tan_theta = np.tan(theta)
        z1 = tan_theta
        z2 = tan_theta - (g*range / u**2)*(1 + tan_theta**2)
        
        a = (u**2) / (g * (1 + tan_theta**2))
        s = a * (z_func(z1) - z_func(z2))
    
        return s

    x_positions_min_u = [0]
    y_positions_min_u = [h]

    x_positions_user_u_high = [0]
    y_positions_user_u_high = [h]

    x_positions_user_u_low = [0]
    y_positions_user_u_low = [h]


    # Min U
    x = 0
    while True:
        x += dx
        y_min_u = h + x * np.tan(theta_rad_min_u) - (g / (2 * u_min**2)) * (1 + np.tan(theta_rad_min_u)**2) * x**2
        if y_min_u <= 0:
            break
        x_positions_min_u.append(x)
        y_positions_min_u.append(y_min_u)

    s_min = trajectory_length(u_min, theta_rad_min_u, range_min_u)

    

    # High U
    x = 0
    while True:
        x += dx
        y_high = h + x * np.tan(theta_rad_user_u_high) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_high)**2) * x**2
        if y_high <= 0:
            break
        x_positions_user_u_high.append(x)
        y_positions_user_u_high.append(y_high)

    s_high = trajectory_length(user_u, theta_rad_user_u_high, range_high)

    # Low U
    x = 0
    while True:
        x += dx
        y_low = h + x * np.tan(theta_rad_user_u_low) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_low)**2) * x**2
        if y_low <= 0:
            break
        x_positions_user_u_low.append(x)
        y_positions_user_u_low.append(y_low)

    s_low = trajectory_length(user_u, theta_rad_user_u_low, range_low)

    return (
        np.array(x_positions_min_u), np.array(y_positions_min_u), 
        np.array(x_positions_user_u_high), np.array(y_positions_user_u_high),
        np.array(x_positions_user_u_low), np.array(y_positions_user_u_low),
        s_min, s_high, s_low
    )

step = 1000 
g = 9.81
h = float(input("Enter starting height in meters: "))
X = float(input("Enter the X coordinate of the target point: "))
Y = float(input("Enter the Y coordinate of the target point: "))

x_positions_min_u, y_positions_min_u, x_positions_user_u_high, y_positions_user_u_high, x_positions_user_u_low, y_positions_user_u_low, s_min, s_high, s_low  = projectile_motion(g, X, Y, step, h)

fig, ax = plt.subplots()

font = FontProperties()
font.set_family('sans-serif')
font.set_name('Arial')
font.set_size(12)

ax.plot(x_positions_min_u, y_positions_min_u, label='Min U')
ax.plot(x_positions_user_u_high, y_positions_user_u_high, label='High')
ax.plot(x_positions_user_u_low, y_positions_user_u_low, label='Low')

ax.plot(X, Y, marker='.', label=f'Target {X}, {Y}')

ax.set_title(f'Target={X},{Y}, g={g}m/s^2, h={h}m', fontsize=14)
ax.set_xlabel('Horizontal Displacement (m)', fontsize=14)
ax.set_ylabel('Vertical Displacement (m)', fontsize=14)
ax.grid(True, linestyle='--', linewidth=0.5)
ax.legend()

print(f"Minimum U distance travelled is {int(s_min)}m")
print(f"High ball distance travelled is {int(s_high)}m")
print(f"High ball distance travelled is {int(s_low)}m")

plt.show()
