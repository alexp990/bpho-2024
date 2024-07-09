from manim import *
import numpy as np

"""Add axes: NO"""

class Task1(Scene):


    def construct(self):

#-----------------------Projectile Motion Simulation--------------------
        h = 1  
        u = 5.0
        theta_initial = 30 
        dt = 0.001
        g = 9.81  

        def projectile_motion(theta):

            theta_rad = np.radians(theta)

            u_x = u * np.cos(theta_rad)
            u_y = u * np.sin(theta_rad)

            x_positions = [0]
            y_positions = [h]
            x_velocities = []
            y_velocities = []
            vc = []
            t = 0

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
                
                if y <= 0:
                    break

            return x_positions, y_positions, x_velocities, y_velocities, vc, u_x, u_y
            
#-----------------------Animation--------------------

        #Draws Axes for graph
        
        x_for_axes, y_for_axes, nan1, nan2, nan3, nan4, nan5 = projectile_motion(theta_initial)
        axes = Axes(
            x_range=[0, max(x_for_axes) + 1, 1],
            y_range=[0, max(y_for_axes) + 1, 1],
            axis_config={"color": BLUE}
        )

        self.add(axes)

        #Labels for initial conditions
        velocity_label = MathTex(r"u = 5.0 \, \text{m/s}").scale(0.7)
        angle_label = MathTex(rf"\theta = {theta_initial}^\circ", color=RED).scale(0.7)
        
        velocity_label.to_corner(UL).shift(RIGHT * 1.1)
        angle_label.next_to(velocity_label, DOWN)

        self.play(Write(velocity_label), Write(angle_label))

        #Showing equations describing projectile motion
        x_eq = MathTex("x = u_x t", color=RED)
        y_eq = MathTex("y = h + u_y t - \\frac{1}{2} g t^2", color=RED)
        vx_eq = MathTex("v_x = u_x")
        vy_eq = MathTex("v_y = u_y - g t")
        v_eq = MathTex("v = \\sqrt{v_x^2 + v_y^2}")

        equations = VGroup(x_eq, y_eq, vx_eq, vy_eq, v_eq).arrange(DOWN, buff=0.5)
        equations.to_corner(UR)

        x_pos, y_pos, x_v, y_v, v, u_x, u_y = projectile_motion(theta_initial)

        initial_path = axes.plot_line_graph(
            x_values=x_pos,
            y_values=y_pos,
            line_color=RED,
            add_vertex_dots=False
        )

        self.play(Create(initial_path), Write(equations))

        #self.wait(0.5)

        theta_vals = [40, 50, 60, 70]
        paths = []
        paths.append(initial_path)
        run_time = 1

        colours = [ORANGE, YELLOW, GREEN, BLUE]

        for theta in theta_vals:
            x_pos, y_pos, x_v, y_v, v, u_x, u_y = projectile_motion(theta)
            current_colour = colours[theta_vals.index(theta)]
            path = axes.plot_line_graph(
                x_values=x_pos,
                y_values=y_pos,
                line_color=current_colour,
                add_vertex_dots=False
            )
            paths.append(path)
            # Update labels
            velocity_label_new = MathTex(fr"u = {u:.1f} \, \text{{m/s}}").scale(0.7)
            angle_label_new = MathTex(fr"\theta = {theta}^\circ", color=current_colour).scale(0.7)

            x_eq_new = MathTex("x = u_x t", color=current_colour)
            y_eq_new = MathTex("y = h + u_y t - \\frac{1}{2} g t^2", color=current_colour)

            equations = VGroup(x_eq_new, y_eq_new, vx_eq, vy_eq, v_eq).arrange(DOWN, buff=0.5)
            equations.to_corner(UR)

            velocity_label_new.to_corner(UL).shift(RIGHT * 1.1)
            angle_label_new.next_to(velocity_label_new, DOWN)

            self.play(Transform(velocity_label, velocity_label_new), run_time=0.001)
            self.play(Transform(angle_label, angle_label_new), Transform(x_eq, x_eq_new), Transform(y_eq, y_eq_new), run_time=0.1)

            self.play(Create(path), run_time=run_time)
            run_time = run_time / 2

        theta_vals.insert(0, theta_initial)

        focus_theta = 50
        focus_index = theta_vals.index(focus_theta)
        focus_path = paths[focus_index]

        for i, path in enumerate(paths):
            if i != focus_index:
                self.play(path.animate.set_stroke(opacity=0), run_time=0.1)
            else:
                self.play(focus_path.animate.set_stroke(opacity=1, color=GREEN), run_time=0.5)

        self.wait(0.7)

        #generates vals for focus path
        x_pos_focus, y_pos_focus, x_v_focus, y_v_focus, v_focus, u_x_focus, u_y_focus = projectile_motion(focus_theta)

        # Update labels
        velocity_label_new = MathTex(fr"u = {u:.1f} \, \text{{m/s}}").scale(0.7)
        angle_label_new = MathTex(fr"\theta = {focus_theta}^\circ", color=GREEN).scale(0.7)

        x_eq_new = MathTex("x = u_x t", color=GREEN)
        y_eq_new = MathTex("y = h + u_y t - \\frac{1}{2} g t^2", color=GREEN)

        equations = VGroup(x_eq_new, y_eq_new, vx_eq, vy_eq, v_eq).arrange(DOWN, buff=0.5)
        equations.to_corner(UR)

        velocity_label_new.to_corner(UL).shift(RIGHT * 1.1)
        angle_label_new.next_to(velocity_label_new, DOWN)

        self.play(Transform(velocity_label, velocity_label_new), run_time=0.001)
        self.play(Transform(angle_label, angle_label_new), Transform(x_eq, x_eq_new), Transform(y_eq, y_eq_new), run_time=0.1)

        #Initial Velocity Vector
        p = 2
        u_vector = Arrow(
        start=axes.c2p(x_pos_focus[0], y_pos_focus[0]),
        end=axes.c2p(x_pos_focus[p] + u_x_focus/8, y_pos_focus[p] + u_y_focus/8),
        buff=0,
        color=BLUE
        )

        u_vector_label = MathTex(r"\vec{u}")
        u_vector_label.next_to(u_vector.get_end(), UP)

        self.play(Write(u_vector_label), Create(u_vector), run_time=0.3)

        i = int(len(y_pos_focus) * 0.3) #Index of position to plot object on
        ball = Circle(radius=0.1, color=YELLOW, fill_opacity=0.8).move_to(axes.coords_to_point(x_pos_focus[i], y_pos_focus[i]))
        self.add(ball)

        # Angle label between x-axis and initial velocity vector
        angle = Angle(
            Line(axes.c2p(0, h), axes.c2p(1, h)),  # X-axis
            Line(axes.c2p(0, h), axes.c2p(u_x_focus, h + u_y_focus)),  # Initial velocity
            radius=0.5,
            other_angle=False,
        )
        angle_label = MathTex(r"\theta^\circ", color=GREEN)
        angle_label.next_to(angle, RIGHT).shift(UP * 0.1).shift(LEFT * 0.2).scale(0.7)

        #Line for angle label
        line_for_angle_label = Line(axes.c2p(0, h), axes.c2p(0.5, h))

        #Vectors for object
        mg_vector = Arrow(start=ball.get_center(), end=ball.get_center() + DOWN * 0.8, color=YELLOW)
        vx_vector = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * x_v_focus[i], color=LIGHT_PINK)
        vy_vector = Arrow(start=ball.get_center(), end=ball.get_center() + UP * y_v_focus[i], color=RED)
        v_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([x_v_focus[i], y_v_focus[i], 0]), color=ORANGE)

        self.play(
            Create(mg_vector),
            Create(vx_vector),
            Create(vy_vector),
            Create(v_vector),
            Create(angle),
            Create(angle_label),
            Create(line_for_angle_label),
            run_time = 0.5
        )

        mg_label = MathTex(r"\vec{mg}", color=YELLOW).next_to(mg_vector).scale(0.9)
        vx_label = MathTex(r"\vec{v}_x", color=LIGHT_PINK).next_to(vx_vector, RIGHT)
        vy_label = MathTex(r"\vec{v}_y", color=RED).next_to(vy_vector, UP)
        v_label = MathTex(r"\vec{v}", color=ORANGE).next_to(v_vector, RIGHT).shift(UP * 0.5)

        vx_eq_new = MathTex("v_x = u_x", color=LIGHT_PINK)
        vy_eq_new = MathTex("v_y = u_y - g t", color=RED)
        v_eq_new = MathTex("v = \\sqrt{v_x^2 + v_y^2}", color=ORANGE)

        equations = VGroup(x_eq, y_eq_new, vx_eq_new, vy_eq_new, v_eq_new).arrange(DOWN, buff=0.5)
        equations.to_corner(UR)


        self.play(
            Write(mg_label),
            Write(vx_label),
            Write(vy_label),
            Write(v_label),
            Transform(vx_eq, vx_eq_new), Transform(vy_eq, vy_eq_new), Transform(v_eq, v_eq_new),
            run_time=0.7
        )

        self.wait(2)


#Renders scene
if __name__ == "__main__":
    scene = Task1()
    scene.render()


        


    