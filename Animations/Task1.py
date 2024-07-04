from manim import *

class ProjectileMotion(Scene):
    def construct(self):

        h = 1  
        u = 5
        theta = 60  
        dt = 0.05  
        g = 9.81  

        theta_rad = np.radians(theta)

        u_x = u * np.cos(theta_rad)
        u_y = u * np.sin(theta_rad)

        x_positions = []
        y_positions = []
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
            
            if y < 0:
                break
            
            x_positions.append(x)
            y_positions.append(y)
            x_velocities.append(vx)
            y_velocities.append(vy)
            vc.append(v)

        axes = Axes(
            x_range=[0, max(x_positions) + 1, 1],
            y_range=[0, max(y_positions) + 1, 1],
            axis_config={"color": BLUE}
        )
        self.add(axes)

        velocity_label = MathTex(r"u = 5 \, \text{m/s}")
        angle_label = MathTex(r"\theta = 30^\circ")
        
        velocity_label.to_corner(UL).shift(RIGHT * 1)
        angle_label.next_to(velocity_label, DOWN)

        self.play(Write(velocity_label), Write(angle_label))

        projectile_path = axes.plot_line_graph(
            x_values=x_positions,
            y_values=y_positions,
            line_color=RED
        )
        self.play(Create(projectile_path))

        i = 6
        ball = Circle(radius=0.1, color=YELLOW).move_to(axes.coords_to_point(x_positions[i], y_positions[i]))
        self.add(ball)

        mg_vector = Arrow(start=ball.get_center(), end=ball.get_center() + DOWN, color=GREEN)
        vx_vector = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * x_velocities[i], color=BLUE)
        vy_vector = Arrow(start=ball.get_center(), end=ball.get_center() + UP * y_velocities[i], color=BLUE)
        v_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([x_velocities[i], y_velocities[i], 0]), color=ORANGE)

        self.play(
            Create(mg_vector),
            Create(vx_vector),
            Create(vy_vector),
            Create(v_vector)
        )

        mg_label = MathTex(r"\vec{mg}").next_to(mg_vector, DOWN)
        vx_label = MathTex(r"\vec{v}_x").next_to(vx_vector, RIGHT)
        vy_label = MathTex(r"\vec{v}_y").next_to(vy_vector, UP)
        v_label = MathTex(r"\vec{v}").next_to(v_vector, RIGHT)

        self.play(
            Write(mg_label),
            Write(vx_label),
            Write(vy_label),
            Write(v_label)
        )

        self.wait(5)

if __name__ == "__main__":
    scene = ProjectileMotion()
    scene.render()
