from manim import *
import numpy as np
from manim import rate_functions as rf

class TriangleInequalityDemo(Scene):
    def construct(self):
        # Initial lengths
        length1 = 2.3
        length2 = 2.84
        length3 = 2.4

        y_offsets = [-1.5, 0, 1.5]

        # Initial start points (horizontal layout)
        start1 = LEFT * length1 / 2 + UP * y_offsets[0]
        start2 = LEFT * length2 / 2 + UP * y_offsets[1]
        start3 = LEFT * length3 / 2 + UP * y_offsets[2]

        end1 = start1 + RIGHT * length1
        end2 = start2 + RIGHT * length2
        end3 = start3 + RIGHT * length3

        # Create lines
        line1 = Line(start1, end1, color=BLUE, stroke_width=10)
        line2 = Line(start2, end2, color=GREEN, stroke_width=10)
        line3 = Line(start3, end3, color=RED, stroke_width=10)

        # Center group of lines
        lines = VGroup(line1, line2, line3).move_to(ORIGIN)
        self.play(Write(lines))
        self.wait(0.5)

        # Elongate green line
        new_length2 = 7
        green_start = line2.get_start()
        green_end = green_start + RIGHT * new_length2
        self.play(
            Transform(line2, Line(green_start, green_end, color=GREEN, stroke_width=10)),
            run_time=1.5
        )
        self.wait()
        new_line1 = Line([-3.49909844, -1.495,  0        ], [-3.02090156,  0.70486974,  0        ], color=BLUE, stroke_width=10)
        new_line3 = Line([1.70822621, 0.1095673, 0.        ], [ 3.49177379, -1.52295673,  0.        ], color=RED, stroke_width=10)
        # Rotate short lines to prep for placement (visually flared out)
        self.play(
            # Rotate(line1, angle=78 * DEGREES),
            # Rotate(line3, angle=-42 * DEGREES),
            Transform(line1, new_line1),
            Transform(line3, new_line3),
            line2.animate.move_to(ORIGIN+DOWN*1.5),
            run_time=3
        )
        # self.play(
        #     line1.animate.move_to(line2.get_start()+UP*1.08+RIGHT*0.24),
        #     line3.animate.move_to(line2.get_end()+UP*0.78+LEFT*0.9),
        #     run_time=2
        # )
        # print(f"{line1.get_start()} , {line1.get_end()},{line3.get_start()}, {line3.get_end()} ")
        self.wait()
        
        self.play(
            Rotate(line1, angle=-71 * DEGREES, about_point=line1.get_start()),
            Rotate(line3, angle=35 * DEGREES, about_point=line3.get_end()),
            run_time=2,
            rate_func=rf.ease_in_quad  # Speeds up over time
        )
        self.wait(5)
        self.play(FadeOut(line1), FadeOut(line3), run_time=1)
        self.wait(0.5)

        # Lengths for new segments that add up to line2's length (7 units)
        seg1_len = 3.2
        seg2_len = 3.8

        # Create new segments
        seg1 = Line(LEFT * (seg1_len / 2), RIGHT * (seg1_len / 2), color=BLUE, stroke_width=10)
        seg2 = Line(LEFT * (seg2_len / 2), RIGHT * (seg2_len / 2), color=RED, stroke_width=10)

        # Move seg1 and seg2 so they're aligned end-to-end above line2
        seg1.shift(UP * 1 + LEFT * (seg2_len / 2))
        seg2.shift(UP * 1 + RIGHT * (seg1_len / 2))

        self.play(Write(VGroup(seg1, seg2)), run_time=2)
        self.wait()
        # self.play(
        #     Rotate(seg1, angle=82 * DEGREES, about_point=line1.get_start()),
        #     Rotate(seg2, angle=-56 * DEGREES, about_point=line3.get_end()),
        #     run_time=2,
        #     rate_func=rf.ease_in_quad  # Speeds up over time
        # )
        new_seg1 = Line([-3.46767696, -1.49442891,  0.        ] , [-3.02232304,  1.67442891,  0.        ], color=BLUE, stroke_width=10)
        new_seg2 = Line([1.36753348, 1.64517139, 0.        ], [ 3.49246652, -1.50517139,  0.], color=RED, stroke_width=10)

        self.play(
            Transform(seg1, new_seg1),
            Transform(seg2, new_seg2),
            run_time = 1
            )
        self.wait()
        # self.play(
        #     seg1.animate.move_to(line2.get_start()+UP*1.59+RIGHT*0.255),
        #     seg2.animate.move_to(line2.get_end()+UP*1.57+LEFT*1.07),
        # )
        print(f"{seg1.get_start()} , {seg1.get_end()},{seg2.get_start()}, {seg2.get_end()} ")

        self.play(
            Rotate(seg1, angle=-82 * DEGREES, about_point=seg1.get_start()),
            Rotate(seg2, angle=56 * DEGREES, about_point=seg2.get_end()),
            run_time=1,
            rate_func=rf.ease_in_quad  # Speeds up over time
        )
        # Calculate midpoint of the new segments
        midpoint = (seg1.get_start() + seg2.get_end()) / 2

        # Calculate vertical shift so the pair is centered above line2
        target_y = line2.get_center()[1] + 2.5  # adjust offset as desired
        delta_y = target_y - midpoint[1]

        # Shift both segments upward by delta_y to center them
        self.play(
            seg1.animate.shift(UP * delta_y),
            seg2.animate.shift(UP * delta_y),
            run_time=1.5
        )
        self.wait(3)
        # print(f"{seg1.get_start()} , {seg1.get_end()},{seg2.get_start()}, {seg2.get_end()} ")
        newline = Line(seg2.get_start(), seg2.get_end()+RIGHT*1.5, color=RED, stroke_width=10)
        self.play(
            Transform(seg2, newline),
            run_time = 1
        )
        # self.play(
        #     Rotate(seg1, angle=82 * DEGREES, about_point=seg1.get_start()),
        #     Rotate(seg2, angle=-56 * DEGREES, about_point=seg2.get_end()),
        #     run_time=1,
        #     rate_func=rf.ease_in_quad  # Speeds up over time
        # )
        # self.play(
        #     seg1.animate.move_to(line2.get_start()+UP*1.57+RIGHT*0.24),
        #     seg2.animate.move_to(line2.get_end()+UP*2.18+LEFT*1.5),
        #     run_time=2
        # )
        new_seg1 = Line([-3.48267696, -1.51442891,  0.        ] , [-3.03732304,  1.65442891,  0.        ], color=BLUE, stroke_width=10)
        new_seg2 = Line([0.5181388,  2.87694957, 0.        ], [ 3.4818612,  -1.51694957,  0.], color=RED, stroke_width=10)

        self.play(
            Transform(seg1, new_seg1),
            Transform(seg2, new_seg2),
            run_time = 1
        )

        # print(f"{seg1.get_start()} , {seg1.get_end()},{seg2.get_start()}, {seg2.get_end()} ")
        self.wait()
        self.play(
            Rotate(seg1, angle=-35.7 * DEGREES, about_point=seg1.get_start()),
            Rotate(seg2, angle=30.3 * DEGREES, about_point=seg2.get_end()),
            run_time=1,
            rate_func=rf.ease_in_quad  # Speeds up over time
        )
        self.wait(3)