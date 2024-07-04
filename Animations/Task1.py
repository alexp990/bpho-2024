from manim import *

class ProjectileMotion(Scene):
    def construct(self):
        # Constants
        g = 9.8
        u = 10  # Initial velocity
        theta = 45 * DEGREES  # Angle of projection
        h = 4  # Initial height
        m = 1  # Mass, for completeness, though not used directly in plot
        t_max = (u * np.sin(theta) + np.sqrt((u * np.sin(theta))**2 + 2 * g * h)) / g
        x_max = u * np.cos(theta) * t_max
        t_points = np.linspace(0, t_max, 100)
        y = h + u * np.sin(theta) * t_points - 0.5 * g * t_points**2
        x = u * np.cos(theta) * t_points

        # Create graph
        path = VMobject()
        path.set_points_as_corners([*zip(x, y)])
        path.set_stroke(color=BLUE)

        # Velocity vectors
        def velocity_at(t):
            vx = u * np.cos(theta)
            vy = u * np.sin(theta) - g * t
            return np.array([vx, vy, 0])

        def position_at(t):
            px = u * np.cos(theta) * t
            py = h + u * np.sin(theta) * t - 0.5 * g * t**2
            return np.array([px, py, 0])

        # Create dots and vectors
        dot = Dot().move_to(position_at(0))
        velocity_vector = Arrow(start=ORIGIN, end=velocity_at(0) / 3, color=RED)
        vx_vector = Arrow(start=ORIGIN, end=velocity_at(0)[0] * RIGHT / 3, color=GREEN)
        vy_vector = Arrow(start=ORIGIN, end=velocity_at(0)[1] * UP / 3, color=GREEN)

        self.add(path)
        self.add(dot)
        self.add(velocity_vector)
        self.add(vx_vector)
        self.add(vy_vector)

        # Animations
        def update_dot(mob, dt):
            t = self.time + dt
            mob.move_to(position_at(t))

        def update_velocity(mob, dt):
            t = self.time + dt
            mob.put_start_and_end_on(ORIGIN, velocity_at(t) / 3)

        def update_vx(mob, dt):
            t = self.time + dt
            mob.put_start_and_end_on(ORIGIN, velocity_at(t)[0] * RIGHT / 3)

        def update_vy(mob, dt):
            t = self.time + dt
            mob.put_start_and_end_on(ORIGIN, velocity_at(t)[1] * UP / 3)

        dot.add_updater(update_dot)
        velocity_vector.add_updater(update_velocity)
        vx_vector.add_updater(update_vx)
        vy_vector.add_updater(update_vy)

        self.add(dot, velocity_vector, vx_vector, vy_vector)

        # Annotations
        self.play(FadeIn(Text("No air resistance", font_size=24).to_edge(UP + RIGHT)))
        self.play(FadeIn(Text("i.e., an inverted parabolic trajectory", font_size=24, color=BLACK).to_edge(RIGHT)))

        self.wait(t_max)

        # Clear updaters
        dot.remove_updater(update_dot)
        velocity_vector.remove_updater(update_velocity)
        vx_vector.remove_updater(update_vx)
        vy_vector.remove_updater(update_vy)

        # Draw velocity vectors at a specific point
        t_specific = t_max / 2  # example time for a specific point
        self.play(dot.animate.move_to(position_at(t_specific)))
        self.play(velocity_vector.animate.put_start_and_end_on(ORIGIN, velocity_at(t_specific) / 3))
        self.play(vx_vector.animate.put_start_and_end_on(ORIGIN, velocity_at(t_specific)[0] * RIGHT / 3))
        self.play(vy_vector.animate.put_start_and_end_on(ORIGIN, velocity_at(t_specific)[1] * UP / 3))

        # Labels
        v_label = MathTex("v", color=RED).next_to(velocity_vector.get_end(), UR, buff=0.1)
        vx_label = MathTex("v_x", color=GREEN).next_to(vx_vector.get_end(), DOWN, buff=0.1)
        vy_label = MathTex("v_y", color=GREEN).next_to(vy_vector.get_end(), LEFT, buff=0.1)
        self.play(Write(v_label), Write(vx_label), Write(vy_label))

        self.wait(2)

        # Labels for initial conditions
        u_vector = Arrow(start=ORIGIN, end=u * np.array([np.cos(theta), np.sin(theta), 0]) / 3, color=RED)
        u_label = MathTex("u", color=RED).next_to(u_vector.get_end(), UR, buff=0.1)
        self.play(FadeIn(u_vector), Write(u_label))

        theta_arc = Arc(radius=1, start_angle=0, angle=theta, color=RED)
        theta_label = MathTex("\\theta", color=RED).next_to(theta_arc, RIGHT, buff=0.1)
        self.play(FadeIn(theta_arc), Write(theta_label))

        self.wait(2)

