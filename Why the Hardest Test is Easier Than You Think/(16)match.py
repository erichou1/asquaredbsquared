from manim import *
import numpy as np

class TwoDTriangle(MovingCameraScene):
    def construct(self):
        # Triangle vertices
        v1 = np.array([-3.22, -3, 0])  # A
        v2 = np.array([3.22, -3, 0])   # B
        v3 = np.array([0.0, 2.7, 0])   # C

        # Original triangle for reference
        triangle = Polygon(v1, v2, v3, color=GREEN, fill_opacity=1, stroke_width=3)

        # Labels
        labels_text = ["A", "B", "C"]
        label_positions = [v1, v2, v3]
        labels = VGroup()
        for i, pos in enumerate(label_positions):
            direction = pos / np.linalg.norm(pos) if np.linalg.norm(pos) != 0 else UP
            label = Text(labels_text[i], weight=BOLD).scale(0.8)
            label.next_to(pos, direction, buff=0.3)
            labels.add(label)

        # Move paths for dots
        line1 = Line(v1 + np.array([0.6, 0, 0]), v2 + np.array([-4, 0, 0]))
        line2 = Line(v1 + np.array([0.45, 0.796583853, 0]), v3 + np.array([-1, -1.77018634, 0]))

        # Moving dots
        moving_dot1 = Dot(color=WHITE, radius=0.2).move_to(line1.get_start())
        moving_dot2 = Dot(color=WHITE, radius=0.2).move_to(line2.get_start())
        label1 = Text("M", weight=BOLD).scale(0.7)
        label2 = Text("N", weight=BOLD).scale(0.7)


        label1.add_updater(lambda m: m.next_to(moving_dot1, UR, buff=0.2))
        label2.add_updater(lambda m: m.next_to(moving_dot2, UR, buff=0.2))

        self.add(triangle, labels, moving_dot1, moving_dot2, label1, label2)

        # Dynamic lines connecting dots and fixed points
        lineMN = always_redraw(lambda: Line(moving_dot1.get_center(), moving_dot2.get_center(), color=BLUE, stroke_width=8))
        lineBN = always_redraw(lambda: Line(v2, moving_dot2.get_center(), color=RED, stroke_width=8))
        lineCM = always_redraw(lambda: Line(v3, moving_dot1.get_center(), color=ORANGE, stroke_width=8))

        self.add(lineMN, lineBN, lineCM)

        # Animate dots moving along their paths
        self.play(
            MoveAlongPath(moving_dot1, line1),
            MoveAlongPath(moving_dot2, line2),
            run_time=2, rate_func=linear
        )
        self.wait()

        # Final points of the moving dots
        point_M = moving_dot1.get_center()
        point_N = moving_dot2.get_center()

        # Lengths of segments after dots move
        len_MN = np.linalg.norm(point_N - point_M)
        len_BN = np.linalg.norm(v2 - point_N)
        len_CM = np.linalg.norm(v3 - point_M)

        # Make copies of the final lines (static)
        lineMN_copy = Line(point_M, point_N, color=BLUE, stroke_width=8)
        lineBN_copy = Line(point_N, v2, color=RED, stroke_width=8)
        lineCM_copy = Line(v3, point_M, color=ORANGE, stroke_width=8)

        self.add(lineMN_copy, lineBN_copy, lineCM_copy)

        # Remove dynamic lines
        for line in [lineMN, lineBN, lineCM]:
            line.clear_updaters()
            self.remove(line)

        # Move camera right to make space
        self.play(self.camera.frame.animate.shift(RIGHT * 5), run_time=1)

        ### Position the base (MN) horizontally at new location
        base_start = RIGHT * 6 + DOWN * 1
        base_end = base_start + np.array([len_MN, 0, 0])

        # Calculate third vertex position (point P) using Law of Cosines
        try:
            angle = np.arccos(
                (len_MN**2 + len_CM**2 - len_BN**2) / (2 * len_MN * len_CM)
            )
        except ValueError:
            angle = 0  # handle edge case for floating point errors

        point_P = base_start + np.array([
            len_CM * np.cos(angle),
            len_CM * np.sin(angle),
            0
        ])

        # Compute centroid of the three points defining the triangle
        centroid = (base_start + base_end + point_P) / 3

        # Desired vertical center (e.g., y=0)
        desired_y = 0

        # Calculate vertical shift needed
        vertical_shift = desired_y - centroid[1]-1

        # Shift points vertically to center the triangle
        shift_vector = np.array([0, vertical_shift, 0])
        base_start += shift_vector
        base_end += shift_vector
        point_P += shift_vector

        # Animate lines to the shifted points (triangle is vertically centered now)
        self.play(lineMN_copy.animate.put_start_and_end_on(base_start, base_end), run_time=1)
        self.play(lineCM_copy.animate.put_start_and_end_on(point_P, base_start), run_time=1)
        self.play(lineBN_copy.animate.put_start_and_end_on(point_P, base_end), run_time=1)
        filled_triangle = Polygon(base_start, base_end, point_P,
                                  color=WHITE, fill_color=GREEN, fill_opacity=0.6, stroke_width=0)
        filled_triangle.set_z_index(-1)
        self.play(Write(filled_triangle))
        self.wait(2)
        self.play(self.camera.frame.animate.shift(LEFT * 5),
                filled_triangle.animate.set_fill(opacity=0), 
                lineMN_copy.animate.set_opacity(0), 
                lineCM_copy.animate.set_opacity(0), 
                lineBN_copy.animate.set_opacity(0), 
                run_time=1
                  )
