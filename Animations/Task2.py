from manim import *
import numpy as np

"""Add changing u vector LABEL: NO
Add equations: NO"""

class Task2(Scene):
    def construct(self):

        # Initial Parameters
        h = 1  
        u = 5
        theta_vals = [20, 30, 40, 50, 60, 70, 80]
        g = 9.81  
        step = 1000

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
        
        
        x_for_axes, y_for_axes, nan1, nan2 = projectile_motion(theta_vals[1])
        axes = Axes(
        x_range=[0, max(x_for_axes) * 2, 1],  
        y_range=[0, max(y_for_axes) * 2, 1], 
        axis_config={"color": BLUE}
        )

        self.add(axes)

        #Labels for initial conditions
        init_labels_scale = 0.5
        shift_val = 1
        #velocity_label = MathTex(r"u = 5.0 \, \text{m/s}").scale(init_labels_scale)
        #angle_label = MathTex(rf"\theta = {theta_vals[1]}^\circ", color=PINK).scale(init_labels_scale)
        height_label_brace_text = MathTex(r"1.0 \, \text{m}").scale(0.5)
        height_label_brace = BraceBetweenPoints(axes.c2p(0, 0), axes.c2p(0, h), LEFT)
        height_label_brace_text.next_to(height_label_brace, LEFT).shift(RIGHT * 0.15)
        step_label = Tex(rf"Accuracy = {step} x points/range").scale(init_labels_scale)
        
        
        initial_conditions = VGroup(step_label).arrange(DOWN, buff=0.2)
        initial_conditions.to_corner(UL).shift(RIGHT * shift_val)

        self.play(Write(initial_conditions), Create(height_label_brace), Write(height_label_brace_text))

        #Initial line
        x_pos, y_pos, u_x, u_y = projectile_motion(theta_vals[0])

        initial_path = axes.plot_line_graph(
            x_values=x_pos,
            y_values=y_pos,
            line_color=PINK,
            add_vertex_dots=False
        )

        angle = Angle(
            Line(axes.c2p(0, h), axes.c2p(1, h)),  # X-axis
            Line(axes.c2p(0, h), axes.c2p(u_x, h + u_y)),  # Initial velocity
            radius=0.5,
            other_angle=False,
            color=PINK
        )
        angle.set_z_index(9)

        angle_text = MathTex(rf"{theta_vals[0]}^\circ", color=PINK)
        angle_text.next_to(angle, RIGHT).shift(UP * 0.1).scale(0.7)

        #Line for angle label
        line_for_angle_label = Line(axes.c2p(0, h), axes.c2p(0.5, h))

        p = 1 #Index of which point to map tjhe end of the u_vector
        u_vector = Arrow(
            start=axes.c2p(x_pos[0], y_pos[0]),
            end=axes.c2p(x_pos[p] + u_x/8, y_pos[p] + u_y/8),
            buff=0,
            color=BLUE
        )       
        u_vector.set_z_index(10)
        angle_text.set_z_index(4)

        self.play(Create(initial_path), Create(u_vector), Create(angle), Write(angle_text), Create(line_for_angle_label), run_time=0.5)
        self.wait(1)
        paths = []
        colours = [RED, ORANGE, YELLOW, GREEN, BLUE, TEAL]

        del(theta_vals[0])

        for theta in theta_vals:
            x_pos, y_pos, u_x, u_y = projectile_motion(theta)
            current_colour = colours[theta_vals.index(theta)]
            path = axes.plot_line_graph(
                x_values=x_pos,
                y_values=y_pos,
                line_color=current_colour,
                add_vertex_dots=False
            )
            #path.set_z_index(theta_vals.index(theta))
            paths.append(path)

            #Update labels
            u_vector_new = Arrow(
            start=axes.c2p(x_pos[0], y_pos[0]),
            end=axes.c2p(x_pos[p] + u_x/8, y_pos[p] + u_y/8),
            buff=0,
            color=BLUE
            )       
            angle_new = Angle(
            Line(axes.c2p(0, h), axes.c2p(1, h)),  # X-axis
            Line(axes.c2p(0, h), axes.c2p(u_x, h + u_y)),  # Initial velocity
            radius=0.5,
            other_angle=False,
            color=current_colour
            )
            angle_new_text = MathTex(rf"{theta}^\circ", color=current_colour)
            angle_new_text.next_to(angle, RIGHT).shift(UP * 0.1).scale(0.7)

            #angle_label_new = MathTex(fr"\theta = {theta}^\circ", color=current_colour).scale(init_labels_scale)
            #initial_conditions = VGroup(velocity_label, angle_label_new, step_label).arrange(DOWN, buff=0.2)
            initial_conditions.to_corner(UL).shift(RIGHT * shift_val)

            self.play(Transform(u_vector, u_vector_new), Transform(angle, angle_new), Transform(angle_text, angle_new_text), Create(path), run_time=0.5)
        
            
#Renders scene
if __name__ == "__main__":
    scene = Task2()
    scene.render()








        
    