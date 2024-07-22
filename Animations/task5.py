from manim import *
import numpy as np

#fix alpha color

class Task5(Scene):
    def construct(self):    

        def projectile_motion(user_u, X, Y, step, h, g=9.81, ):

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
            y_positions_bounding = [(user_u**2 / (2 * g)) - (g / (2 * user_u**2)) * 0**2]

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

            while True:
                x += dx
                y_high = h + x * np.tan(theta_rad_user_u_high) - (g / (2 * user_u**2)) * (1 + np.tan(theta_rad_user_u_high)**2) * x**2
                if y_high <= 0:
                    break
                x_positions_user_u_high.append(x)
                y_positions_user_u_high.append(y_high)

            x = 0

            while True:
                x += dx
                y_bound = (user_u**2 / (2 * g)) - (g / (2 * user_u**2)) * x**2
                x_positions_bounding.append(x)
                y_positions_bounding.append(y_bound)
                if y_bound <= 0:
                    break
 
            x = 0

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
        
        X, Y = 600, 100
        step = 1000
        h = 0
        user_u = 100

        u_min, theta_deg_min_u, theta_deg_user_u_high, theta_deg_user_u_low, theta_deg_max_range, range_min_u , x_pos_min_u, y_pos_min_u, x_pos_u_high, y_pos_u_high, x_pos_u_low, y_pos_u_low, x_pos_bounding, y_pos_bounding, x_pos_max_r, y_pos_max_r = projectile_motion(user_u, X, Y, step, h)  

        #Axes
        axes = Axes(
        x_range=[0, max(x_pos_bounding) * 1.3, 200],  
        y_range=[0, max(y_pos_bounding) * 1.3, 200], 
        axis_config={"color": BLUE}
        )
        axes.scale(0.8)
        axes.to_corner(DL)
        axes.shift(RIGHT*0.2).shift(UP*0.2)
        axes.add_coordinates()
        self.add(axes)

        #Showing equations describing projectile motion
        y_bound_eq = MathTex(
            r"y = \frac{u^2}{2g} - \frac{g}{2u^2}x^2", color=YELLOW
        )

        alpha_eq = MathTex(
            r"\alpha = \frac{2gh}{u^2}"
        )

        max_range_angle_eq = MathTex(
            r"\theta_{maxrange} = \arcsin(\frac{1}{\sqrt{2 + \alpha}})", color=PINK
        )

        equations = VGroup(y_bound_eq, alpha_eq, max_range_angle_eq).arrange(DOWN, buff=0.3).scale(0.6)
        equations.to_corner(UR)

        self.play(Write(equations))

        u_min_path = axes.plot_line_graph(
            x_values=x_pos_min_u,
            y_values=y_pos_min_u,
            line_color=RED,
            add_vertex_dots=False
        )

        u_high_path = axes.plot_line_graph(
            x_values=x_pos_u_high,
            y_values=y_pos_u_high,
            line_color=ORANGE,
            add_vertex_dots=False
        )

        u_low_path = axes.plot_line_graph(
            x_values=x_pos_u_low,
            y_values=y_pos_u_low,
            line_color=GREEN,
            add_vertex_dots=False
        )

        max_r_path = axes.plot_line_graph(
            x_values=x_pos_max_r,
            y_values=y_pos_max_r,
            line_color=PINK,
            add_vertex_dots=False
        )

        bounding_path = axes.plot_line_graph(
            x_values=x_pos_bounding,
            y_values=y_pos_bounding,
            line_color=YELLOW,
            add_vertex_dots=False
        )

        target_point = Dot(point=axes.c2p(X, Y), color=WHITE, radius=0.1)
        target_point_text = Tex(r"(X, Y)", color=BLUE).next_to(target_point, UP).scale(0.7).shift(LEFT * 0.1).shift(DOWN * 0.3)

        u_min_label = MathTex(r"u_{\text{min}} \approx " + f"{int(u_min)} \, \t{{m/s}}", color=RED).scale(0.6)
        user_u_label = MathTex(r"u = " + f"{user_u} \, \t{{m/s}}").scale(0.6)
        target_label = Tex(rf"X = {X}, Y = {Y}", color=BLUE).scale(0.6)
        
        initial_conditions = VGroup(u_min_label, user_u_label, target_label).arrange(DOWN, buff=0.2)
        initial_conditions.to_corner(UL).shift(RIGHT * 0.3).shift(DOWN * 0.1)

        angle_min_u_text = MathTex(r"\theta_{u_{\text{min}}} \approx " + f"{int(theta_deg_min_u)} ^\\circ", color=RED)
        angle_u_high_text = MathTex(r"\theta_{\text{high}} \approx " + f"{int(theta_deg_user_u_high)} ^\\circ", color=ORANGE)
        angle_u_low_text = MathTex(r"\theta_{\text{low}} \approx " + f"{int(theta_deg_user_u_low)} ^\\circ", color=GREEN)
        angle_max_r_text = MathTex(r"\theta_{\text{maxrange}} \approx " + f"{int(theta_deg_max_range)} ^\\circ", color=PINK)

        angle_labels = VGroup(angle_min_u_text, angle_u_high_text, angle_u_low_text, angle_max_r_text).arrange(DOWN, buff=0.2).scale(0.6)
        angle_labels.next_to(initial_conditions, RIGHT)

        self.play(Create(u_min_path), Create(u_high_path), Create(u_low_path), Create(max_r_path), Create(bounding_path), Write(target_point), Write(target_point_text), Write(initial_conditions), Write(angle_labels))

        self.wait(3)