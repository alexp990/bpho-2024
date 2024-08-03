import numpy as np
import matplotlib.pyplot as plt

class Tasks:

    #----------------------------Exact Model------------------------

    def task1(self, h, u, theta, dt, g):

        theta_rad = np.radians(theta)

        u_x = u * np.cos(theta_rad)
        u_y = u * np.sin(theta_rad)

        x_positions = [0]
        y_positions = [h]
        x_velocities = []
        y_velocities = []
        vc = [0]
        t = 0
        time = [0]

        while True:
            t += dt
            x = u_x * t
            y = h + u_y * t - 0.5 * g * np.square(t)
            vx = u_x
            vy = u_y - g * t
            v = np.sqrt(vx**2 + vy**2)

            x_positions.append(x)
            y_positions.append(y)
            x_velocities.append(vx)
            y_velocities.append(vy)
            vc.append(v)
            time.append(t)
            
            if y <= 0:
                break

        return x_positions, y_positions

    #----------------------------Analytical Model------------------------

    def task2(self, h, u, theta, step, g):

        theta_rad = np.deg2rad(theta)
        range = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
        tof = range / (u * np.cos(theta_rad))
        dx = range / step

        x_a = (u**2 / g) * np.sin(theta_rad)*np.cos(theta_rad)
        y_a = h + (u**2 / (2 * g)) * ((np.sin(theta_rad))**2)

        x_positions = [0]
        y_positions = [h]

        x = 0

        while True:
            x = x + dx

            y = h + x*np.tan(theta_rad) - (g / (2 * u ** 2)) * (1 + np.tan(theta_rad) ** 2) * x ** 2

            x_positions.append(x)
            y_positions.append(y)

            if y <= 0:
                break

        
        
        return np.array(x_positions), np.array(y_positions), x_a, y_a, tof, range

    #----------------------------To XY------------------------

    def task3(self, h, user_u, step, g, X, Y):

        u_min = np.sqrt(g) * np.sqrt(Y + np.sqrt(X**2 + Y**2)) 

        a_m = g / (2 * u_min**2) * X**2
        b_m = -1 * X
        c_m = Y - h + (g * X**2) / (2 * u_min**2)

        a_u = g / (2 * user_u**2) * X**2
        b_u = -1 * X
        c_u = Y - h + (g * X**2) / (2 * user_u**2)

        theta_rad_min_u = np.arctan((-b_m + np.sqrt(b_m**2 - 4*a_m*c_m)) / (2*a_m)) 
        theta_deg_min_u = np.rad2deg(theta_rad_min_u)

        theta_rad_user_u_high = np.arctan((-b_u + np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
        theta_deg_user_u_high = np.rad2deg(theta_rad_user_u_high)

        theta_rad_user_u_low = np.arctan((-b_u - np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
        theta_deg_user_u_low = np.rad2deg(theta_rad_user_u_low)

        range_min_u = u_min**2 / g * (np.sin(theta_rad_min_u) * np.cos(theta_rad_min_u) + np.cos(theta_rad_min_u) * np.sqrt(np.square(np.sin(theta_rad_min_u)) + (2 * g * h) / (np.square(u_min))))

        dx = range_min_u / step

        x_positions_min_u = [0]
        y_positions_min_u = [h]

        x_positions_user_u_high = [0]
        y_positions_user_u_high = [h]

        x_positions_user_u_low = [0]
        y_positions_user_u_low = [h]

        x = 0

        while True:
            x += dx
            y_min_u = h + x * np.tan(theta_rad_min_u) - (g / (2 * u_min**2)) * (1 + np.tan(theta_rad_min_u)**2) * x**2
            if y_min_u <= 0:
                break
            x_positions_min_u.append(x)
            y_positions_min_u.append(y_min_u)

        x = 0

        if user_u > u_min:
            while True:
                x += dx
                y_high = h + x * np.tan(theta_rad_user_u_high) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_high)**2) * x**2
                if y_high <= 0:
                    break
                x_positions_user_u_high.append(x)
                y_positions_user_u_high.append(y_high)

        x = 0

        if user_u > u_min:
            while True:
                x += dx
                y_low = h + x * np.tan(theta_rad_user_u_low) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_low)**2) * x**2
                if y_low <= 0:
                    break
                x_positions_user_u_low.append(x)
                y_positions_user_u_low.append(y_low)

        return (
            u_min,
            theta_deg_min_u,
            theta_deg_user_u_high,
            theta_deg_user_u_low,
            range_min_u ,
            x_positions_min_u, y_positions_min_u,
            x_positions_user_u_high, y_positions_user_u_high,
            x_positions_user_u_low, y_positions_user_u_low           
        )


    #----------------------------Bounding Parabola to XY------------------------

    def task5(self, h, user_u, step, g, X, Y):

        u_min = np.sqrt(g) * np.sqrt(Y + np.sqrt(X**2 + Y**2)) 

        a_m = g / (2 * u_min**2) * X**2
        b_m = -1 * X
        c_m = Y - h + (g * X**2) / (2 * u_min**2)

        a_u = g / (2 * user_u**2) * X**2
        b_u = -1 * X
        c_u = Y - h + (g * X**2) / (2 * user_u**2)

        theta_rad_min_u = np.arctan((-b_m + np.sqrt(b_m**2 - 4*a_m*c_m)) / (2*a_m)) 
        theta_deg_min_u = np.rad2deg(theta_rad_min_u)

        theta_rad_user_u_high = np.arctan((-b_u + np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
        theta_deg_user_u_high = np.rad2deg(theta_rad_user_u_high)

        theta_rad_user_u_low = np.arctan((-b_u - np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
        theta_deg_user_u_low = np.rad2deg(theta_rad_user_u_low)

        alpha = 2*g*h / user_u**2
        theta_rad_max_range = 1 / np.sqrt(2 + alpha)
        theta_deg_max_range = np.rad2deg(theta_rad_max_range)

        range_min_u = u_min**2 / g * (np.sin(theta_rad_min_u) * np.cos(theta_rad_min_u) + np.cos(theta_rad_min_u) * np.sqrt(np.square(np.sin(theta_rad_min_u)) + (2 * g * h) / (np.square(u_min))))

        dx = range_min_u / step

        x_positions_min_u = [0]
        y_positions_min_u = [h]

        x_positions_user_u_high = [0]
        y_positions_user_u_high = [h]

        x_positions_user_u_low = [0]
        y_positions_user_u_low = [h]

        x_positions_bounding = [0]
        y_positions_bounding = [((user_u**2 / (2 * g)) - (g / (2 * user_u**2)) * 0**2) + h]

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
        if user_u > u_min:
            while True:
                x += dx
                y_high = h + x * np.tan(theta_rad_user_u_high) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_high)**2) * x**2
                if y_high <= 0:
                    break
                x_positions_user_u_high.append(x)
                y_positions_user_u_high.append(y_high)

        x = 0
        if user_u > u_min:
            while True:
                x += dx
                y_bound = (user_u**2 / (2 * g)) - (g / (2 * user_u**2)) * x**2
                x_positions_bounding.append(x)
                y_positions_bounding.append(y_bound + h)
                if y_bound + h <= 0:
                    break

        x = 0
        if user_u > u_min:
            while True:
                x += dx
                y_low = h + x * np.tan(theta_rad_user_u_low) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_low)**2) * x**2
                if y_low <= 0:
                    break
                x_positions_user_u_low.append(x)
                y_positions_user_u_low.append(y_low)

        x = 0

        while True:
            x += dx
            y_max_r = h + x * np.tan(theta_rad_max_range) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_max_range)**2) * x**2
            x_positions_max_range.append(x)
            y_positions_max_range.append(y_max_r)
            if y_max_r <= 0:
                break

        return (
            u_min,
            theta_deg_min_u,
            theta_deg_user_u_high,
            theta_deg_user_u_low,
            theta_deg_max_range,
            range_min_u ,
            x_positions_min_u, y_positions_min_u,
            x_positions_user_u_high, y_positions_user_u_high,
            x_positions_user_u_low, y_positions_user_u_low,
            x_positions_bounding, y_positions_bounding,
            x_positions_max_range, y_positions_max_range           
        )
    
    #----------------------------Min Max Range Graph------------------------
       
    class Task7:

        def r(self, u, theta, g, t):
            return np.sqrt(u**2 * t**2 - g * t**3 * u * np.sin(theta) + 0.25 * g**2 * t**4)

        def compute_t_max(self, u, theta, g):
            discriminant = (9 * u**2 * np.sin(theta)**2) / (4 * g**2) - (2 * u**2) / (g**2)
            if discriminant < 0:
                return None
            term = np.sqrt(discriminant)
            t2 = (3 * u * np.sin(theta)) / (2 * g) - term
            if t2 > 0:
                return t2
            else:
                return None  

        def compute_t_min(self, u, theta, g):
            discriminant = (9 * u**2 * np.sin(theta)**2) / (4 * g**2) - (2 * u**2) / (g**2)
            if discriminant < 0:
                return None
            term = np.sqrt(discriminant)
            t1 = (3 * u * np.sin(theta)) / (2 * g) + term
            if t1 > 0:
                return t1
            else:
                return None 

        def projectile_motion(self, u, theta, g, t):
            x = u * t * np.cos(theta)
            y = u * t * np.sin(theta) - 0.5 * g * t**2
            return x, y


    #----------------------------Verlet Trajectory Solver------------------------

    def task8(self, h, u, theta, dt, g, N, C):
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
    
    #----------------------------Air Resistance and No Air Resistance------------------------
    
    class Task9:

        def __init__(self, g, dt):
            self.g = g
            self.dt = dt

        def k_factor(self, C_d, rho, cs_area, m):
            return (0.5 * C_d * rho * cs_area) / m

        def with_air_resistance(self, v0, h, C_d, rho, cs_area, m, angle):

            theta = np.deg2rad(angle)

            k = self.k_factor(C_d, rho, cs_area, m)
            vx0 = v0 * np.cos(np.radians(angle))
            vy0 = v0 * np.sin(np.radians(angle))
            x, y, vx, vy, t = [0], [h], [vx0], [vy0], [0]
            dt = self.dt

            while y[-1] >= 0:
                t.append(t[-1] + dt)
                v = np.sqrt(vx[-1]**2 + vy[-1]**2)

                ax = - (vx[-1] / v) * k * v**2
                ay = -self.g - (vy[-1] / v) * k * v**2

                x.append(x[-1] + vx[-1] * dt + 0.5 * ax * dt**2)
                y.append(y[-1] + vy[-1] * dt + 0.5 * ay * dt**2)

                vx.append(vx[-1] + ax * dt)
                vy.append(vy[-1] + ay * dt)

            return x, y, v, vx, vy, t

        def without_air_resistance(self, v0, h, angle):
            theta = np.radians(angle) 
            vx0 = v0 * np.cos(theta)
            vy0 = v0 * np.sin(theta)
            
            x, y, v, vx, vy, t = [0], [h], [v0], [vx0], [vy0], [0]

            while y[-1] >= 0:

                t.append(t[-1] + self.dt)

                x.append(vx[-1] * t[-1])
                y.append(h + vy[-1] * t[-1] - 0.5 * self.g * t[-1]**2)

                vx.append(vx0)
                vy.append(vy0 - self.g * t[-1])

                v.append(np.sqrt(vx[-1]**2 + vy[-1]**2))

            return x, y, v, vx, vy, t        
