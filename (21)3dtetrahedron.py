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
        def add_right_angle_ticks(vertex, point1, point2, length=0.4, color=YELLOW, stroke_width=5, quadrant=(1, 1)):
            """
            Adds a right-angle marker (L-shape) at a vertex.
            This function creates two lines that form a right angle, similar to
            Manim's `RightAngle` mobject. It is positioned at the `vertex`
            between the lines defined by (`vertex`, `point1`) and (`vertex`, `point2`).
            
            Parameters
            ----------
            vertex : np.ndarray
                The corner point where the right angle is located.
            point1 : np.ndarray
                A point on the first line segment originating from the vertex.
            point2 : np.ndarray
                A point on the second line segment originating from the vertex.
            length : float, optional
                The length of the arms of the right-angle marker, by default 0.4.
            color : ManimColor, optional
                The color of the marker, by default YELLOW.
            stroke_width : int, optional
                The stroke width of the marker lines, by default 5.
            quadrant : tuple[int, int], optional
                A tuple of two values (either 1 or -1) to determine which quadrant
                the angle marker is drawn in. This flips the direction of the arms.
                Defaults to (1, 1).
            Returns
            -------
            VGroup
                A VGroup containing the two lines that form the right-angle marker.
            """
            # Define vectors along the lines from the vertex
            v1 = point1 - vertex
            v2 = point2 - vertex

            # Normalize the vectors and scale them by the desired length
            v1 = v1 / np.linalg.norm(v1) * length
            v2 = v2 / np.linalg.norm(v2) * length
            
            # Adjust vectors based on the quadrant to control marker placement
            v1 = v1 * quadrant[0]
            v2 = v2 * quadrant[1]
            
            # Calculate the points for the L-shaped marker
            p_on_line1 = vertex + v1
            p_on_line2 = vertex + v2
            p_corner = vertex + v1 + v2
            
            # Create the two segments of the L-shape
            tick1 = Line(p_on_line1, p_corner, color=color, stroke_width=stroke_width)
            tick2 = Line(p_on_line2, p_corner, color=color, stroke_width=stroke_width)
            
            return VGroup(tick1, tick2)
        extended_perp_line = Line(B, extended_point, color=YELLOW, stroke_width=9)
        extended_perp_line.set_stroke(opacity=0.25)
        right_angle_ticks = add_right_angle_ticks(foot, A, B, length=0.5, color=YELLOW, stroke_width=5, quadrant=(1, 1))
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
        right_angle_ticks_C = add_right_angle_ticks(foot_C, v1, v3, length=0.5, color=YELLOW, stroke_width=5, quadrant=(1, 1))

        right_angle_C = RightAngle(Line(v1, foot_C), Line(foot_C, v3), length=1, stroke_width=5, quadrant=(1, -1), color=YELLOW)
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
        label_d.move_to([0.1,        -9.66349888,  0.        ])
        label_e.move_to([-7.4404159,   2.85232812,  0.        ])
        self.add(point_e, label_e)
        self.add_fixed_orientation_mobjects(label_e)
        traced_BN = Line(v2, moving_dot2.get_center(), color="#a4d8c2", stroke_width=9)
        traced_BN.set_stroke(opacity=0.25)
        self.add(traced_BN)
        traced_BN.put_start_and_end_on(v2, moving_dot2.get_center())


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
        tick1.set_stroke(opacity=0),
        tick1_C.set_stroke(opacity=0),
        tick2.set_stroke(opacity=0),
        tick2_C.set_stroke(opacity=0),
        bn_ticks.set_stroke(opacity=0),
        cm_ticks.set_stroke(opacity=0),
        dn_ticks.set_stroke(opacity=0),
        em_ticks.set_stroke(opacity=0),
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
    

        label_d2 = Text("D", weight=BOLD).scale(0.49142857)


        extended_perp_line.set_stroke(opacity=0.15)
        point_d2.set_fill(opacity=0.15)
        self.add_fixed_orientation_mobjects(label_d2)

        label_d.set_stroke(opacity=0).set_fill(opacity=0)
        labels[0].move_to([-5.8, -4.4,  0.        ])
        labels[1].move_to([[ 3.55122106, -3.31799997,  0.3        ]])
        labels[2].move_to([0.,         3.11973773, 0.3        ])
        extended_perp_line.set_stroke(opacity=1)
        point_d2.set_fill(opacity=1)
        label_e2 = Text("E", weight=BOLD).scale(0.49142857)
        extended_perp_line_C.set_stroke(opacity=0.15)
        point_e2.set_fill(opacity=0.15).set_stroke(opacity=0.15)
        self.add_fixed_orientation_mobjects(label_e2)


        label_e.set_fill(opacity=0)
        extended_perp_line_C.set_stroke(opacity=1)
        point_e2.set_fill(opacity=1)
        
        # self.add(cegroup2)
        label_d2.move_to([ 1.79008922, -2.85455883,  3.96485901])
        label_e2.move_to([-4.44089210e-16,  1.18431478e-01,  4.26494136e+00])
        # Highlight the 20th point of the blue clone
        # Assume the dot is the second submobject (index 1) in the group
        highlight_dot = Dot3D([ 0.,         -1.00267249,  5.33860308], color="#FFD700", radius=0.2)
        highlight_dot.z_index = 999  # Highest priority

        # Optional: ensure it's in front visually
        self.bring_to_front(highlight_dot)  # Extra layer of safety
        self.add(highlight_dot)
        highlight_dot.set_opacity(1)
        label2.next_to(moving_dot2, UL, buff=0.2)
        self.add(highlight_dot)  # Add first to place it above others
        highlight_label = Text("F", weight=BOLD).scale(0.49142857)
        highlight_label.move_to([-2, -2,  5.35])
        self.add_fixed_orientation_mobjects(highlight_label)
        highlight_label.set_opacity(1)

         # === Animate Connection Between M, N, and F ===
        # Get positions
        moving_dot13D = Dot3D(color=RED, radius=0.2).move_to(line3.get_end())
        moving_dot23D = Dot3D(color=RED, radius=0.2).move_to(line4.get_end())
        self.add(moving_dot13D, moving_dot23D)
        label1.set_fill(opacity=1),
        label2.set_fill(opacity=1),
        moving_dot1.set_fill(opacity=0),
        moving_dot13D.set_fill(opacity=1),
        moving_dot2.set_fill(opacity=0),
        moving_dot23D.set_fill(opacity=1),
        ce_group.set_fill(opacity=0.05).set_stroke(opacity=0.05),
        bd_group.set_fill(opacity=0.05).set_stroke(opacity=0.05),
        point_d2.set_fill(opacity=0.05).set_stroke(opacity=0.05),
        point_e2.set_fill(opacity=0.05).set_stroke(opacity=0.05),
        label_d2.set_fill(opacity=0.05).set_stroke(opacity=0.05),
        label_e2.set_fill(opacity=0.05).set_stroke(opacity=0.05),

        labels[0].move_to([-4.68633652, -3.85979185,  0.])
        M_pos = moving_dot1.get_center()
        N_pos = moving_dot2.get_center()
        F_pos = highlight_dot.get_center()

        # Optional: Triangle fill
        triangle_MNF = Polygon(M_pos, N_pos, F_pos, fill_color=BLUE, fill_opacity=0.4, stroke_width=0)
        triangle_MNF.z_index = 10
        moving_dot13D.z_index = 999
        moving_dot23D.z_index = 999
        # Animate the connections
        trace_FM = Line(F_pos, M_pos, color=ORANGE, stroke_width=10)
        trace_FM.set_stroke(opacity=1.0)
        trace_MN = Line(M_pos, N_pos, color=YELLOW, stroke_width=10)
        self.add(triangle_MNF)
        self.add(trace_MN, trace_FM)
        # CM line
        line_CM = Line(v3, M_pos, color=ORANGE, stroke_width=8)


        self.add(line_CM)
        # BN line
        line_BN = Line(v2, N_pos, color=PURPLE, stroke_width=8)

        # Purple trace from F to N
        trace_FN = Line(F_pos, N_pos, color=PURPLE, stroke_width=10)
        trace_FN.set_stroke(opacity=1.0)

        self.add(line_BN, trace_FN)

        ce_group.set_fill(opacity=0.).set_stroke(opacity=0),
        bd_group.set_fill(opacity=0.).set_stroke(opacity=0),
        point_d2.set_fill(opacity=0.).set_stroke(opacity=0),
        point_e2.set_fill(opacity=0.).set_stroke(opacity=0),
        label_d2.set_fill(opacity=0).set_stroke(opacity=0),
        label_e2.set_fill(opacity=0).set_stroke(opacity=0),

        self.wait()
        self.play(
            line_BN.animate.set_stroke(opacity=0),
            line_CM.animate.set_stroke(opacity=0),
            triangle_MNF.animate.set_fill(opacity=0),
            trace_FM.animate.set_stroke(opacity=0),
            trace_MN.animate.set_stroke(opacity=0),
            trace_FN.animate.set_stroke(opacity=0),
            linea.animate.set_stroke(opacity=0),
            lineb.animate.set_stroke(opacity=0),
            linec.animate.set_stroke(opacity=0),
            linea_NME.animate.set_stroke(opacity=0),
            lineb_NME.animate.set_stroke(opacity=0),
            linec_NME.animate.set_stroke(opacity=0),
            triangle_fill.animate.set_fill(opacity=0),
            triangle_fill_NME.animate.set_fill(opacity=0),
            right_angle.animate.set_stroke(opacity=0),
            right_angle_C.animate.set_stroke(opacity=0),
            traced_line.animate.set_stroke(opacity=0),
            static_lineBN.animate.set_stroke(opacity=0),
            dashed_ME.animate.set_stroke(opacity=0),
            traced_BN.animate.set_stroke(opacity=0),
            moving_dot13D.animate.set_fill(opacity=0),
            moving_dot23D.animate.set_fill(opacity=0),
            label1.animate.set_fill(opacity=0),
            label2.animate.set_fill(opacity=0),
            run_time=1.5
        )
        # === TETRAHEDRON EDGE AND FACE ANIMATION ===

        # Get final point positions
        A_pos = v1
        B_pos = v2
        C_pos = v3
        F_pos = highlight_dot.get_center()  # already positioned earlier

        # Create edges
        edge_AB = Line(A_pos, B_pos, color=BLUE, stroke_width=8)
        edge_AC = Line(A_pos, C_pos, color=BLUE, stroke_width=8)
        edge_BC = Line(B_pos, C_pos, color=BLUE, stroke_width=8)
        edge_AF = Line(A_pos, F_pos, color=BLUE, stroke_width=8)
        edge_BF = Line(B_pos, F_pos, color=BLUE, stroke_width=8)
        edge_CF = Line(C_pos, F_pos, color=BLUE, stroke_width=8)

        # Animate edges one by one
        self.play(Create(edge_AB), run_time=0.3)
        self.play(Create(edge_BC), run_time=0.3)
        self.play(Create(edge_AC), run_time=0.3)
        self.play(Create(edge_AF), run_time=0.3)
        self.play(Create(edge_BF), run_time=0.3)
        self.play(Create(edge_CF), run_time=0.3)

        # Create transparent triangular faces
        face_ABC = Polygon(A_pos, B_pos, C_pos, fill_color=BLUE, fill_opacity=0.15, stroke_width=0)
        face_ABF = Polygon(A_pos, B_pos, F_pos, fill_color=BLUE, fill_opacity=0.25, stroke_width=0)
        face_ACF = Polygon(A_pos, C_pos, F_pos, fill_color=BLUE, fill_opacity=0.25, stroke_width=0)
        face_BCF = Polygon(B_pos, C_pos, F_pos, fill_color=BLUE, fill_opacity=0.25, stroke_width=0)

        # Animate face filling
        self.play(
            FadeIn(face_ABF),
            FadeIn(face_ACF),
            FadeIn(face_BCF),
            run_time=0.5
        )
        self.play(
            FadeOut(face_ABF),
            FadeOut(face_ACF),
            FadeOut(face_BCF),
            FadeOut(edge_AB),
            FadeOut(edge_AF),
            FadeOut(edge_AC),
            FadeOut(edge_BC),
            FadeOut(edge_BF),
            FadeOut(edge_CF),
            FadeOut(moving_dot13D),
            FadeOut(moving_dot23D)
        )
        self.wait()

        # === Animate extension of extended_perp_line (D line - yellow) ===
        midpoint_D = B + perp_vector
        half_line_D = Line(B, B, color=YELLOW, stroke_width=9).set_z_index(999)
        self.play(Create(half_line_D), run_time=0.3)

        # Hide the full version
        extended_perp_line.set_stroke(opacity=0)

        # Animate halfway
        self.play(half_line_D.animate.put_start_and_end_on(B, midpoint_D), run_time=0.5)

        # One tick after halfway
        tick_D1 = Line(foot_midpoint - perp_dir / 2, foot_midpoint + perp_dir / 2, color=WHITE, stroke_width=5).set_stroke(opacity=1).set_z_index(999)
        self.play(Create(tick_D1), run_time=0.3)

        self.wait(0.3)
        half_line_2D = Line(midpoint_D, midpoint_D, color=YELLOW, stroke_width=9).set_z_index(999)
        # Animate full extension
        self.play(half_line_2D.animate.put_start_and_end_on(midpoint_D, extended_point), run_time=0.5)

        # One tick after full
        tick_D2 = Line(tip_midpoint - perp_dir / 2, tip_midpoint + perp_dir / 2, color=WHITE, stroke_width=5).set_stroke(opacity=1).set_z_index(999)
        self.play(
            Create(tick_D2),             
            Create(right_angle_ticks),
            run_time=0.3)
        self.play(
                point_d2.animate.set_fill(opacity=1), 
                label_e.animate.set_fill(opacity=1),

                run_time=0.3)


        self.wait(0.4)

        # === Animate extension of extended_perp_line_C (E line - blue) ===
        midpoint_E = v3 + perp_vector_C
        half_line_E = Line(v3, v3, color=BLUE, stroke_width=9).set_z_index(999)
        half_line_2E = Line(midpoint_E, midpoint_E, color=BLUE, stroke_width=9).set_z_index(999)
        self.play(Create(half_line_E), run_time=0.3)

        # Hide full version
        extended_perp_line_C.set_stroke(opacity=0)

        # Helper: create 2 ticks between p1 and p2
        def create_ticks(p1, p2, color=WHITE, tick_len=0.4, spacing=0.07, stroke_width=5):
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
            return VGroup(tick1.set_z_index(999).set_stroke(opacity=1), tick2.set_z_index(999).set_stroke(opacity=1))
        def create_three_ticks(p1, p2, color=WHITE, tick_len=0.4, spacing=0.15, stroke_width=5):
            direction = p2 - p1
            direction_norm = direction / np.linalg.norm(direction)
            perp = np.array([-direction[1], direction[0], 0])
            perp = perp / np.linalg.norm(perp) * tick_len

            # Center and offsets
            mid = (p1 + p2) / 2
            offset1 = direction_norm * spacing
            offset2 = direction_norm * spacing * 2

            pos1 = mid
            pos2 = mid + offset1
            pos3 = mid - offset1

            tick1 = Line(pos1 - perp / 2, pos1 + perp / 2, color=color, stroke_width=stroke_width)
            tick2 = Line(pos2 - perp / 2, pos2 + perp / 2, color=color, stroke_width=stroke_width)
            tick3 = Line(pos3 - perp / 2, pos3 + perp / 2, color=color, stroke_width=stroke_width)

            return VGroup(tick1.set_z_index(999), tick2.set_z_index(999), tick3.set_z_index(999)).set_stroke(opacity=1)

        # Animate halfway
        self.play(half_line_E.animate.put_start_and_end_on(v3, midpoint_E), run_time=0.5)

        # Two ticks after halfway
        em_half_ticks = create_ticks(v3, midpoint_E)
        self.play(Create(em_half_ticks), run_time=0.3)

        self.wait(0.3)

        # Animate full extension
        self.play(half_line_2E.animate.put_start_and_end_on(midpoint_E, extended_point_E), run_time=0.5)

        # Two ticks after full
        em_full_ticks = create_ticks(midpoint_E, extended_point_E)
        self.play(Create(em_full_ticks), Create(right_angle_ticks_C),run_time=0.3)
        self.play(
            point_e2.animate.set_fill(opacity=1), 
            label_d.animate.set_fill(opacity=1),
            run_time=0.3
            )
        
                # === Animate Line AD ===
        # Midpoints
        mid_AC = (v1 + v3) / 2  # Midpoint of AC
        mid_AB = (v1 + v2) / 2  # Midpoint of AB

        # Dashed halves of AC
        line_AC_1 = DashedLine(v1, mid_AC, color=WHITE, stroke_width=6, dashed_ratio=0.6, dash_length=0.3).set_z_index(999)
        line_AC_2 = DashedLine(mid_AC, v3, color=WHITE, stroke_width=6, dashed_ratio=0.6, dash_length=0.3).set_z_index(999)

        # Dashed halves of AB
        line_AB_1 = DashedLine(v1, mid_AB, color=WHITE, stroke_width=6, dashed_ratio=0.6, dash_length=0.3).set_z_index(999)
        line_AB_2 = DashedLine(mid_AB, v2, color=WHITE, stroke_width=6, dashed_ratio=0.6, dash_length=0.3).set_z_index(999)

        # Animate AC first half, then second

        line_AD = Line(v1, v1, color=GREEN, stroke_width=8).set_z_index(998)
        self.add(line_AD)
        self.play(line_AD.animate.put_start_and_end_on(v1, point_d2.get_center()), run_time=1)
        self.play(Create(line_AC_1), run_time=0.8)
        self.wait()
        # === Animate Line CD ===
        line_CD = Line(v3, v3, color=GREEN, stroke_width=8).set_z_index(998)
        self.add(line_CD)
        self.play(line_CD.animate.put_start_and_end_on(v3, point_d2.get_center()), run_time=1)
        self.play(Create(line_AC_2), run_time=0.8)



        self.wait()
        # === Animate Line BE ===
        line_BE = Line(v2, v2, color=GREEN, stroke_width=8).set_z_index(998)
        self.add(line_BE)
        self.play(line_BE.animate.put_start_and_end_on(v2, point_e2.get_center()), run_time=1)
 
        self.play(Create(line_AB_1), run_time=0.8)
        # === Animate Line AE ===
        line_AE = Line(v1, v1, color=GREEN, stroke_width=8).set_z_index(998)
        self.add(line_AE)
        self.play(line_AE.animate.put_start_and_end_on(v1, point_e2.get_center()), run_time=1)
        # Animate AB first half, then second

        self.play(Create(line_AB_2), run_time=0.8)

        # BC
        ticks_BC = create_three_ticks(v2, v3)

        # AD
        ticks_AD = create_three_ticks(v1, point_d2.get_center())

        # CD – spaced out
        ticks_CD = create_three_ticks(v3, point_d2.get_center(), spacing=0.25)
        ticks_BD = create_three_ticks(v3, point_d2.get_center(), spacing=0.15, tick_len=0.75)
        # AE
        ticks_AE = create_three_ticks(v1, point_e2.get_center())
        # BE – spaced out
        ticks_BE = create_three_ticks(v2, point_e2.get_center(), spacing=0.25)
        ticks_CE = create_three_ticks(v2, point_e2.get_center(), spacing=0.15, tick_len=0.75)
        ticks_BD.set_stroke(opacity=0).set_stroke(opacity=0)
        ticks_CE.set_stroke(opacity=0).set_stroke(opacity=0)

        self.play(
            Create(ticks_BC),
            Create(ticks_AD),
            Create(ticks_CD),
            Create(ticks_AE),
            Create(ticks_BE),
        )
        
        # Get coordinates of E and D
        E = point_e2.get_center()
        D = point_d2.get_center()

        # Triangle AEB
        triangle_AEB = Polygon(v1, E, v2, color=GREEN, fill_opacity=0.3, stroke_opacity=0, z_index=500)
        # Triangle ADC
        triangle_ADC = Polygon(v1, D, v3, color=GREEN, fill_opacity=0.3, stroke_opacity=0, z_index=500)

        # Animate the triangle fills
        self.play(FadeIn(triangle_AEB), FadeIn(triangle_ADC), run_time=1)
        # Step 1: Get all relevant objects
        # Define point F
        F = np.array([0,0,3])

        # Points
        A = v1
        B = v2
        C = v3
        E = point_e2.get_center()
        D = point_d2.get_center()
        AB = v2 - v1  # vector from A to B
        AB_unit = AB / np.linalg.norm(AB)

        AC = v3 - v1  # vector from A to C
        AC_unit = AC / np.linalg.norm(AC)
        def angle_to_rotate_around_axis(point, target, axis, pivot):
            # vectors from pivot
            v1 = point - pivot
            v2 = target - pivot

            # remove component along axis (project onto plane perpendicular to axis)
            v1_proj = v1 - np.dot(v1, axis) * axis
            v2_proj = v2 - np.dot(v2, axis) * axis

            # normalize
            v1_proj /= np.linalg.norm(v1_proj)
            v2_proj /= np.linalg.norm(v2_proj)

            # angle between v1_proj and v2_proj
            angle = np.arccos(np.clip(np.dot(v1_proj, v2_proj), -1, 1))

            # determine rotation direction (sign)
            cross = np.cross(v1_proj, v2_proj)
            sign = np.sign(np.dot(axis, cross))
            return sign * angle

        angle_AEB = angle_to_rotate_around_axis(E, F, AB_unit, v1)
        angle_ADC = angle_to_rotate_around_axis(D, F, AC_unit, v1)

        # Group all AEB components (you used these names in your code)
        group_AEB = VGroup(
            triangle_AEB, line_AE, line_BE,
            ticks_AE, ticks_BE,
            half_line_2E, em_full_ticks, point_e2, ticks_CE
        )

        # Group all ADC components
        group_ADC = VGroup(
            triangle_ADC, line_AD, line_CD,
            ticks_AD, ticks_CD,
            half_line_2D, tick_D2, point_d2, ticks_BD
        )
        label_d.add_updater(lambda mob: mob.next_to(point_e2, DOWN, buff=0.6))
        label_e.add_updater(lambda mob: mob.next_to(point_d2, UL, buff=0.3))
        # Animate the full rotations
        self.play(
            Rotate(group_AEB, angle=angle_AEB+0.427, axis=AB_unit, about_point=v1),
            Rotate(group_ADC, angle=angle_ADC-0.105, axis=AC_unit, about_point=v1),

            run_time=3
        )
        labels[0].z_index = 999
        ticks_BD.set_stroke(opacity=1).set_stroke(opacity=1)
        ticks_CE.set_stroke(opacity=1).set_stroke(opacity=1)
        self.play(
            ticks_AE.animate.set_stroke(opacity=0),
            ticks_AD.animate.set_stroke(opacity=0),
            tick_D1.animate.set_stroke(opacity=0),
            tick_D2.animate.set_stroke(opacity=0),
            em_full_ticks.animate.set_stroke(opacity=0),
            em_half_ticks.animate.set_stroke(opacity=0),            
            Transform(ticks_BE, ticks_CE),
            Transform(ticks_CD, ticks_BD),
            run_time=0.2
        )
        self.wait(1)
        line_AB = Line(v1, v2, color=GREEN, stroke_width=8).set_z_index(998)
        line_AC = Line(v1, v3, color=GREEN, stroke_width=8).set_z_index(998)
        line_BC = Line(v2, v3, color=GREEN, stroke_width=8).set_z_index(998)
        traced_CM.set_stroke(opacity=0)
        self.play(
            FadeOut(label_d, label_e, half_line_2D, half_line_2E, half_line_D, half_line_E, right_angle_ticks, right_angle_ticks_C, line_AB_1, line_AB_2, line_AC_1, line_AC_2),
            FadeIn(moving_dot23D, label2, line_AB, line_AC, line_BC),

            label2.animate.set_fill(opacity=1),

            run_time = 1
        )
        self.move_camera(phi=66 * DEGREES, theta=22.5* DEGREES, gamma = -62.5* DEGREES, frame_center=([0.0, -1.07566812, 1.33465077]), run_time=1)
        self.play(
            highlight_label.animate.move_to([-2.35, -2.35,  5.35]),
            labels[0].animate.move_to([-4.8633652, -4.45979185,  0.]),
            triangle.animate.set_opacity(0.3),
            run_time=0.5
        )
        self.wait()
    
         # Dynamic lines MB and MF
        line_nb = always_redraw(lambda: Line(moving_dot23D.get_center(), v2, stroke_width = 8, color=BLUE))
        line_nf = always_redraw(lambda: Line(moving_dot23D.get_center(), highlight_dot.get_center(), stroke_width = 8, color=BLUE))
        # Dynamic label following M
        label2.add_updater(lambda mob: mob.next_to(moving_dot23D, UL, buff=0.2))


        # Add elements after defining with updaters
        self.play(
            Create(line_nb),
            Create(line_nf)
        )

        # Animate the dot along AC (t from 0 to 1)
        alpha = 0.65  # Choose any value between 0 and 1
        target_point = A + (C - A) * alpha
        self.bring_to_front(moving_dot23D)
        moving_dot23D.z_index = 999
        self.play(moving_dot23D.animate.move_to(target_point), run_time=2, rate_func=linear)
        self.wait()
        target_point4 = A + (B - A) * 0.55

        moving_dot13D.move_to(target_point4)
        self.play(
            FadeOut(line_nb,line_nf, moving_dot23D, label2)
        )
        self.move_camera(phi=76.5 * DEGREES, theta=22.5* DEGREES, gamma = 58.5* DEGREES, frame_center=([0.0, -1.07566812, 1.33465077]), run_time=1)
    
         # Dynamic lines MB and MF
        line_mc = always_redraw(lambda: Line(moving_dot13D.get_center(), v3, stroke_width = 8, color=BLUE))
        line_mf = always_redraw(lambda: Line(moving_dot13D.get_center(), highlight_dot.get_center(), stroke_width = 8, color=BLUE))

        # Dynamic label following M
        label1.add_updater(lambda mob: mob.next_to(moving_dot13D, UR, buff=0.75))


        # Add elements after defining with updaters
        self.play(
            labels[0].animate.move_to([-6.5, -3.25,  0]),
            highlight_label.animate.move_to([-6.9, -3,  5.1]),
            label1.animate.set_opacity(1).set_fill(opacity=1),
            Create(line_mc),
            Create(line_mf)
        )
        # Animate the dot along AC (t from 0 to 1)
        alpha = 0.05  # Choose any value between 0 and 1
        target_point2 = A + (B - A) * alpha
        target_point3 = A + (B - A) * 0.55

        self.bring_to_front(moving_dot13D)
        moving_dot13D.z_index = 999
        self.play(moving_dot13D.animate.move_to(target_point2), run_time=1.25, rate_func=linear)
        self.play(moving_dot13D.animate.move_to(target_point3), run_time=1.25, rate_func=linear)

        self.wait()