from manim import *

import numpy as np

class Task7(Scene):
    def construct(self):
        # Parameters
        h = 10.0   # Initial height (m)
        N = 6     # Maximum number of bounces
        C = 0.7    # Coefficient of restitution
        g = 9.81   # Acceleration due to gravity (m/s^2)
        dt = 1/25  # Time step (s)
        theta = 45.0  # Initial launch angle in degrees
        u = 20.0   # Initial speed of object in m/s
-
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

        # Compute trajectory
        t, x, y, vx, vy = verlet_trajectory_solver(N, C, g, dt, h, theta, u)
        
        # Create axes
        axes = Axes(
            x_range=[0, np.max(x) * 1.1, 20],
            y_range=[0, np.max(y) * 1.1, 5],
            axis_config={"color": BLUE},
        )

        axes.add_coordinates()

        dots = [Dot(axes.c2p(x_coords, y_coords), color=RED, radius=0.03) for x_coords, y_coords in zip(x, y)]

        self.play(Create(axes))

        self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=0.01))

        x_new_eq = MathTex(r"x_{\text{new}} = x_{\text{old}} + v_x \cdot \Delta t + \frac{1}{2} a_x \cdot (\Delta t)^2")
        y_new_eq = MathTex(r"y_{\text{new}} = y_{\text{old}} + v_y \cdot \Delta t + \frac{1}{2} a_y \cdot (\Delta t)^2")

        v_x_new_eq = MathTex(r"v_x^{\text{new}} = v_x^{\text{old}} + \frac{1}{2} (a_x + a_x^{\text{new}}) \cdot \Delta t")
        v_y_new_eq = MathTex(r"v_y^{\text{new}} = v_y^{\text{old}} + \frac{1}{2} (a_y + a_y^{\text{new}}) \cdot \Delta t")

        v_y_bounce_eq = MathTex(r"v_y^{\text{new}} = -C \cdot v_y")

        verlet_text = Tex("'Verlet Integration'", color = RED).scale(0.8).to_corner(UR)

        equations = VGroup(x_new_eq, y_new_eq, v_x_new_eq, v_y_new_eq, v_y_bounce_eq).arrange(DOWN, buff=0.3).scale(0.6).next_to(verlet_text, DOWN)

        max_bounces_label = Tex(f"N of bounces simulated = {N}")
        coeff_of_rest_label = Tex(f"Coefficient of restitution = {C}")
        delta_t_label = MathTex(r"\Delta t = \frac{1}{25} seconds")
        u_label = Tex(f"u = {20} m/s")

        labels = VGroup(max_bounces_label, coeff_of_rest_label, delta_t_label, u_label).arrange(DOWN, buff=0.3).scale(0.6).next_to(verlet_text, LEFT).shift(DOWN).shift(LEFT)

        self.play(Write(verlet_text), Write(equations), Write(labels), run_time=2)

        self.wait(4)


