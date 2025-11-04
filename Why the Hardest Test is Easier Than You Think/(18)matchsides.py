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
        labels.z_index = 1
        # Move paths for dots
        line1 = Line(v1 + np.array([0.6, 0, 0]), v2 + np.array([-4, 0, 0]))
        line2 = Line(v1 + np.array([0.45, 0.796583853, 0]), v3 + np.array([-1, -1.77018634, 0]))
        line3 = Line(v2 + np.array([-4, 0, 0]), v2+np.array ([-2, 0, 0]))
        line4 = Line(v3 + np.array([-1, -1.77018634, 0]), v3 + np.array([-2.7, -4.77950313, 0]))

        # Moving dots
        moving_dot1 = Dot(color=WHITE, radius=0.2).move_to(line1.get_end())
        moving_dot2 = Dot(color=WHITE, radius=0.2).move_to(line2.get_end())
        label1 = Text("M", weight=BOLD).scale(0.8)
        label2 = Text("N", weight=BOLD).scale(0.8)

        moving_dot1.z_index = 1
        moving_dot2.z_index = 1
        label1.add_updater(lambda m: m.next_to(moving_dot1, UR, buff=0.2))
        label2.add_updater(lambda m: m.next_to(moving_dot2, UR, buff=0.2))

        self.add(triangle, labels, moving_dot1, moving_dot2, label1, label2)

        # Dynamic lines connecting dots and fixed points
        lineMN = always_redraw(lambda: Line(moving_dot1.get_center(), moving_dot2.get_center(), color=BLUE, stroke_width=8))
        lineBN = always_redraw(lambda: Line(v2, moving_dot2.get_center(), color=RED, stroke_width=8))
        lineCM = always_redraw(lambda: Line(v3, moving_dot1.get_center(), color=ORANGE, stroke_width=8))

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
        self.add(pin, pin2)
        moving_dot1.move_to(line3.get_end())
        moving_dot2.move_to(line4.get_end())
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
        self.add(dashed_lineBN, dashed_lineMN, dashed_lineCM)
        moving_dot1.set_fill(color="#D3AF37")
        moving_dot2.set_fill(color="#D3AF37")

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

        self.add(question_group)
        glide_targets = [
            moving_dot1.get_center() + UP * 3+LEFT*5.9,
            moving_dot1.get_center() + UP * 5.6+RIGHT*0.6,     # Near M
            moving_dot2.get_center() + RIGHT * 6,  # Near N
            moving_dot2.get_center()+RIGHT*2,  # Near N
        ]

        question_group.move_to(glide_targets[3])

        static_lineBN = DashedLine(
            v2,
            moving_dot2.get_center(),
            color=RED,
            stroke_width=8,
            dashed_ratio=0.6,
            dash_length=0.35
        
        )
        self.remove(dashed_lineBN)
        self.add(static_lineBN)        
        # Animate dashed_lineCM's stroke_width to 0
        self.play(
            Succession(
                AnimationGroup(
                    FadeOut(question_group),
                    FadeOut(pin),
                    FadeOut(pin2),
                    lag_ratio=0
                ),
                Wait(0.1),  # Proper delay between groups
                AnimationGroup(
                    FadeOut(dashed_lineCM), 
                    static_lineBN.animate.set_stroke(opacity=0.8),
                    lag_ratio=0
                )
            ),
            run_time = 2
        )

        # Create a solid line to trace dashed_lineMN's path
        traced_line = Line(
            start=moving_dot2.get_center(),
            end=moving_dot2.get_center(),  # Start as a point
            color=BLUE,
            stroke_width=15
        )

        self.add(traced_line)

        # Animate the traced_line to extend to moving_dot2's position
        self.play(
            traced_line.animate.put_start_and_end_on(
                moving_dot2.get_center(),
                moving_dot1.get_center()
                
            ),
            run_time=1.5
        )

        # Optionally remove the dashed_lineMN after tracing
        self.remove(dashed_lineMN)
        # --- Perpendicular from B to line AC ---
        # Define AC vector and point B
        A = v1
        C = v3
        B = v2

        AC = C - A
        AB = B - A

        # Projection of AB onto AC
        projection_length = np.dot(AB, AC) / np.dot(AC, AC)
        foot = A + projection_length * AC  # Foot of perpendicular

        # Vector from B to foot
        perp_vector = foot - B

        # Extended point (twice the distance in the same direction)
        extended_point = B + 2 * perp_vector

        # Line from B through foot to extended point
        extended_perp_line = Line(B, extended_point, color=YELLOW, stroke_width=15)

        # Right angle marker at the foot
        right_angle = RightAngle(
            Line(A, foot), Line(foot, B), 
            length=0.4, 
            stroke_width=7,
            quadrant=(-1, 1),
            color = YELLOW
        )        # Temporarily remove updater so we can animate the label
        label2.clear_updaters()
        label1.clear_updaters()

        # Animate label N slightly lower and to the right of moving_dot2

        # Re-attach updater if you still want it to follow the dot afterward
        # Midpoints of each half of the perpendicular line
        foot_midpoint = (B + foot) / 2
        tip_midpoint = (foot + extended_point) / 2

        # Direction perpendicular to the line (use normalized vector rotated 90°)
        perp_dir = np.array([-(foot - B)[1], (foot - B)[0], 0])
        perp_dir = perp_dir / np.linalg.norm(perp_dir) * 0.5  # scale for tick length

        # Tick marks as short lines centered at each midpoint
        tick1 = Line(foot_midpoint - perp_dir / 2, foot_midpoint + perp_dir / 2, color=WHITE, stroke_width=8)
        tick2 = Line(tip_midpoint - perp_dir / 2, tip_midpoint + perp_dir / 2, color=WHITE, stroke_width=8)
        def create_ticks(p1, p2, color=WHITE, tick_len=0.4, spacing=0.07):
            """
            Creates two ticks spaced apart by `2 * spacing`, centered on the midpoint of line p1–p2.
            """
            direction = p2 - p1
            direction_norm = direction / np.linalg.norm(direction)

            # Perpendicular vector for tick orientation
            perp = np.array([-direction[1], direction[0], 0])
            perp = perp / np.linalg.norm(perp) * tick_len

            # Centered positions along the line
            mid = (p1 + p2) / 2
            offset = direction_norm * spacing

            pos1 = mid + offset
            pos2 = mid - offset

            tick1 = Line(pos1 - perp / 2, pos1 + perp / 2, color=color, stroke_width=8)
            tick2 = Line(pos2 - perp / 2, pos2 + perp / 2, color=color, stroke_width=8)

            return VGroup(tick1, tick2)
        bn_ticks = create_ticks(v2, moving_dot2.get_center())
        dn_ticks = create_ticks(extended_point, moving_dot2.get_center())
        bn_ticks.z_index = 1
        dn_ticks.z_index = 1
        self.play(
            AnimationGroup(
                label2.animate.next_to(moving_dot2, DR, buff=0.2),
                label1.animate.next_to(moving_dot1, DR, buff=0.2),
                self.camera.frame.animate.scale(1.2).move_to([-1.6625, -0.2411, 0]),
                Wait(1),  # 1 second delay before the other two
                Create(extended_perp_line),
                Create(right_angle),
                Create(tick1),
                Create(tick2),
                lag_ratio=0  # Run them in parallel, respecting the Wait
            ),
            run_time=3
        )
        label2.add_updater(lambda m: m.next_to(moving_dot2, DR, buff=0.2))
        # Label point D
        point_d = Dot(extended_point, color=YELLOW, radius = 0.2)
        label_d = Text("D", weight=BOLD).next_to(extended_point, DOWN, buff=0.3).scale(0.8)
        self.play(FadeIn(point_d), Write(label_d))


        # Highlight BM and DM as hypotenuses
        BN = Line(v2, moving_dot2.get_center(), color="#FFBF00", stroke_width = 15)
        DN = Line(extended_point, moving_dot2.get_center(), color="#FFBF00", stroke_width = 15)
        DN.z_index = -1
        extended_perp_line.z_index = 0
        # Create dashed line from N to foot of perpendicular
        dashed_NF = DashedLine(
            moving_dot2.get_center(),
            foot,
            color=YELLOW,
            stroke_width=10,
            dashed_ratio=0.6,
            dash_length=0.2
        )

        # Animate BN first, then animate DN and dashed_NF simultaneously
        self.play(
            Succession(
                Create(BN),
                Create(bn_ticks),
                AnimationGroup(
                    Create(DN),
                    Create(dashed_NF),
                    Create(dn_ticks),
                    lag_ratio=0
                )
            ),
            run_time=2
        )

        self.wait(0.5)
        # Pose the question about CM
        cm_line = Line(v3, moving_dot1.get_center(), color=ORANGE, stroke_width=15)
                # Capture the location of N
        n_point = moving_dot2.get_center().copy()

        # Create the tracing lines (initially with zero length)
        trace_BN = Line(v2, v2, color="#a4d8c2", stroke_width=16)
        trace_DN = Line(extended_point, extended_point, color="#a4d8c2", stroke_width=16)

        # Add them to the scene
        self.add(trace_BN, trace_DN)

        # Animate them being drawn from B to N and D to N
        self.play(
            trace_BN.animate.put_start_and_end_on(v2, n_point),
            run_time=1.2
        )
        self.play(
            trace_DN.animate.put_start_and_end_on(extended_point, n_point),
            run_time=1.2
        )
        triangle_fill = Polygon(
            moving_dot1.get_center(),
            moving_dot2.get_center(),
            extended_point,
            fill_color="#A4DBC3",
            fill_opacity=0,
            stroke_width=0
        )
        dota = Dot(moving_dot1.get_center(), color=RED, radius=0.2)
        dotb = Dot(moving_dot2.get_center(), color=RED, radius=0.2)
        dotc = Dot(extended_point, color=RED, radius=0.2)
        linea = Line(moving_dot1.get_center(), moving_dot2.get_center(), color=WHITE, stroke_width=16)
        lineb = Line(moving_dot2.get_center(), extended_point, color=WHITE, stroke_width=16)
        linec = Line(extended_point, moving_dot1.get_center(), color=WHITE, stroke_width=16)
        dota.z_index = 3
        dotb.z_index = 3
        dotc.z_index = 3
        linea.z_index = 2
        lineb.z_index = 2
        linec.z_index = 2
        triangle_fill.z_index = 1
        trace_BN.z_index = 0
        BN.z_index=-1
        self.play(
            AnimationGroup(
                    DN.animate.set_stroke(opacity=0),
                    traced_line.animate.set_stroke(opacity=0.25),
                    trace_DN.animate.set_stroke(opacity=0.25),
                    trace_BN.animate.set_stroke(opacity=0.5),
                    BN.animate.set_stroke(opacity=0.25),
                    dn_ticks.animate.set_stroke(opacity=0.25),
                    bn_ticks.animate.set_stroke(opacity=0.25),
                    extended_perp_line.animate.set_stroke(opacity=0.25),
                    dashed_NF.animate.set_stroke(opacity=0.25),
                    tick1.animate.set_stroke(opacity=0.25),
                    tick2.animate.set_stroke(opacity=0.25),
                    right_angle.animate.set_stroke(opacity=0.25),
                    moving_dot1.animate.set_color(RED),
                    moving_dot2.animate.set_color(RED),
                    static_lineBN.animate.set_stroke(opacity=0.25),
                    point_d.animate.set_fill(RED).set_stroke(RED).set_z_index(2),
                    Succession(
                        Write(dota),
                        Write(dotb),
                        Write(dotc),
                        Create(linea),
                        Create(lineb),
                        Create(linec),
                        triangle_fill.animate.set_fill(opacity=1)
                    ),
                    lag_ratio=0.3
                ),
                run_time=5
            )

        self.wait(2)
        self.play(Create(cm_line), run_time=2)

        # --- Perpendicular from C to line AB ---
        A = v1
        B = v2
        C = v3

        AB = B - A
        AC = C - A

        # Project AC onto AB to find foot of perpendicular
        projection_length_ce = np.dot(AC, AB) / np.dot(AB, AB)
        foot_C = A + projection_length_ce * AB

        # Vector from C to foot
        perp_vector_C = foot_C - C

        # Extend to form E
        extended_point_E = C + 2 * perp_vector_C

        # Line from C through foot to E
        extended_perp_line_C = Line(C, extended_point_E, color=YELLOW, stroke_width=15)
        extended_perp_line_C.z_index = 0
        # Right angle marker at foot_C
        right_angle_C = RightAngle(
            Line(A, foot_C), Line(foot_C, C),
            length=0.4,
            stroke_width=7,
            quadrant=(1, -1),
            color = YELLOW
        )
        label2.z_index = 1
        # Midpoints for tick marks
        foot_midpoint_C = (C + foot_C) / 2
        tip_midpoint_C = (foot_C + extended_point_E) / 2

        perp_dir_C = np.array([-(foot_C - C)[1], (foot_C - C)[0], 0])
        perp_dir_C = perp_dir_C / np.linalg.norm(perp_dir_C) * 0.5

        tick1_C = Line(foot_midpoint_C - perp_dir_C / 2, foot_midpoint_C + perp_dir_C / 2, color=WHITE, stroke_width=8)
        tick2_C = Line(tip_midpoint_C - perp_dir_C / 2, tip_midpoint_C + perp_dir_C / 2, color=WHITE, stroke_width=8)
        cm_ticks = create_ticks(v3, moving_dot1.get_center())
        em_ticks = create_ticks(extended_point_E, moving_dot1.get_center())
        cm_ticks.z_index = 1
        em_ticks.z_index = 1
        self.wait()
        self.play(
            AnimationGroup(
                self.camera.frame.animate.scale(1.4).move_to([(0.0, -3.0, 0)]),
                dota.animate.set_fill(opacity=0.9),
                dotb.animate.set_fill(opacity=0.9),
                dotc.animate.set_fill(opacity=0.9),
                linea.animate.set_stroke(opacity=0.9),
                lineb.animate.set_stroke(opacity=0.9),
                linec.animate.set_stroke(opacity=0.9),
                triangle_fill.animate.set_fill(opacity=0.9),
                cm_line.animate.set_stroke(opacity=0.25),
                Create(extended_perp_line_C),
                Create(right_angle_C),
                Create(tick1_C),
                Create(tick2_C),
                lag_ratio=0
            ),
            run_time=3
        )
        self.wait()
        # Label point E
        point_e = Dot(extended_point_E, color=YELLOW, radius=0.2)
        label_e = Text("E", weight=BOLD).next_to(extended_point_E, DOWN, buff=0.3).scale(0.8)
        self.play(FadeIn(point_e), Write(label_e))

        # Draw CE and ME
        CE = Line(C, extended_point_E, color=YELLOW, stroke_width=15)
        ME = Line(extended_point_E, moving_dot1.get_center(), color="#8377D1", stroke_width=15)
        dashed_ME = DashedLine(moving_dot1.get_center(), foot_C, color=YELLOW, stroke_width=10, dashed_ratio=0.6, dash_length=0.2)
        cm_line2 = Line(v3, moving_dot1.get_center(), color="#8377D1", stroke_width=15)
        cm_line2.z_index = 0
        ME.z_index = 0
        self.play(
            Succession(
                Create(CE),
                AnimationGroup(
                    Create(ME),
                    Create(em_ticks),

        
                ),
                Wait(1),
                AnimationGroup(

                    Create(dashed_ME),
                    Create(cm_line2),
                    Create(cm_ticks),                    

                    lag_ratio=0
                )
            ),
            run_time=3
        )

        self.wait()
        label1.z_index = 1

        # Draw triangle NME
        # Final layered construction of triangle NME
        dota_NME = Dot(moving_dot2.get_center(), color=RED, radius=0.2)
        dotb_NME = Dot(moving_dot1.get_center(), color=RED, radius=0.2)
        dotc_NME = Dot(extended_point_E, color=RED, radius=0.2)
        linea_NME = Line(moving_dot2.get_center(), moving_dot1.get_center(), color="#c4c4c4", stroke_width=16)
        lineb_NME = Line(moving_dot1.get_center(), extended_point_E, color="#c4c4c4", stroke_width=16)
        linec_NME = Line(extended_point_E, moving_dot2.get_center(), color="#c4c4c4", stroke_width=16)
        triangle_fill_NME = Polygon(
            moving_dot2.get_center(),
            moving_dot1.get_center(),
            extended_point_E,
            fill_color="#7da895",
            fill_opacity=0,
            stroke_width=0,
            z_index = 0
        )
        # Z-indices for proper layering
        dota_NME.z_index = dotb_NME.z_index = dotc_NME.z_index = 3
        linea_NME.z_index = lineb_NME.z_index = linec_NME.z_index = 2
        label2.z_index = 1
        self.add(triangle_fill_NME)  # Add manually with correct z-index before any animation
        # Fade prior elements to highlight triangle NME
        self.play(
            CE.animate.set_stroke(opacity=0.25),
            ME.animate.set_stroke(opacity=0),
            dashed_ME.animate.set_stroke(opacity=0.25),
            cm_line2.animate.set_stroke(opacity=0.25),
            em_ticks.animate.set_stroke(opacity=0.25),
            cm_ticks.animate.set_stroke(opacity=0.25),
            tick1_C.animate.set_stroke(opacity=0.25),
            tick2_C.animate.set_stroke(opacity=0.25),
            right_angle_C.animate.set_stroke(opacity=0.25),
            point_e.animate.set_fill(RED).set_stroke(RED).set_z_index(2),
            moving_dot1.animate.set_color(RED),
            moving_dot2.animate.set_color(RED),

            Succession(
            Write(dotc_NME),
            Create(linea_NME),
            Create(lineb_NME),
            Create(linec_NME),
            triangle_fill_NME.animate.set_fill(opacity=1)
        ),
        lag_ratio=0.3,
        run_time=3
        )
        self.wait()
        trace_DN.set_stroke(opacity=0)
        DN.set_stroke(opacity=0)
        ME.set_stroke(opacity=0)
        self.remove(dota, dotb)
        moving_dot1.z_index = 999
        moving_dot2.z_index = 999
        self.play(
            linea.animate.set_stroke(opacity=0.1),
            lineb.animate.set_stroke(opacity=0.1),
            linec.animate.set_stroke(opacity=0.1),
            linea_NME.animate.set_stroke(opacity=0.1),
            lineb_NME.animate.set_stroke(opacity=0.1),
            linec_NME.animate.set_stroke(opacity=0.1),
            triangle_fill.animate.set_fill(opacity=0.1),
            triangle_fill_NME.animate.set_fill(opacity=0.1),
            moving_dot1.animate.set_fill(color=RED, opacity=0.1),
            moving_dot2.animate.set_fill(color=RED, opacity=0.1),
            extended_perp_line_C.animate.set_stroke(opacity=0.1),
            tick1.animate.set_stroke(opacity=0),
            tick1_C.animate.set_stroke(opacity=0),
            tick2.animate.set_stroke(opacity=0),
            tick2_C.animate.set_stroke(opacity=0),
            bn_ticks.animate.set_stroke(opacity=0),
            cm_ticks.animate.set_stroke(opacity=0),
            dn_ticks.animate.set_stroke(opacity=0),
            em_ticks.animate.set_stroke(opacity=0),
            cm_line.animate.set_stroke(opacity=0),
            cm_line2.animate.set_stroke(opacity=0/1),
            right_angle.animate.set_stroke(opacity=0.1),
            right_angle_C.animate.set_stroke(opacity=0.1),
            traced_line.animate.set_stroke(opacity=0.1),
            static_lineBN.animate.set_stroke(opacity=0.1),
            label1.animate.set_stroke(opacity=0.1),
            label2.animate.set_stroke(opacity=0.1),
            run_time=1.5
        )
        self.wait(2)
        self.play(
            extended_perp_line.animate.set_stroke(opacity=1),
            extended_perp_line_C.animate.set_stroke(opacity=1)
        )
        self.wait()