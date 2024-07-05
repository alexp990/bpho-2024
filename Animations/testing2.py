from manim import *
import numpy as np

"""Plot more than 1 initial value:NO"""

class Task1(Scene):


    def construct(self):

        def mean(input):
            mean = sum(input) / len(input)

            return mean

#-----------------------Projectile Motion Simulation--------------------
        h = 1  
        u = 5
        theta_values = [20, 85, 50]  
        dt = 0.007
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
        
        x_for_axes, y_for_axes, nan1, nan2, nan3, nan4, nan5 = projectile_motion(mean(theta_values))
        axes = Axes(
            x_range=[0, max(x_for_axes) + 1, 1],
            y_range=[0, max(y_for_axes) + 1, 1],
            axis_config={"color": BLUE}
        )

        self.add(axes)

        #Labels for initial conditions
        velocity_label = MathTex(r"u = 10 \, \text{m/s}").scale(0.7)
        angle_label = MathTex(r"\theta = 20^\circ").scale(0.7)
        
        velocity_label.to_corner(UL).shift(RIGHT * 1.1)
        angle_label.next_to(velocity_label, DOWN)

        self.play(Write(velocity_label), Write(angle_label))

        for theta in theta_values:

            x_pos, y_pos, x_v, y_v, v, ux, uy = projectile_motion(theta)

            projectile_path_new = axes.plot_line_graph(
                x_values=x_pos,
                y_values=y_pos,
                line_color=RED,
                vertex_dot_radius=0.04,
                vertex_dot_style={"fill_color": RED}
            )

            if 'projectile_path' in locals():
                self.play(Transform(projectile_path, projectile_path_new))
            else:
                projectile_path = projectile_path_new
                self.play(Create(projectile_path))

            # Update labels
            velocity_label_new = MathTex(fr"u = {u:.1f} \, \text{{m/s}}").scale(0.7)
            angle_label_new = MathTex(fr"\theta = {theta}^\circ").scale(0.7)
            velocity_label_new.to_corner(UL).shift(RIGHT * 1.1)
            angle_label_new.next_to(velocity_label_new, DOWN)
            self.play(Transform(velocity_label, velocity_label_new))
            self.play(Transform(angle_label, angle_label_new))

            #Initial Velocity Vector
        p = 2
        u_vector = Arrow(
        start=axes.c2p(x_pos[0], y_pos[0]),
        end=axes.c2p(x_pos[p] + ux/8, y_pos[p] + uy/8),
        buff=0,
        color=BLUE
        )

        self.play(Create(u_vector))

        u_vector_label = MathTex(r"\vec{u}")
        u_vector_label.next_to(u_vector.get_end(), DOWN).shift(DOWN * 0.3)

        self.play(Write(u_vector_label))

        i = int(len(y_pos) * 0.3) #Index of position to plot object on
        ball = Circle(radius=0.1, color=YELLOW, fill_opacity=0.8).move_to(axes.coords_to_point(x_pos[i], y_pos[i]))
        self.add(ball)

        #Vectors for object
        mg_vector = Arrow(start=ball.get_center(), end=ball.get_center() + DOWN * 1.105, color=GREEN)
        vx_vector = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * x_pos[i], color=BLUE)
        vy_vector = Arrow(start=ball.get_center(), end=ball.get_center() + UP * y_pos[i], color=BLUE)
        v_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([x_pos[i], y_pos[i], 0]), color=ORANGE)

        self.play(
            Create(mg_vector),
            Create(vx_vector),
            Create(vy_vector),
            Create(v_vector)
        )

        mg_label = MathTex(r"\vec{mg}").next_to(mg_vector, ).scale(0.9)
        vx_label = MathTex(r"\vec{v}_x").next_to(vx_vector, RIGHT)
        vy_label = MathTex(r"\vec{v}_y").next_to(vy_vector, UP)
        v_label = MathTex(r"\vec{v}").next_to(v_vector, RIGHT).shift(UP * 0.5)

        self.play(
            Write(mg_label),
            Write(vx_label),
            Write(vy_label),
            Write(v_label)
        )

        #Showing equations describing projectile motion
        x_eq = MathTex("x = u_x t")
        y_eq = MathTex("y = h + u_y t - \\frac{1}{2} g t^2")
        vx_eq = MathTex("v_x = u_x")
        vy_eq = MathTex("v_y = u_y - g t")
        v_eq = MathTex("v = \\sqrt{v_x^2 + v_y^2}")

        self.wait(2)

        equations = VGroup(x_eq, y_eq, vx_eq, vy_eq, v_eq).arrange(DOWN, buff=0.5)
        equations.to_corner(UR)
        self.play(Write(equations))

        self.wait(5)


if __name__ == "__main__":
    scene = Task1()
    scene.render()


        


    