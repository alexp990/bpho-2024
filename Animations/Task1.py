from manim import *

"""Plot more than 1 initial value:NO"""

class Task1(Scene):
    def construct(self):

#-----------------------Projectile Motion Simulation--------------------

        h = 1  
        u = 5
        theta = 70  
        dt = 0.007
        g = 9.81  

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
            
#-----------------------Animation--------------------

        #Draws Axes for graph
        axes = Axes(
            x_range=[0, max(x_positions) + 1, 1],
            y_range=[0, max(y_positions) + 1, 1],
            axis_config={"color": BLUE}
        )

        self.add(axes)

        #Labels for initial conditions
        velocity_label = MathTex(r"u = 10 \, \text{m/s}").scale(0.7)
        angle_label = MathTex(r"\theta = 70^\circ").scale(0.7)
        
        velocity_label.to_corner(UL).shift(RIGHT * 1.1)
        angle_label.next_to(velocity_label, DOWN)

        self.play(Write(velocity_label), Write(angle_label))

        #Plots path
        projectile_path = axes.plot_line_graph(
            x_values=x_positions,
            y_values=y_positions,
            line_color=RED,
            vertex_dot_radius=0.04
        )
        projectile_path.set_color(RED)
        self.play(Create(projectile_path))

        #Initial Velocity Vector
        p = 2
        u_vector = Arrow(
        start=axes.c2p(x_positions[0], y_positions[0]),
        end=axes.c2p(x_positions[p] + u_x/8, y_positions[p] + u_y/8),
        buff=0,
        color=BLUE
        )

        self.play(Create(u_vector))

        u_vector_label = MathTex(r"\vec{u}")
        u_vector_label.next_to(u_vector.get_end(), DOWN).shift(DOWN * 0.3)

        self.play(Write(u_vector_label))

        i = int(len(y_positions) * 0.3) #Index of position to plot object on
        ball = Circle(radius=0.1, color=YELLOW, fill_opacity=0.8).move_to(axes.coords_to_point(x_positions[i], y_positions[i]))
        self.add(ball)

        #Vectors for object
        mg_vector = Arrow(start=ball.get_center(), end=ball.get_center() + DOWN * 1.105, color=GREEN)
        vx_vector = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * x_velocities[i], color=BLUE)
        vy_vector = Arrow(start=ball.get_center(), end=ball.get_center() + UP * y_velocities[i], color=BLUE)
        v_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([x_velocities[i], y_velocities[i], 0]), color=ORANGE)

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
