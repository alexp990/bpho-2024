import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(h, u, theta, dt, g=9.81):

    theta = np.radians(theta) 
    u_x = u * np.cos(theta)
    u_y = u * np.sin(theta)
    
    x_positions = [0]
    y_positions = [h]
    
    t = 0
    while True:
        t += dt
        x = u_x * t
        y = h + u_y*t - 0.5*g*np.square(t)

        
        if y < 0:
            break  
        
        x_positions.append(x)
        y_positions.append(y)
    
    return np.array(x_positions), np.array(y_positions)


u = 30  # Initial velocity in m/s
theta =30  # Launch angle in degrees
dt = 0.01  # Time step in seconds
h = 10 #Initial height

x_positions, y_positions = projectile_motion(h, u, theta, dt)


plt.plot(x_positions, y_positions)
plt.title('Projectile Motion')
plt.xlabel('Horizontal Displacement (m)')
plt.ylabel('Vertical Displacement (m)')
plt.grid(True)
plt.show()
