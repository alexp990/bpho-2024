import numpy as np
import matplotlib.pyplot as plt

class Tasks:

    #----------------------------Exact Model------------------------

    def task1(self, h, u, theta, dt, g):

        theta_rad = np.radians(theta)

        range_ = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))

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

        return x_positions, y_positions, range_







    #----------------------------Analytical Model------------------------

    def task2(self, h, u, theta, step, g):

        theta_rad = np.deg2rad(theta)
        range_ = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
        tof = range_ / (u * np.cos(theta_rad))
        dx = range_ / step

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
    
    
    def task4(self, h, u, theta, step, g):

        theta_rad = np.deg2rad(theta)
        theta_rad_max_r = np.arcsin(1/(np.sqrt(2 + 2*g*h/u**2)))

        range_ = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
        range_max = (u**2 / g) * (np.sqrt(1 + (2*g*h)/u**2))

        tof = range_ / (u * np.cos(theta_rad))
        dx = range_ / step

        tof_max_r = range_max / (u * np.cos(theta_rad_max_r))
        dx_max_r = range_max / step

        x_a = (u**2 / g) * np.sin(theta_rad)*np.cos(theta_rad)
        y_a = h + (u**2 / (2 * g)) * ((np.sin(theta_rad))**2)

        x_a_max_r = (u**2 / g) * np.sin(theta_rad_max_r)*np.cos(theta_rad_max_r)
        y_a_max_r = h + (u**2 / (2 * g)) * ((np.sin(theta_rad_max_r))**2)

        x_positions = [0]
        y_positions = [h]

        x_positions_max_range = [0]
        y_positions_max_range = [h]

        x = 0

        while True:
            x = x + dx

            y = h + x*np.tan(theta_rad) - (g / (2 * u ** 2)) * (1 + np.tan(theta_rad) ** 2) * x ** 2

            x_positions.append(x)
            y_positions.append(y)

            if y <= 0:
                break

        x = 0

        while True:
            x = x + dx_max_r

            y = h + x*np.tan(theta_rad_max_r) - (g / (2 * u ** 2)) * (1 + np.tan(theta_rad_max_r) ** 2) * x ** 2

            x_positions_max_range.append(x)
            y_positions_max_range.append(y)

            if y <= 0:
                break

        return np.array(x_positions), np.array(y_positions), np.array(x_positions_max_range), np.array(y_positions_max_range), x_a, y_a, x_a_max_r, y_a_max_r, range, range_max, tof, tof_max_r, theta, np.rad2deg(theta_rad_max_r)



    #----------------------------Maximum Range Surface Plots------------------------

    def task4_surface_plots(self):

        def projectile_motion(h, u, g=9.81):
            theta_max_range = np.arcsin(1 / np.sqrt(2 + (2 * g * h) / u**2))
            max_range = (u**2 / g) * (1 + np.sqrt(1 + 2 * g * h / u**2))
            max_height = h + (u * np.sin(theta_max_range))**2 / (2 * g)
            return max_range, np.rad2deg(theta_max_range), max_height

        def Rg_u2(theta, alpha):
            theta_rad = np.radians(theta)
            return np.sin(theta_rad) * np.cos(theta_rad) + np.cos(theta_rad) * np.sqrt(np.sin(theta_rad)**2 + alpha)

        u_values = np.linspace(1, 50, 200)
        h_values = np.linspace(0, 50, 200)
        theta_values = np.linspace(0, 90, 100)
        alpha_values = range(11)
        Rg_u2_theta_values = []

        max_range = np.zeros((len(h_values), len(u_values)))
        launch_elevation = np.zeros((len(h_values), len(u_values)))
        Rg_u2_values = np.zeros((len(h_values), len(u_values)))

        for i, u in enumerate(u_values):
            for j, h in enumerate(h_values):
                R, theta, H = projectile_motion(h, u)
                max_range[j, i] = R
                launch_elevation[j, i] = theta
                Rg_u2_values[j, i] = R * 9.81 / u**2

        for alpha in alpha_values:
            Rg_u2_theta_values.append(Rg_u2(theta_values, alpha))


        return max_range, launch_elevation, Rg_u2_values, alpha_values, h_values, theta_values, u_values, Rg_u2_theta_values, alpha_values







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

        if user_u > u_min:
            theta_rad_user_u_high = np.arctan((-b_u + np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
            theta_deg_user_u_high = np.rad2deg(theta_rad_user_u_high)

            theta_rad_user_u_low = np.arctan((-b_u - np.sqrt(b_u**2 - 4*a_u*c_u)) / (2*a_u)) 
            theta_deg_user_u_low = np.rad2deg(theta_rad_user_u_low)
        else:                  
            theta_rad_user_u_high = np.deg2rad(0)
            theta_deg_user_u_high = 0

            theta_rad_user_u_low = np.deg2rad(0)
            theta_deg_user_u_low = 0


        alpha = 2*g*h / user_u**2
        theta_rad_max_range = 1 / np.sqrt(2 + alpha)
        theta_deg_max_range = np.rad2deg(theta_rad_max_range)

        range_min_u = u_min**2 / g * (np.sin(theta_rad_min_u) * np.cos(theta_rad_min_u) + np.cos(theta_rad_min_u) * np.sqrt(np.square(np.sin(theta_rad_min_u)) + (2 * g * h) / (np.square(u_min))))
        if user_u > u_min:
            range_high = user_u**2 / g * (np.sin(theta_rad_user_u_high) * np.cos(theta_rad_user_u_high) + np.cos(theta_rad_user_u_high) * np.sqrt(np.square(np.sin(theta_rad_user_u_high)) + (2 * g * h) / (np.square(user_u))))
            range_low = user_u**2 / g * (np.sin(theta_rad_user_u_low) * np.cos(theta_rad_user_u_low) + np.cos(theta_rad_user_u_low) * np.sqrt(np.square(np.sin(theta_rad_user_u_low)) + (2 * g * h) / (np.square(user_u))))
        else:
            range_high = 0
            range_low = 0
        range_max = user_u**2 / g * (np.sin(theta_rad_max_range) * np.cos(theta_rad_max_range) + np.cos(theta_rad_max_range) * np.sqrt(np.square(np.sin(theta_rad_max_range)) + (2 * g * h) / (np.square(user_u))))


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
            range_min_u, range_high, range_low, range_max,
            x_positions_min_u, y_positions_min_u,
            x_positions_user_u_high, y_positions_user_u_high,
            x_positions_user_u_low, y_positions_user_u_low,
            x_positions_bounding, y_positions_bounding,
            x_positions_max_range, y_positions_max_range           
        )
    
    #----------------------------Total Distance Travelled by Projectile------------------------
    
    def trajectory_length(self, u, theta, range, g):

        def z_func(z):
            return 0.5 * np.log(np.abs(np.sqrt(1 + z**2) + z)) + 0.5 * z * np.sqrt(1 + z**2)
        
        tan_theta = np.tan(theta)
        z1 = tan_theta
        z2 = tan_theta - (g*range / u**2)*(1 + tan_theta**2)
        
        a = (u**2) / (g * (1 + tan_theta**2))
        s = a * (z_func(z1) - z_func(z2))
    
        return s





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
