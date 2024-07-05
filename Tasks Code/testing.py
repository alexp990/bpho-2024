from manim import *

class ScrollNumber(Scene):
    def construct(self):
        # Create a ValueTracker to keep track of the variable
        value_tracker = ValueTracker(0)

        # Create a DecimalNumber that displays the value of the ValueTracker
        number = DecimalNumber(value_tracker.get_value(), show_ellipsis=False)
        number.add_updater(lambda n: n.set_value(value_tracker.get_value()))

        # Position the number on screen
        number.to_edge(UP)

        # Add the number to the scene
        self.add(number)

        # Animate the change in the ValueTracker
        self.play(value_tracker.animate.set_value(100), run_time=5, rate_func=linear)

        # Hold the final state on screen
        self.wait()

# To render the scene, run:
# manim -pql scroll_number.py ScrollNumber
