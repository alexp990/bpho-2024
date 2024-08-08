import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(t, y, rho, C_d, A, m, g):
    x, y, vx, vy = y
    v = np.sqrt(vx**2 + vy**2)
    ax = -0.5 * rho * C_d * A * v * vx / m
    ay = -g - 0.5 * rho * C_d * A * v * vy / m
    return np.array([vx, vy, ax, ay])

def rk4_step(f, y, t, dt, *args):
    k1 = dt * f(t, y, *args)
    k2 = dt * f(t + 0.5 * dt, y + 0.5 * k1, *args)
    k3 = dt * f(t + 0.5 * dt, y + 0.5 * k2, *args)
    k4 = dt * f(t + dt, y + k3, *args)
    return y + (k1 + 2*k2 + 2*k3 + k4) / 6

def trajectory_length(u, theta, rho, C_d, A, m, g=9.81, dt=0.01):
    vx0 = u * np.cos(theta)
    vy0 = u * np.sin(theta)
    y0 = np.array([0, 0, vx0, vy0])
    
    t = 0
    trajectory = [y0[:2]]  
    while y0[1] >= 0: 
        y0 = rk4_step(projectile_motion, y0, t, dt, rho, C_d, A, m, g)
        t += dt
        trajectory.append(y0[:2])
    
    trajectory = np.array(trajectory)

    dx = np.diff(trajectory[:, 0])
    dy = np.diff(trajectory[:, 1])
    ds = np.sqrt(dx**2 + dy**2)
    length = np.sum(ds)
    
    return trajectory, length

def plot_trajectory(trajectory):
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory[:, 0], trajectory[:, 1], label='Trajectory Path')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Vertical Distance (m)')
    plt.title('Projectile Trajectory with Air Resistance')
    plt.grid(True)
    plt.legend()
    plt.show()

u = 50  # initial speed (m/s)
theta = np.pi / 4  # launch angle (radians)
rho = 1.225  # air density (kg/m^3)
C_d = 0.47  # drag coefficient (dimensionless)
A = 0.01  # cross-sectional area (m^2)
m = 0.1  # mass of the projectile (kg)

trajectory, length = trajectory_length(u, theta, rho, C_d, A, m)
print(f"Trajectory length with air resistance: {length:.2f} meters")

plot_trajectory(trajectory)
