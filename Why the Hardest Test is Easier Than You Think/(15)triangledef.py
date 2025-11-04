from manim import *

class DynamicTriangle(Scene):
    def construct(self):
        # Initial positions
        center = np.array([0, 0, 0])
        left = np.array([-2, -1, 0])
        right = np.array([2, -1, 0])

        # Create dots
        dot_center = Dot(center, color=WHITE, radius=0.1)
        dot_left = Dot(left, color=WHITE, radius=0.1)
        dot_right = Dot(right, color=WHITE, radius=0.1)

        # Labels with always_redraw so they follow their dots
        label_center = always_redraw(lambda: Text("A").scale(0.75).next_to(dot_center, UP))
        label_left = always_redraw(lambda: Text("B").scale(0.75).next_to(dot_left, LEFT))
        label_right = always_redraw(lambda: Text("C").scale(0.75).next_to(dot_right, RIGHT))

        # Triangle fill and outline
        triangle_fill = always_redraw(lambda: Polygon(
            dot_center.get_center(),
            dot_left.get_center(),
            dot_right.get_center(),
            fill_color=GREEN,
            fill_opacity=0.5,
            stroke_width=0
        ))
        triangle_outline = always_redraw(lambda: Polygon(
            dot_center.get_center(),
            dot_left.get_center(),
            dot_right.get_center(),
            color=GREEN,
            stroke_width=2
        ))

        # Add everything to the scene
        self.play(Write(dot_center),
                  Write(dot_left),
                  Write(dot_right),
                  Write(label_center),
                  Write(label_left),
                  Write(label_right),
                  run_time=2)
        self.wait(1)
        self.play(Write(triangle_fill),
                  Write(triangle_outline))
        self.wait(2)
        # Animate large movements of outer points
        self.play(
            dot_left.animate.move_to([-5, 3, 0]),
            dot_right.animate.move_to([5, 2, 0]),
            run_time=2
        )
        self.wait()

        # Move them again to a different shape
        self.play(
            dot_left.animate.move_to([-4, -2, 0]),
            dot_right.animate.move_to([4, -3, 0]),
            run_time=2
        )
        self.wait(2)
