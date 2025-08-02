from manim import *
import numpy as np

class ThreeDTriangle(ThreeDScene):
    def construct(self):
        # Match 2D scene camera position
        # Triangle vertices
        v1 = np.array([-3.22, -3, 0])
        v2 = np.array([3.22, -3, 0])
        v3 = np.array([0.0, 2.7, 0])

        triangle = Polygon(v1, v2, v3, color=GREEN, fill_opacity=1, stroke_width=3)

        label_positions = [v1, v2, v3]
        label_texts = ["A", "B", "C"]
        labels = VGroup()
        for i, pos in enumerate(label_positions):
            direction = pos / np.linalg.norm(pos) if np.linalg.norm(pos) != 0 else UP
            label = Text(label_texts[i], weight=BOLD).scale(0.49142857)
            label.next_to(pos, direction, buff=0.3)
            labels.add(label)

        line1 = Line3D(v1 + np.array([0.6, 0, 0]), v2 + np.array([-4, 0, 0]))
        line2 = Line3D(v1 + np.array([0.45, 0.796583853, 0]), v3 + np.array([-1, -1.77018634, 0]))
        line3 = Line(v2 + np.array([-4, 0, 0]), v2 + np.array([-2, 0, 0]))
        line4 = Line(v3 + np.array([-1, -1.77018634, 0]), v3 + np.array([-2.7, -4.77950313, 0]))

        moving_dot1 = Dot(color=RED, radius=0.2).move_to(line3.get_end())
        moving_dot2 = Dot(color=RED, radius=0.2).move_to(line4.get_end())

        label1 = Text("M", weight=BOLD).scale(0.49142857)
        label2 = Text("N", weight=BOLD).scale(0.49142857)
        label2.next_to(moving_dot2, DR, buff=0.2)
        label1.next_to(moving_dot1, DR, buff=0.2)
        label2.z_index = 999
        label1.z_index = 999
        moving_dot1.z_index = 999
        moving_dot2.z_index = 999
        self.add(triangle, moving_dot1, moving_dot2)
        self.add_fixed_orientation_mobjects(*labels)

        static_lineBN = DashedLine(v2, moving_dot2.get_center(), color=YELLOW, stroke_width=8, dashed_ratio=0.6, dash_length=0.35)
        self.add(static_lineBN)
        static_lineBN.set_stroke(opacity=0.25)

        A, B, C = v1, v2, v3
        AC = C - A
        AB = B - A
        projection_length = np.dot(AB, AC) / np.dot(AC, AC)
        foot = A + projection_length * AC
        perp_vector = foot - B
        extended_point = B + 2 * perp_vector

        extended_perp_line = Line(B, extended_point, color=YELLOW, stroke_width=9)
        extended_perp_line.set_stroke(opacity=0.25)
        right_angle = RightAngle(Line(A, foot), Line(foot, B), length=0.4, stroke_width=5, quadrant=(-1, 1), color=YELLOW)
        right_angle.set_stroke(opacity=0.25)
        self.add(extended_perp_line, right_angle)

        foot_midpoint = (B + foot) / 2
        tip_midpoint = (foot + extended_point) / 2
        perp_dir = np.array([-(foot - B)[1], (foot - B)[0], 0])
        perp_dir = perp_dir / np.linalg.norm(perp_dir) * 0.5
        tick1 = Line(foot_midpoint - perp_dir / 2, foot_midpoint + perp_dir / 2, color=WHITE, stroke_width=5)
        tick2 = Line(tip_midpoint - perp_dir / 2, tip_midpoint + perp_dir / 2, color=WHITE, stroke_width=5)
        tick1.set_stroke(opacity=0.25)
        tick2.set_stroke(opacity=0.25)
        self.add(tick1,tick2)

        def create_ticks(p1, p2, color=WHITE, tick_len=0.4, spacing=0.07, stroke_width = 5):
            direction = p2 - p1
            direction_norm = direction / np.linalg.norm(direction)
            perp = np.array([-direction[1], direction[0], 0])
            perp = perp / np.linalg.norm(perp) * tick_len
            mid = (p1 + p2) / 2
            offset = direction_norm * spacing
            pos1 = mid + offset
            pos2 = mid - offset
            tick1 = Line(pos1 - perp / 2, pos1 + perp / 2, color=color, stroke_width=stroke_width)
            tick2 = Line(pos2 - perp / 2, pos2 + perp / 2, color=color, stroke_width=stroke_width)
            return VGroup(tick1, tick2)
        def create_ticks_3d(start, end, tick_len=0.2, spacing=0.07):
            # Direction of the segment
            direction = normalize(end - start)
            midpoint = (start + end) / 2

            # A vector perpendicular to the direction
            if not np.allclose(direction, [0, 0, 1]):
                perp = normalize(np.cross(direction, [0, 0, 1]))
            else:
                perp = normalize(np.cross(direction, [0, 1, 0]))

            ticks = VGroup()

            if spacing == 0:
                for scale in [-1, 1]:
                    tick = Line3D(midpoint + perp * tick_len / 2 * scale,
                                midpoint - perp * tick_len / 2 * scale,
                                color=WHITE, stroke_width=6)
                    ticks.add(tick)
            else:
                for offset in [-spacing, spacing]:
                    point = midpoint + offset * direction
                    for scale in [-1, 1]:
                        tick = Line3D(point + perp * tick_len / 2 * scale,
                                    point - perp * tick_len / 2 * scale,
                                    color=WHITE, stroke_width=6)
                        ticks.add(tick)

            return ticks

        bn_ticks = create_ticks(v2, moving_dot2.get_center())
        dn_ticks = create_ticks(extended_point, moving_dot2.get_center())
        bn_ticks.z_index = 999
        dn_ticks.z_index = 999
        bn_ticks.set_stroke(opacity=0.25)
        dn_ticks.set_stroke(opacity=0.25)
        
        self.add(bn_ticks, dn_ticks)

        point_d = Dot(extended_point, color=RED, radius=0.2)
        point_d.z_index = 999
        label_d = Text("D", weight=BOLD).next_to(extended_point, DOWN, buff=0.3000001).scale(0.49142857)
        self.add(point_d)
        self.add_fixed_orientation_mobjects(label_d)
        AB = v2 - v1
        AC = v3 - v1
        projection_length_C = np.dot(AC, AB) / np.dot(AB, AB)
        foot_C = v1 + projection_length_C * AB
        perp_vector_C = foot_C - v3
        extended_point_E = v3 + 2 * perp_vector_C

        extended_perp_line_C = Line(v3, extended_point_E, color=YELLOW, stroke_width=9)
        right_angle_C = RightAngle(Line(v1, foot_C), Line(foot_C, v3), length=0.4, stroke_width=5, quadrant=(1, -1), color=YELLOW)
        right_angle_C.set_stroke(opacity=0.25)
        self.add(extended_perp_line_C, right_angle_C)

        foot_midpoint_C = (v3 + foot_C) / 2
        tip_midpoint_C = (foot_C + extended_point_E) / 2
        perp_dir_C = np.array([-(foot_C - v3)[1], (foot_C - v3)[0], 0])
        perp_dir_C = perp_dir_C / np.linalg.norm(perp_dir_C) * 0.5
        tick1_C = Line(foot_midpoint_C - perp_dir_C / 2, foot_midpoint_C + perp_dir_C / 2, color=WHITE, stroke_width=5)
        tick2_C = Line(tip_midpoint_C - perp_dir_C / 2, tip_midpoint_C + perp_dir_C / 2, color=WHITE, stroke_width=5)
        tick1_C.set_stroke(opacity=0.25)
        tick2_C.set_stroke(opacity=0.25)
        self.add(tick1_C, tick2_C)

        cm_ticks = create_ticks(v3, moving_dot1.get_center())
        em_ticks = create_ticks(extended_point_E, moving_dot1.get_center())
        cm_ticks.set_stroke(opacity=0.25)
        em_ticks.set_stroke(opacity=0.25)
        
        self.add(cm_ticks, em_ticks)

        point_e = Dot(extended_point_E, color=RED, radius=0.2)
        point_e.z_index = 999
        label_e = Text("E", weight=BOLD).next_to(extended_point_E, DOWN, buff=0.28).scale(0.49142857)
        self.add(point_e, label_e)
        self.add_fixed_orientation_mobjects(label_e)
        traced_BN = Line(v2, moving_dot2.get_center(), color="#a4d8c2", stroke_width=9)
        traced_DN = Line(extended_point, moving_dot2.get_center(), color="#a4d8c2", stroke_width=9)
        traced_BN.set_stroke(opacity=0.25)
        traced_DN.set_stroke(opacity=0)
        self.add(traced_BN, traced_DN)
        traced_BN.put_start_and_end_on(v2, moving_dot2.get_center())
        traced_DN.put_start_and_end_on(extended_point, moving_dot2.get_center())


        traced_CM = Line(v3, moving_dot1.get_center(), color=PURPLE, stroke_width=9)
        traced_CM.set_stroke(opacity=0.1)
        dashed_ME = DashedLine(moving_dot1.get_center(), foot_C, color=YELLOW, stroke_width=10, dashed_ratio=0.6, dash_length=0.2)
        dashed_ME.set_stroke(opacity=0.25)
        CE = Line(v3, extended_point_E, color=YELLOW, stroke_width=9)
        ME = Line(extended_point_E, moving_dot1.get_center(), color="#8377D1", stroke_width=15)
        ME.set_stroke(opacity =0.25)
        self.add(CE, ME, dashed_ME, traced_CM)
        triangle_fill = Polygon(
            moving_dot1.get_center(),
            moving_dot2.get_center(),
            extended_point,
            fill_color="#A4DBC3",
            fill_opacity=0.9,
            stroke_width=0
        )
        triangle_fill.z_index = 995
        linea = Line(moving_dot1.get_center(), moving_dot2.get_center(), color=WHITE, fill_opacity=0.9, stroke_width=9)
        lineb = Line(moving_dot2.get_center(), extended_point, color=WHITE, fill_opacity=0.9, stroke_width=9)
        linec = Line(extended_point, moving_dot1.get_center(), color=WHITE, fill_opacity=0.9, stroke_width=9)
        linea.z_index = 996
        lineb.z_index = 996
        linec.z_index = 996
        self.add(triangle_fill, linea, lineb, linec)        
        linea_NME = Line(moving_dot2.get_center(), moving_dot1.get_center(), color="#c4c4c4", stroke_width=9)
        lineb_NME = Line(moving_dot1.get_center(), extended_point_E, color="#c4c4c4", stroke_width=9)
        triangle_fill_NME = Polygon(
            moving_dot2.get_center(),
            moving_dot1.get_center(),
            extended_point_E,
            fill_color="#7da895",
            fill_opacity=1,
            stroke_width=0,
            z_index = 0
        )
        triangle_fill_NME.z_index = 0
        linec_NME = Line(extended_point_E, moving_dot2.get_center(), color="#c4c4c4", stroke_width=9)
        traced_line = Line(
            start=moving_dot2.get_center(),
            end=moving_dot2.get_center(),  # Start as a point
            color=BLUE,
            stroke_width=15
        )
        linea_NME.z_index = 998
        lineb_NME.z_index = 998
        linec_NME.z_index = 998
        self.add(linea_NME, lineb_NME, triangle_fill_NME, linec_NME )
        self.add_fixed_orientation_mobjects(label1, label2)
        ME.set_stroke(opacity=0)
        linea.set_stroke(opacity=0.1)
        lineb.set_stroke(opacity=0.1)
        linec.set_stroke(opacity=0.1)
        linea_NME.set_stroke(opacity=0.1)
        lineb_NME.set_stroke(opacity=0.1)
        linec_NME.set_stroke(opacity=0.1)
        triangle_fill.set_fill(opacity=0.1)
        triangle_fill_NME.set_fill(opacity=0.1)
        moving_dot1.set_fill(color=RED, opacity=0.1)
        moving_dot2.set_fill(color=RED, opacity=0.1)
        extended_perp_line_C.set_stroke(opacity=0.1)
        tick1.set_stroke(opacity=0.1)
        tick1_C.set_stroke(opacity=0.1)
        tick2.set_stroke(opacity=0.1)
        tick2_C.set_stroke(opacity=0.1)
        bn_ticks.set_stroke(opacity=0.1)
        cm_ticks.set_stroke(opacity=0.1)
        dn_ticks.set_stroke(opacity=0.1)
        em_ticks.set_stroke(opacity=0.1)
        traced_CM.set_stroke(opacity=0.1)
        right_angle.set_stroke(opacity=0.1)
        right_angle_C.set_stroke(opacity=0.1)
        traced_line.set_stroke(opacity=0.1)
        static_lineBN.set_stroke(opacity=0.1)
        extended_perp_line.set_stroke(opacity=1)
        extended_perp_line_C.set_stroke(opacity=1)
        label1.set_fill(opacity=0.1)
        label2.set_fill(opacity=0.1)
        self.add(traced_line)
        extended_perp_line.z_index = 999
        point_d2 = Dot3D(extended_point, color=RED, radius=0.2)
        point_d2.set_stroke(opacity=0)
        point_e2 = Dot3D(extended_point_E, color=RED, radius=0.2)
        point_e2.set_stroke(opacity=0)
        point_d2.z_index=999
        point_e2.z_index=999
        extended_perp_line.z_index = 998
        extended_perp_line.z_index = 999
        extended_perp_line_C.set_color(BLUE)
        point_d.set_stroke(opacity=0)
        point_d2.set_stroke(opacity=1)
        point_e2.set_stroke(opacity=1)
        point_e.set_stroke(opacity=0)
        self.remove(point_d,point_e, CE)        
        dummy_mobject = Dot3D().set_opacity(0)  # invisible
        self.add(dummy_mobject)
        self.play(dummy_mobject.animate.shift(5 * OUT), run_time=0.0001)

        self.set_camera_orientation(phi=60 * DEGREES, theta=29 * DEGREES, frame_center=[-2.25, -3, 0], zoom=0.5)
        label_d.move_to([-6.54404159,  1.85232812,  0.        ])
        label_e.move_to([ 0.0,         -9.36349888,  0.0        ])
                # === ROTATION SETUP ===
        # Define rotation axis (AC)
        axis_ac = v3 - v1  # vector from A to C
        axis_ac = axis_ac / np.linalg.norm(axis_ac)*3/4  # normalize
        axis_ab = v2 - v1  # vector from A to B
        axis_ab = axis_ab / np.linalg.norm(axis_ab)*3/4  # normalize
        # Group D and BD
        bd_group = VGroup(extended_perp_line, point_d2)
        ce_group = VGroup(extended_perp_line_C, point_e2)
        bd_group2 = VGroup(extended_perp_line, point_d2)
        ce_group2 = VGroup(extended_perp_line_C, point_e2)
        # Add to scene before rotating
        self.add((bd_group-label_d), (ce_group-label_e))
        self.add_fixed_orientation_mobjects(bd_group-extended_perp_line-point_d2, (ce_group-extended_perp_line_C-point_e2))
        def get_rotated_clones(group, axis, about_point, steps, total_angle):
            clones = []
            for i in range(1, steps + 1):
                step_angle = (i / steps) * total_angle
                copy = VGroup()

                for mob in group:
                    if isinstance(mob, Line):
                        # Top half of the line: from midpoint to end
                        mid = (mob.get_start() + mob.get_end()) / 2
                        top_half = Line(mid, mob.get_end(), color=mob.color, stroke_width=mob.stroke_width)
                        top_half.z_index = 20
                        top_half.rotate(angle=step_angle, axis=axis, about_point=about_point)
                        top_half.set_opacity(0.15)
                        copy.add(top_half)
                    else:
                        # Assume it's a dot
                        mob_copy = mob.copy()
                        mob_copy.rotate(angle=step_angle, axis=axis, about_point=about_point)
                        mob_copy.set_opacity(0.15)
                        copy.add(mob_copy)

                clones.append(copy)
            return clones

        num_steps = 25
        rotation_fraction = 0.75
        angle_bd = rotation_fraction * PI
        angle_ce = -rotation_fraction * PI+0.06

        label_d2 = Text("D", weight=BOLD).scale(0.49142857)


        # ========== BD ROTATION ==========
        bd_tracker = ValueTracker(0)
 

        bd_outlines = get_rotated_clones(bd_group2, axis_ac, v1, num_steps, angle_bd)
        self.add(*bd_outlines)

        temp_bd_group = bd_group2.copy()
        self.add(temp_bd_group)
        extended_perp_line.set_stroke(opacity=0.15)
        point_d2.set_fill(opacity=0.15)
        self.add_fixed_orientation_mobjects(label_d2)

        label_d.set_stroke(opacity=0).set_fill(opacity=0)
        bd_tracker.set_value(1),
        labels[0].move_to([-5.8, -4.4,  0.        ])
        labels[1].move_to([[ 3.55122106, -3.31799997,  0.3        ]])
        labels[2].move_to([0.,         3.11973773, 0.3        ])
        extended_perp_line.set_stroke(opacity=1)
        point_d2.set_fill(opacity=1)

        self.remove(temp_bd_group)
        bdgroup2 = bd_group.copy()
        (bdgroup2-point_d2-label_d).set_stroke(opacity=0.15).set_fill(opacity=0.15)
        self.add(bdgroup2)
        bd_group.rotate(angle_bd, axis=axis_ac, about_point=v1)
        self.add(bd_group)
        label_e2 = Text("E", weight=BOLD).scale(0.49142857)
        # ========== CE ROTATION ==========
        ce_tracker = ValueTracker(0)
        ce_outlines = get_rotated_clones(ce_group2, axis_ab, v1, num_steps, angle_ce)
        self.add(*ce_outlines)

        temp_ce_group = ce_group2.copy()
        self.add(temp_ce_group)

        # Set the original lines to semi-transparent before animation starts
        extended_perp_line_C.set_stroke(opacity=0.15)
        point_e2.set_fill(opacity=0.15).set_stroke(opacity=0.15)
        self.add_fixed_orientation_mobjects(label_e2)


        label_e.set_fill(opacity=0)

        ce_tracker.set_value(1)
        extended_perp_line_C.set_stroke(opacity=1)
        point_e2.set_fill(opacity=1)
        self.remove(temp_ce_group)
        
        cegroup2 = ce_group.copy()
        # self.add(cegroup2)
        ce_group.rotate(angle_ce, axis=axis_ab, about_point=v1)
        label_d2.move_to([ 1.79008922, -2.85455883,  3.96485901])
        label_e2.move_to([-4.44089210e-16,  1.18431478e-01,  4.26494136e+00])
        # Highlight the 20th point of the blue clone
        highlight_index = 20  # 20th clone (0-indexed)
        target_clone = ce_outlines[highlight_index]

        # Assume the dot is the second submobject (index 1) in the group
        highlight_dot = target_clone[1].copy().set_opacity(1)
        highlight_dot.set_color("#FFD700")
        highlight_dot.z_index = 999  # Highest priority

        # Optional: ensure it's in front visually
        self.bring_to_front(highlight_dot)  # Extra layer of safety
        self.play(
            FadeIn(highlight_dot),
            highlight_dot.animate.set_opacity(1),
            label2.animate.next_to(moving_dot2, UL, buff=0.2),
            run_time=2
        )
        self.add(highlight_dot)  # Add first to place it above others
        highlight_label = Text("F", weight=BOLD).scale(0.49142857)
        highlight_label.move_to([-2, -2,  5.35])
        self.add_fixed_orientation_mobjects(highlight_label)
        self.wait()
        self.play(
            highlight_label.animate.set_opacity(1),
            run_time=2
        )
         # === Animate Connection Between M, N, and F ===
        # Get positions
        fade_anims = []
        moving_dot13D = Dot3D(color=RED, radius=0.2).move_to(line3.get_end())
        moving_dot23D = Dot3D(color=RED, radius=0.2).move_to(line4.get_end())

        for group in bd_outlines + ce_outlines:
            for mob in group:
                fade_anims.append(mob.animate.set_opacity(0.05))
        self.play(
            label1.animate.set_fill(opacity=1),
            label2.animate.set_fill(opacity=1),
            moving_dot1.animate.set_fill(opacity=0),
            moving_dot13D.animate.set_fill(opacity=1),
            moving_dot2.animate.set_fill(opacity=0),
            moving_dot23D.animate.set_fill(opacity=1),
            ce_group.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            bd_group.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            bdgroup2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            point_d2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            point_e2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            label_d2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            label_e2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.05),
            *fade_anims,
        )
        M_pos = moving_dot1.get_center()
        N_pos = moving_dot2.get_center()
        F_pos = highlight_dot.get_center()

        # Create lines connecting M, N, and F
        line_MN = Line(M_pos, N_pos, color=WHITE, stroke_width=10)
        line_NF = Line(N_pos, F_pos, color=WHITE, stroke_width=10)
        line_FM = Line(F_pos, M_pos, color=WHITE, stroke_width=10)

        # Optional: Triangle fill
        triangle_MNF = Polygon(M_pos, N_pos, F_pos, fill_color=BLUE, fill_opacity=0.4, stroke_width=0)
        triangle_MNF.z_index = 10
        moving_dot13D.z_index = 999
        moving_dot23D.z_index = 999
        # Animate the connections
        self.play(
            FadeIn(triangle_MNF),
            Create(line_MN),
            Create(line_NF),
            Create(line_FM),
            run_time=2
        )
        # CM line
        line_CM = Line(v3, M_pos, color=ORANGE, stroke_width=8)

        # Orange trace from F to M
        trace_FM = Line(F_pos, M_pos, color=ORANGE, stroke_width=11)
        trace_FM.set_stroke(opacity=1.0)

        self.add(line_CM)

        self.play(
            Create(line_CM),
            Create(trace_FM),  # Or ShowPassingFlash(trace_FM.copy())
            run_time=1.5
        )
        # BN line
        line_BN = Line(v2, N_pos, color=PURPLE, stroke_width=8)

        # Purple trace from F to N
        trace_FN = Line(F_pos, N_pos, color=PURPLE, stroke_width=10)
        trace_FN.set_stroke(opacity=1.0)

        self.add(line_BN)

        self.play(
            Create(line_BN),
            Create(trace_FN),
            run_time=1.5
        )

