from manim import *
import numpy as np

class Task2(Scene):
    def construct(self):
        # Initial Parameters
        h = 1  
        u = 5
        theta_initial = 30
        g = 9.81  
        step = 100

        def projectile_motion(theta):
            theta_rad = np.deg2rad(theta)
            
            range_value = (u ** 2 / g) * (np.sin(theta_rad) * np.cos(theta_rad) + 
                                          np.cos(theta_rad) * np.sqrt(np.square(np.sin(theta_rad)) + 
                                          (2 * g * h) / np.square(u)))
                    
            dx = range_value / step

            u_x = u * np.cos(theta_rad)
            u_y = u * np.sin(theta_rad)

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

            return x_positions, y_positions, u_x, u_y

        x_for_axes, y_for_axes, nan1, nan2 = projectile_motion(theta_initial)
        axes = Axes(
            x_range=[0, max(x_for_axes) * 2, 1],  
            y_range=[0, max(y_for_axes) * 2, 1], 
            axis_config={"color": BLUE}
        )

        self.add(axes)

        # Labels for initial conditions
        init_labels_scale = 0.3
        shift_val = 1
        velocity_label = MathTex(r"u = 5.0 \, \text{m/s}").scale(init_labels_scale)
        angle_label = MathTex(rf"\theta = {theta_initial}^\circ", color=PINK).scale(init_labels_scale)
        height_label_brace_text = MathTex(r"1.0 \, \text{m}").scale(init_labels_scale)
        height_label_brace = BraceBetweenPoints(axes.c2p(0, 0), axes.c2p(0, h), LEFT)
        height_label_brace_text.next_to(height_label_brace, LEFT)
        step_label = MathTex(rf"accuracy - {step}").scale(init_labels_scale)

        initial_conditions = VGroup(velocity_label, angle_label, step_label).arrange(DOWN, buff=0.2)
        initial_conditions.to_corner(UL).shift(RIGHT * shift_val)

        self.play(Write(initial_conditions), Create(height_label_brace), Write(height_label_brace_text))

        theta_vals = [20, 30, 40, 50, 60, 70, 80]
        paths = []
        colours = [PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        for theta in theta_vals:
            x_pos, y_pos, u_x, u_y = projectile_motion(theta)
            current_colour = colours[theta_vals.index(theta)]
            path = axes.plot_line_graph(
                x_values=x_pos,
                y_values=y_pos,
                line_color=current_colour,
                add_vertex_dots=False
            )
            paths.append(path)

            # Update labels
            angle_label_new = MathTex(fr"\theta = {theta}^\circ", color=current_colour).scale(init_labels_scale)
            initial_conditions = VGroup(velocity_label, angle_label_new, step_label).arrange(DOWN, buff=0.2)
            initial_conditions.to_corner(UL).shift(RIGHT * shift_val)

            self.play(Transform(angle_label, angle_label_new), Create(path), run_time=0.5)

            # Update u_vector
            u_vector = Arrow(
                start=axes.c2p(x_pos[0], y_pos[0]),
                end=axes.c2p(x_pos[2] + u_x/8, y_pos[2] + u_y/8),
                buff=0,
                color=BLUE
            )

            self.play(
                ApplyMethod(u_vector.put_start_and_end_on, axes.c2p(x_pos[0], y_pos[0]), axes.c2p(x_pos[2] + u_x/8, y_pos[2] + u_y/8)),
                run_time=0.5
            )

            # Add the u_vector to the scene
            self.add(u_vector)

        self.wait(1)
