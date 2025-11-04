from manim import *
import numpy as np

class TwoDTriangle(Scene):
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
        labels.z_index = 1
        # Move paths for dots
        line1 = Line(v1 + np.array([0.6, 0, 0]), v2 + np.array([-4, 0, 0]))
        line2 = Line(v1 + np.array([0.45, 0.796583853, 0]), v3 + np.array([-1, -1.77018634, 0]))
        line3 = Line(v2 + np.array([-4, 0, 0]), v2+np.array ([-2, 0, 0]))
        line4 = Line(v3 + np.array([-1, -1.77018634, 0]), v3 + np.array([-2.7, -4.77950313, 0]))
        # Moving dots
        moving_dot1 = Dot(color=WHITE, radius=0.2).move_to(line1.get_end())
        moving_dot2 = Dot(color=WHITE, radius=0.2).move_to(line2.get_end())
        label1 = Text("M", weight=BOLD).scale(0.7)
        label2 = Text("N", weight=BOLD).scale(0.7)
        label1.z_index=1
        label2.z_index=1
        moving_dot1.z_index = 1
        moving_dot2.z_index = 1

        label1.add_updater(lambda m: m.next_to(moving_dot1, UR, buff=0.2))
        label2.add_updater(lambda m: m.next_to(moving_dot2, UR, buff=0.2))

        self.add(triangle, labels, moving_dot1, moving_dot2, label1, label2)

        # Dynamic lines connecting dots and fixed points
        lineMN = always_redraw(lambda: Line(moving_dot1.get_center(), moving_dot2.get_center(), color=BLUE, stroke_width=8))
        lineBN = always_redraw(lambda: Line(v2, moving_dot2.get_center(), color=RED, stroke_width=8))
        lineCM = always_redraw(lambda: Line(v3, moving_dot1.get_center(), color=ORANGE, stroke_width=8))

        self.play(Write(lineMN), Write(lineBN), Write(lineCM))
        self.wait()
        # Arrows pointing to points B and C
        pin = SVGMobject("./pin.svg")
        pin2 = SVGMobject("./pin.svg")
        pin.scale(0.4)
        pin2.scale(0.4)
        pin.z_index = -1

        pin.rotate(-80*DEGREES)
        pin2.rotate(-80*DEGREES)
        pin.move_to(v3+np.array([0.5, 0.05, 0]))
        pin2.move_to(v2+np.array([0.45, 0.1, 0]))
        self.play(Write(pin), Write(pin2), run_time=1, rate_func=linear)
        self.wait()
        self.play(MoveAlongPath(moving_dot1, line3),
                  MoveAlongPath(moving_dot2, line4), run_time=1.5)
        self.wait()
        dashed_lineMN = always_redraw(lambda: DashedLine(
            moving_dot1.get_center(),
            moving_dot2.get_center(),
            color=BLUE,
            stroke_width=8,
            dashed_ratio=0.6,  # 30% dash, 70% gap
            dash_length=0.35    # length of each dash+gap segment
))
        dashed_lineBN = always_redraw(lambda: DashedLine(
            v2,
            moving_dot2.get_center(),
            color=RED,
            stroke_width=8,
            dashed_ratio=0.6,  # 30% dash, 70% gap
            dash_length=0.35    # length of each dash+gap segment

        ))
        dashed_lineCM = always_redraw(lambda: DashedLine(
            v3,
            moving_dot1.get_center(),
            color=ORANGE,
            stroke_width=8,
            dashed_ratio=0.6,  # 30% dash, 70% gap
            dash_length=0.35    # length of each dash+gap segment

        ))
        self.play(
            FadeOut(lineMN, run_time=1),
            FadeOut(lineBN, run_time=1),
            FadeOut(lineCM, run_time=1),
            FadeIn(dashed_lineMN),
            FadeIn(dashed_lineBN),
            FadeIn(dashed_lineCM),
        )
        self.wait(0.5)
        self.play(
            moving_dot1.animate.set_fill(color="#D3AF37"), run_time = 0.75

        )
        self.play(
            moving_dot2.animate.set_fill(color="#D3AF37"), run_time = 0.75
        )
                # Create a dashed golden-outlined circle (as the dot)
        base_circle = Circle(
            radius=0.2,
            stroke_color=WHITE,
            stroke_width=7,
            fill_color=BLACK,
            fill_opacity=0
        )


        # Question mark inside the circle (bold)
        question_mark = Text("?", color=WHITE, weight=BOLD).scale(0.5)
        question_mark.move_to(base_circle.get_center())

        # Group the circle and the question mark
        question_group = VGroup(base_circle, question_mark)

        # Initial position and group add
        outside_position = v1 + LEFT * 1.5 + UP * 0.5
        question_group.move_to(outside_position)
        self.play(Write(question_group))
        self.wait(0.5)

        # List of target points for gliding
        glide_targets = [
            moving_dot1.get_center() + UP * 3+LEFT*5.9,
            moving_dot1.get_center() + UP * 5.6+RIGHT*0.6,     # Near M
            moving_dot2.get_center() + RIGHT * 6,  # Near N
            moving_dot2.get_center()+RIGHT*2,  # Near N
        ]

        # Animate through all positions
        for target in glide_targets:
            self.play(question_group.animate.move_to(target), run_time=1.2)
        self.wait(1)
        