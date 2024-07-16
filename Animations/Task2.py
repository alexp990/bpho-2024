from manim import *
import numpy as np

"""Fix u vector placement: NO"""

class Task2(Scene):
    def construct(self):       

        # Initial Parameters
        h = 1  
        u = 5
        theta_vals = [20, 30, 40, 50, 60, 70, 80]
        g = 9.81  
        step = 1000

        def projectile_motion(h, u, theta, step, g=9.81):

            #-----------------------Projectile Motion Simulation--------------------

            theta_rad = np.deg2rad(theta)
            range = u**2/g * (np.sin(theta_rad)*np.cos(theta_rad) + np.cos(theta_rad)*np.sqrt(np.square(np.sin(theta_rad)) + (2*g*h)/(np.square(u))))
            tof = range / (u * np.cos(theta_rad))
            dx = range / step

            u_x = u * np.cos(theta_rad)
            u_y = u * np.sin(theta_rad)

            x_a = (u**2 / g) * np.sin(theta_rad)*np.cos(theta_rad)
            y_a = h + (u**2 / (2 * g)) * ((np.sin(theta_rad))**2)

            x_pos = [0]
            y_pos = [h]

            x = 0

            while True:
                x = x + dx

                y = h + x*np.tan(theta_rad) - (g / (2 * u ** 2)) * (1 + np.tan(theta_rad) ** 2) * x ** 2

                x_pos.append(x)
                y_pos.append(y)

                if y <= 0:
                    break

            return x_pos, y_pos, tof, range, x_a, y_a, u_x, u_y


        #Constant vals for graphs
        u = 5
        h = 1
        step = 1000

        x_for_axes, y_for_axes, nan1, nan2, nan3, nan4, nan6, nan7 = projectile_motion(h, u, theta_vals[1], step)
        axes = Axes(
        x_range=[0, max(x_for_axes) * 2, 1],  
        y_range=[0, max(y_for_axes) * 2, 1], 
        axis_config={"color": BLUE}
        )
        axes.scale(0.8)
        axes.add_coordinates()
        self.add(axes)

        #Labels for initial conditions
        init_labels_scale = 0.5
        shift_val = 1

        height_label_brace_text = MathTex(r"1.0 \, \text{m}").scale(0.5)
        height_label_brace = BraceBetweenPoints(axes.c2p(0, 0), axes.c2p(0, h), LEFT)
        height_label_brace_text.next_to(height_label_brace, LEFT).shift(RIGHT * 0.15)

        step_label = Tex(rf"Accuracy = {step} x points/range").scale(init_labels_scale)
        u_label = MathTex(r"u = 5.0 \, \text{m/s}").scale(init_labels_scale)
        
        initial_conditions = VGroup(step_label, u_label).arrange(DOWN, buff=0.2)
        initial_conditions.to_corner(UL).shift(RIGHT * shift_val)

        #Showing equations describing projectile motion
        y_eq = MathTex(r"y = h + x\tan \theta - \frac{g}{2u^2} \left(1 + \tan^2 \theta \right)x^2", color=PINK)
        x_eq = Tex("Each x position is a fraction of the range R",  color=PINK)
        x_a_eq = MathTex(r"x_a = \frac{u^2}{g} \sin \theta \cos \theta", color=YELLOW)
        y_a_eq = MathTex(r"y_a = h + \frac{u^2}{2g} \sin^2 \theta", color=YELLOW)
        tof_eq = MathTex(r"TOF = \frac{R}{u \cos \theta}")
        range_eq = MathTex(r"R = \frac{u^2}{g} \left( \sin \theta \cos \theta + \cos \theta \sqrt{\sin^2 \theta + \frac{2gh}{u^2}} \right)", color=RED)

        equations = VGroup(y_eq, x_eq, x_a_eq, y_a_eq, tof_eq, range_eq).arrange(DOWN, buff=0.5).scale(0.5)
        equations.to_corner(UR) 

        self.play(Write(initial_conditions), Create(height_label_brace), Write(height_label_brace_text), Write(equations))

        #Initial line
        x_pos, y_pos, tof, range, x_a, y_a, u_x, u_y = projectile_motion(h, u, theta_vals[0], step)

        initial_path = axes.plot_line_graph(
            x_values=x_pos,
            y_values=y_pos,
            line_color=PINK,
            add_vertex_dots=False
        )
        #Apogee point
        apogee_point = Dot(point=axes.c2p(x_a, y_a), color=WHITE, radius=0.1)
        apogee_point_text = MathTex(r"x_a, y_a", color=YELLOW).next_to(apogee_point, UP).scale(0.7)

        #Brace for range equation
        range_brace = BraceBetweenPoints(axes.c2p(0, 0), axes.c2p(range, 0))
        range_brace_text = Tex("Range R", color=RED)
        range_brace_text.next_to(range_brace, DOWN).scale(0.5)

        #Angle theta graphical representation
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

        #U vector text
        u_vector_text = MathTex(r"\vec{u}")
        u_vector_text.next_to(u_vector, UP * 0.5).scale(0.7)

        u_vector.set_z_index(10)
        u_vector_text.set_z_index(15)
        angle_text.set_z_index(4)

        self.play(Create(initial_path), Create(u_vector), Create(angle), Write(u_vector_text), Write(angle_text), Create(line_for_angle_label), Create(range_brace), Write(range_brace_text), run_time=0.5)
        self.play(Create(apogee_point), Write(apogee_point_text), run_time=0.5)
        self.wait(1)
        paths = []
        colours = [RED, ORANGE, YELLOW, GREEN, BLUE, TEAL]

        del(theta_vals[0])

        #Plota many lines
        for theta in theta_vals:
            x_pos, y_pos, tof, range, x_a, y_a, u_x, u_y = projectile_motion(h, u, theta, step)
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

            #U vector text
            u_vector_text_new = MathTex(r"\vec{u}")
            u_vector_text_new.next_to(u_vector_new, UP * 0.5).scale(0.7)

            y_eq_new = MathTex(r"y = h + x\tan \theta - \frac{g}{2u^2} \left(1 + \tan^2 \theta \right)x^2", color=current_colour).scale(0.5)
            x_eq_new = Tex("Each x position is a fraction of the range R", color=current_colour).scale(0.5)
            equations = VGroup(y_eq_new, x_eq_new, x_a_eq, y_a_eq, tof_eq, range_eq).arrange(DOWN)
            equations.to_corner(UR) 

            apogee_point_new = Dot(point=axes.c2p(x_a, y_a), color=WHITE, radius=0.1)
            apogee_point.set_z_index(path.z_index + 1)
            apogee_point_text_new = MathTex(r"x_a, y_a", color=YELLOW).next_to(apogee_point_new, UP).scale(0.7)
 
            angle_new = Angle(
            Line(axes.c2p(0, h), axes.c2p(1, h)), 
            Line(axes.c2p(0, h), axes.c2p(u_x, h + u_y)), 
            radius=0.5,
            other_angle=False,
            color=current_colour
            )

            angle_new_text = MathTex(rf"{theta}^\circ", color=current_colour)
            angle_new_text.next_to(angle, RIGHT).shift(UP * 0.1).scale(0.7)

            initial_conditions.to_corner(UL).shift(RIGHT * shift_val)

            #Transforms all labels that need transforming
            self.play(Transform(apogee_point, apogee_point_new), Transform(apogee_point_text, apogee_point_text_new), Transform(x_eq, x_eq_new), Transform(y_eq, y_eq_new), Transform(u_vector, u_vector_new), Transform(u_vector_text, u_vector_text_new), Transform(angle, angle_new), Transform(angle_text, angle_new_text), Create(path), run_time=0.5)

            self.wait(0.5)

        self.wait(1)
        
            
#Renders scene
if __name__ == "__main__":
    scene = Task2()
    scene.render()








        
    