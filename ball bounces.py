import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def verlet_trajectory_solver(N, C, g, dt, h, theta, u):
    theta = np.deg2rad(theta)
    
  
    nbounce = 0
    t = [0.0]
    x = [0.0]
    y = [h]
    vx = [u * np.cos(theta)]
    vy = [u * np.sin(theta)]
    
    while nbounce <= N:
        ax = 0.0
        ay = -g
        
        x_new = x[-1] + vx[-1] * dt + 0.5 * ax * dt**2
        y_new = y[-1] + vy[-1] * dt + 0.5 * ay * dt**2
        
        x.append(x_new)
        y.append(y_new)
        
        aax = 0.0
        aay = -g
        
        vx_new = vx[-1] + 0.5 * (ax + aax) * dt
        vy_new = vy[-1] + 0.5 * (ay + aay) * dt
        
        vx.append(vx_new)
        vy.append(vy_new)
        
        t.append(t[-1] + dt)
        
        if y[-1] < 0:
            y[-1] = 0.0
            vy[-1] = -C * vy[-1]
            nbounce += 1
    
    t = np.array(t)
    x = np.array(x)
    y = np.array(y)
    vx = np.array(vx)
    vy = np.array(vy)
    
    return t, x, y, vx, vy

h = 10.0   # Initial height (m)
N = 10     # Maximum number of bounces
C = 0.8    # Coefficient of restitution
g = 9.81   # Acceleration due to gravity (m/s^2)
dt = 1/25  # Time step (s)
theta = 45.0  # Initial launch angle in degrees
u = 20.0   # Initial speed of object in m/s

t, x, y, vx, vy = verlet_trajectory_solver(N, C, g, dt, h, theta, u)

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, np.max(x) * 1.1)
ax.set_ylim(0, np.max(y) * 1.1)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.set_title('Projectile Trajectory Animation with Bounces (Verlet Method)')

line, = ax.plot([], [], '.', lw=0.1)

def update(frame):
    line.set_data(x[:frame], y[:frame])
    return line,

ani = FuncAnimation(fig, update, frames=len(t), interval=1, blit=True)

plt.show()
