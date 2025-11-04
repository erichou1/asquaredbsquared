from manim import *
import numpy as np

class TwoDTriangle(Scene):
    def construct(self):
        # Coordinate plane
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.8}
        )
        self.add(plane)
        # plane.z_index = 1
        # Triangle vertices
        v1 = np.array([-3.22, -3, 0])  # A
        v2 = np.array([3.22, -3, 0])   # B
        v3 = np.array([0.0, 2.7, 0])   # C

        triangle = Polygon(v1, v2, v3, color=GREEN, fill_opacity=1, stroke_width=3)

        # Vertex labels
        labels_text = ["A", "B", "C"]
        label_positions = [v1, v2, v3]
        labels = VGroup()
        for i, pos in enumerate(label_positions):
            direction = pos / np.linalg.norm(pos) if np.linalg.norm(pos) != 0 else UP
            label = Text(labels_text[i], weight=BOLD).scale(0.8)
            label.next_to(pos, direction, buff=0.3)
            labels.add(label)

        # Auxiliary lines
        line1 = Line(v1+ np.array([0.6, 0, 0]), v2 + np.array([-2, 0, 0]))
        line2 = Line(v1+np.array([0.45, 0.796583853, 0]), v3 + np.array([-1, -1.77018634, 0]))
        line3 = Line(v2 + np.array([-1.2, 0, 0]), v1+ np.array([0.6, 0, 0]))
        line4 = Line(v3 + np.array([-1, -1.77018634, 0]), v3 + np.array([-2, -3.54037268, 0]))

        # Moving dots
        moving_dot1 = Dot(color=WHITE, radius=0.2)
        moving_dot2 = Dot(color=WHITE, radius=0.2)
        moving_dot1.move_to(v2 + np.array([-1.2, 0, 0]))
        moving_dot2.move_to(v1+np.array([0.45, 0.796583853, 0]))

        # Coordinate labels
        coord1 = always_redraw(
            lambda: MathTex(
                f"({moving_dot1.get_x():.2f}, {moving_dot1.get_y():.2f})"
            ).scale(0.6).next_to(moving_dot1, UR, buff=0.2)
        )
        coord2 = always_redraw(
            lambda: MathTex(
                f"({moving_dot2.get_x():.2f}, {moving_dot2.get_y():.2f})"
            ).scale(0.6).next_to(moving_dot2, UR, buff=0.2)
        )        
        coord1.add_updater(lambda m: m.next_to(moving_dot1, UR, buff=0.2))
        coord2.add_updater(lambda m: m.next_to(moving_dot2, UR, buff=0.2))

        coord1.next_to(moving_dot1, UR, buff=0.25)
        coord2.next_to(moving_dot2, UR, buff=0.25)
        
        # Add everything
        self.add(triangle, labels)
        self.add(moving_dot1, moving_dot2)
        self.add(coord1, coord2)
        self.add(line1, line2, line3, line4)
        for line in [line1, line2, line3, line4]:
            line.set_opacity(0)
        self.add(line1, line2, line3, line4)
        self.play(MoveAlongPath(moving_dot1, line3),
                MoveAlongPath(moving_dot2, line2), run_time=2, rate_func=linear
        )
        self.wait(0.1)
        self.play(MoveAlongPath(moving_dot1, line1),
                  MoveAlongPath(moving_dot2, line4, rate_func=linear), run_time=1.5, rate_func=linear
                  )
    
        self.wait()
