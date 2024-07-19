from manim import *

class Task3(Scene):
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
        
        X, Y = 100, 50
        step = 1000
        h = 0
        user_u = 50

        _, _, _, _, _, x_for_axes, y_for_axes, _, _, _, _  = projectile_motion(user_u, X, Y, step, h)

        #Axes
        axes = Axes(
        x_range=[0, max(x_for_axes) * 2, 40],  
        y_range=[0, max(y_for_axes) * 2, 40], 
        axis_config={"color": BLUE}
        )
        axes.scale(0.7)
        axes.to_corner(DL)
        axes.shift(RIGHT*0.2).shift(UP*0.2)
        axes.add_coordinates()
        self.add(axes)

        #Showing equations describing projectile motion
        u_eq = MathTex(
            r"u \geq \sqrt{g\sqrt{Y} + \sqrt{X^2 + Y^2}}").scale(0.6)

        theta_eq_parts = MathTex(
            r"a = \frac{g}{2u^2}X^2, \quad b = -X, \quad c = Y - h + \frac{gX^2}{2u^2}").scale(0.6)

        theta_eq_quadratic = MathTex(
            r"\theta_{\pm} = \tan^{-1}\left(\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\right)").scale(0.6)
        
        discriminant_description_text = Tex(
            r"When $u > u_{min}$, $b^2-4ac > 0$  \\",
            r"$\therefore$ the +solution is the high path and -solution is the low path"
        )
        #self.add(index_labels(discriminant_description_text[0]))
        discriminant_description_text[1][4:13].set_color(ORANGE)
        discriminant_description_text[1][29:38].set_color(GREEN)
        discriminant_description_text.scale(0.6)

        equations = VGroup(u_eq, theta_eq_parts, theta_eq_quadratic, discriminant_description_text).arrange(DOWN, buff=0.3)
        equations.to_corner(UR)

        self.play(Write(equations))

        u_min, theta_deg_min_u, theta_deg_user_u_high, theta_deg_user_u_low, range_min_u , x_pos_min_u, y_pos_min_u, x_pos_u_high, y_pos_u_high, x_pos_u_low, y_pos_u_low = projectile_motion(user_u, X, Y, step, h)  

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

        angle_labels = VGroup(angle_min_u_text, angle_u_high_text, angle_u_low_text).arrange(DOWN, buff=0.2).scale(0.6)
        angle_labels.next_to(initial_conditions, RIGHT)

        self.play(Create(u_min_path), Create(u_high_path), Create(u_low_path), Write(target_point), Write(target_point_text), Write(initial_conditions), Write(angle_labels))

        self.wait(3)

        

            

