from manim import *
import numpy as np

class TwoDTriangle(Scene):
    def construct(self):
        scale_factor = 3

        v1 = np.array([-3.22, -3, 0])  # A
        v2 = np.array([3.22, -3, 0])   # B
        v3 = np.array([0.0, 2.7, 0])   # C

        triangle = Polygon(v1, v2, v3, color=GREEN, fill_opacity=1, stroke_width=3)

        labels_text = ["A", "B", "C"]
        label_positions = [v1, v2, v3]
        labels = VGroup()
        for i, pos in enumerate(label_positions):
            direction = pos / np.linalg.norm(pos) if np.linalg.norm(pos) != 0 else UP
            label = Text(labels_text[i], weight=BOLD).scale(0.8)
            label.next_to(pos, direction, buff=0.3)
            labels.add(label)

        line1 = Line(v1, v2 + np.array([-1.2, 0, 0]))
        line2 = Line(v1, v3 + np.array([-1, -1.77018634, 0]))
        line3 = Line(v2 + np.array([-1.2, 0, 0]), v2 + np.array([-3.25, 0, 0]))
        line4 = Line(v3 + np.array([-1, -1.77018634, 0]), v3 + np.array([-2, -3.54037268, 0]))
        line5 = Line(v2 + np.array([-3.25, 0, 0]), v2 + np.array([-4, 0, 0]))
        line6 = Line(v3 + np.array([-2, -3.54037268, 0]), v3 + np.array([-1.5, -2.38975156, 0]))
        moving_dot1 = Dot(color=WHITE, radius=0.2)
        moving_dot2 = Dot(color=WHITE, radius=0.2)
        label1 = Text("M", weight=BOLD).scale(0.7)
        label2 = Text("N", weight=BOLD).scale(0.7)

        moving_dot1.move_to(v1)
        moving_dot2.move_to(v1)

        label1.add_updater(lambda m: m.next_to(moving_dot1, UR, buff=0.2))
        label2.add_updater(lambda m: m.next_to(moving_dot2, UR, buff=0.2))

        self.add(triangle)
        self.play(Write(labels), run_time=2)
        self.wait(0.5)

        self.add(moving_dot1, label1)
        self.play(MoveAlongPath(moving_dot1, line1), run_time=1.5, rate_func=linear)
        self.play(MoveAlongPath(moving_dot1, line3), run_time=1.5, rate_func=linear)

        self.add(moving_dot2, label2)
        self.play(
            AnimationGroup(
                Write(moving_dot2, run_time=0.5),
                moving_dot1.animate(run_time=1).set_fill(opacity=0.5),
                label1.animate(run_time=1).set_fill(opacity=0.5),
                AnimationGroup(
                    MoveAlongPath(moving_dot2, line2),
                    MoveAlongPath(moving_dot2, line4, rate_func=linear),
                    lag_ratio=1.0
                ),
                lag_ratio=0
            ),
            run_time=4.5
        )
        self.wait()

        # --- DYNAMIC SEGMENTS AND MINI TRIANGLE ---
        lineMN = Line(moving_dot1.get_center(), moving_dot2.get_center(), color=BLUE, stroke_width=8)
        lineBN  = Line(v2, moving_dot2.get_center(), color=RED,stroke_width=8)
        lineCM = Line(v3, moving_dot1.get_center(), color=YELLOW,stroke_width=8)
        self.attach_line_updater(lineMN, moving_dot1, moving_dot2, is_dot=True)
        self.attach_line_updater(lineBN, v2, moving_dot2, is_dot=False)
        self.attach_line_updater(lineCM, v3, moving_dot1, is_dot=False)

        self.play(
            moving_dot1.animate(run_time=1.5).set_fill(opacity=1),
            label1.animate(run_time=1.5).set_fill(opacity=1),
            Write(lineMN, run_time=1.5),
            Write(lineBN , run_time=1.5),
            Write(lineCM, run_time=1.5)
        )
        self.wait(2)
        self.play(
            AnimationGroup(
                MoveAlongPath(moving_dot1, line5),
                MoveAlongPath(moving_dot2, line6),
            ),
            run_time=3
        )
    def attach_line_updater(self, line, dot1, dot2, is_dot):
        """
        Attaches an updater to an existing line, making it dynamically follow the positions of two dots.

        Args:
            line: The Line3D object to update.
            dot1: The first Dot3D object.
            dot2: The second Dot3D object.
        """
        # Define the updater function
        def update_line(line):
            # Recalculate the start and end positions based on the current dot positions
            if is_dot==True:
                start_pos = dot1.get_center()
            else:
                start_pos = dot1
            end_pos = dot2.get_center()
            # print(f"{start_pos}, {end_pos}")
            line.put_start_and_end_on(start_pos, end_pos)  # Update the line's geometry
        line.add_updater(update_line)
            