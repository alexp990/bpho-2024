from manim import *
import numpy as np

class Task2(Scene):
    def construct(self):

        # Initial Parameters
        h = 1  
        u = 5
        theta = 30  
        theta_tracker = ValueTracker(theta)
        g = 9.81  
        step = 100
        theta_tracker = ValueTracker(theta)

        def generate_path(theta):
            theta_rad = np.deg2rad(theta)
            
            # Compute the range
            range_value = (u ** 2 / g) * (np.sin(theta_rad) * np.cos(theta_rad) + 
                    np.cos(theta_rad) * np.sqrt(np.square(np.sin(theta_rad)) + 
                    (2 * g * h) / np.square(u)))
                    
            dx = range_value / step

            x_positions = [0]
            y_positions = [h]

            x = 0

            while True:
                x += dx
                y = (h + x * np.tan(theta_rad) - 
                    (g / (2 * u ** 2)) * (1 + np.tan(theta_rad) ** 2) * x ** 2)

                x_positions.append(x)
                y_positions.append(y)

                if y <= 0:
                    break

            return x_positions, y_positions
        
        x_positions, y_positions = generate_path(30)
        
        def update_path(obj):
            current_theta = theta_tracker.get_value()
            x_positions, y_positions = generate_path(current_theta)
            obj.set_points([*zip(x_positions, y_positions, np.zeros_like(x_positions))])

        #Generate Initial PAth
        projectile_path = VMobject()
        projectile_path.set_points([*zip(x_positions, y_positions, np.zeros_like(x_positions))])
        projectile_path.set_color(RED)

        axes = Axes(
        x_range=[0, max(x_positions) + 1, 1],
        y_range=[0, max(y_positions) + 1, 1],
        axis_config={"color": BLUE}
        )

        self.add(axes, projectile_path)

        velocity_label = MathTex(r"u = 5 \, \text{m/s}").scale(0.7)
        angle_label = MathTex(r"\theta = 70^\circ").scale(0.7)

        velocity_label.to_corner(UL).shift(RIGHT * 1.1)
        angle_label.next_to(velocity_label, DOWN)

        self.play(Write(velocity_label), Write(angle_label))

        self.add(theta_tracker)
        self.wait(1)

        theta_tracker.set_value(30)  # Change theta to 30
        self.play(theta_tracker.animate.set_value(80), UpdateFromFunc(projectile_path, update_path))
        self.wait(1)
        self.play(theta_tracker.animate.set_value(50), UpdateFromFunc(projectile_path, update_path))
        self.wait(1)

        self.wait(3)
