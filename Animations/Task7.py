"""Fix initial conditions"""

from manim import *
import numpy as np
import subprocess

u = 10.0  
g = 9.81  
h = 0
dt = 1/1000

def r(u, g, theta, t):
    return np.sqrt(u**2 * t**2 - g * t**3 * u * np.sin(theta) + 0.25 * g**2 * t**4)

def compute_t_min(u, g, theta):
    discriminant = (9 * u**2 * np.sin(theta)**2) / (4 * g**2) - (2 * u**2) / (g**2)
    if discriminant < 0:
        return None
    term = np.sqrt(discriminant)
    t2 = (3 * u * np.sin(theta)) / (2 * g) - term
    if t2 > 0:
        return t2
    else:
        return None  

def compute_t_max(u, g, theta):
    discriminant = (9 * u**2 * np.sin(theta)**2) / (4 * g**2) - (2 * u**2) / (g**2)
    if discriminant < 0:
        return None
    term = np.sqrt(discriminant)
    t1 = (3 * u * np.sin(theta)) / (2 * g) + term
    if t1 > 0:
        return t1
    else:
        return None 

def projectile_motion(u, g, theta, t):
    x = u * t * np.cos(theta)
    y = u * t * np.sin(theta) - 0.5 * g * t**2
    return x, y

class Task6(Scene):
    def construct(self):
        theta_degrees = np.arange(45, 90, 5)
        
        # Create axes for "Range vs Time"
        ax1 = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 15, 2.5],
            axis_config={"color": BLUE}
        ).to_edge(UP).add_coordinates()

        

        # Create axes for "Displacement"
        ax2 = Axes(
            x_range=[0, 15, 5],
            y_range=[0, 5, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN).add_coordinates()


        VGroup(ax1, ax2).arrange(UP, buff=1).scale_to_fit_height(7).to_edge(LEFT)

        labels1 = Tex("x displacement (m)")
        labels1.next_to(ax2, DOWN*0.5).scale(0.5).shift(UP*0.15)
        labels2 = Tex("y displacement (m)").rotate(PI/2)
        labels2.next_to(ax2, LEFT*0.5).scale(0.5).shift(RIGHT*0.15)

        labels3 = Tex("time(s) (m)")
        labels3.next_to(ax1, DOWN*0.5).scale(0.5).shift(UP*0.15)
        labels4 = Tex("range (m)").rotate(PI/2)
        labels4.next_to(ax1, LEFT*0.5).scale(0.5).shift(RIGHT*0.15)

        #Initial conditions
        u_initial_condition = MathTex(r"u = " + f"{u} \, \t{{m/s}}")
        theta_vals_initial_condition = Tex(r"Theta values from $45^\circ$ to $90^\circ$, incremented by $5^\circ$").scale(0.6).shift(LEFT * 2)
        h_initial_condition = MathTex(r"h = " + f"{h} \, \t{{m}}")

        initial_conditions = VGroup(u_initial_condition, h_initial_condition).arrange(DOWN, buff=0.4).scale(0.6).to_corner(UR).shift(DOWN * 0.5).shift(LEFT * 2)
        theta_vals_initial_condition.next_to(initial_conditions, UP)

        self.play(
            Create(ax1), Create(labels1), 
            Create(labels3), Create(labels4),
            Create(ax2), Create(labels2),
            Write(initial_conditions),
            Write(theta_vals_initial_condition),
            run_time=1
        )

        range_plots = []
        displacement_plots = []
        dots_to_show = []

        for theta_deg in theta_degrees:
            theta = np.deg2rad(theta_deg)
            range_val = u**2 / g * (np.sin(theta) * np.cos(theta) + np.cos(theta) * np.sqrt(np.square(np.sin(theta)) + (2 * g * h) / np.square(u)))
            tof = range_val / (u * np.cos(theta))
            ts = np.arange(0, tof, dt)

            # Range vs Time
            range_values = r(u, g, theta, ts)
            range_plot = ax1.plot_line_graph(
                x_values=ts,
                y_values=range_values,
                line_color=BLUE,
                add_vertex_dots=False
            )
            range_plots.append(range_plot)

            t_max = compute_t_max(u, g, theta)
            t_min = compute_t_min(u, g, theta)

            if t_max is not None and t_min is not None:
                range_max = r(u, g, theta, t_max)
                range_min = r(u, g, theta, t_min)
                t_max_dot = Dot(ax1.c2p(t_max, range_max), color=RED)
                t_min_dot = Dot(ax1.c2p(t_min, range_min), color=PINK)
                dots_to_show.append(t_max_dot)
                dots_to_show.append(t_min_dot)

            # Displacement
            x_positions = []
            y_positions = []

            for t in ts:
                x, y = projectile_motion(u, g, theta, t)
                x_positions.append(x)
                y_positions.append(y)

            displacement_plot = ax2.plot_line_graph(
                x_values=x_positions,
                y_values=y_positions,
                line_color=GREEN,
                add_vertex_dots=False
            )
            displacement_plots.append(displacement_plot)

            if t_max is not None and t_min is not None:
                x_max, y_max = projectile_motion(u, g, theta, t_max)
                x_min, y_min = projectile_motion(u, g, theta, t_min)
                x_max_dot = Dot(ax2.c2p(x_max, y_max), color=RED)
                x_min_dot = Dot(ax2.c2p(x_min, y_min), color=PINK)
                dots_to_show.append(x_max_dot)
                dots_to_show.append(x_min_dot)

        max_dots_label_dot = Dot(color=PINK).next_to(initial_conditions, DOWN*1.3).shift(LEFT * 2.5)
        max_dots_label_text = Tex(r"maximum point on range vs time graph").next_to(max_dots_label_dot, RIGHT*0.2).scale(0.6).shift(LEFT*1.7)

        min_dots_label_dot = Dot(color=RED).next_to(initial_conditions, DOWN*2.8).shift(LEFT * 2.5)
        min_dots_label_text = Tex(r"minimum point on range vs time graph").next_to(min_dots_label_dot, RIGHT*0.2).scale(0.6).shift(LEFT*1.7)

        range_label_eq = MathTex(r"r = \sqrt{u^2 t^2 - g t^3 u \sin{\theta} + \frac{1}{4} g^2 t^4}")
        t_plus_minus_eq = MathTex(r"t_{\pm} = \frac{3u}{2g} \left( \sin{\theta} \pm \sqrt{\sin^2{\theta} - \frac{8}{9}} \right)")
        theta_geq_eq = MathTex(r"\theta \geq \arcsin{\frac{2 \sqrt{2}}{3}}} \approx 70.5^\circ")

        equations = VGroup(range_label_eq, t_plus_minus_eq, theta_geq_eq).arrange(DOWN, buff=0.3).next_to(initial_conditions, DOWN * 3.5).scale(0.6)

        self.play(*[Create(plot) for plot in range_plots + displacement_plots], Write(equations), run_time=3)
        self.play(*[FadeIn(dot) for dot in dots_to_show], Create(max_dots_label_dot), Write(max_dots_label_text), Create(min_dots_label_dot), Write(min_dots_label_text), run_time=1)

        self.wait(4)




