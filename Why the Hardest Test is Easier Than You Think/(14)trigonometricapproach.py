from manim import *
import numpy as np

class TwoDTriangle(Scene):
    def construct(self):
        # Coordinate plane


        # Triangle vertices
        v1 = np.array([-3.22, -3, 0])  # A
        v2 = np.array([3.22, -3, 0])   # B
        v3 = np.array([0.0, 2.7, 0])   # C

        triangle = Polygon(v1, v2, v3, color="#a4d8c2", fill_opacity=1, stroke_width=3)
        triangle.z_index =-1
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
        line1 = Line(v1+ np.array([2.4, 0, 0]), v2 + np.array([-3.2, 0, 0]))
        line2 = Line(v1+np.array([0.36, 0.637267082, 0]), v3 + np.array([-1.2, -2.12422361, 0]))
        line3 = Line(v2 + np.array([-3.2, 0, 0]), v1+ np.array([2.4, 0, 0]))
        line4 = Line(v3 + np.array([-1.2, -2.12422361, 0]), v3 + np.array([-2, -3.54037268, 0]))
        
        # Moving dots
        moving_dot1 = Dot(color=WHITE, radius=0.2)
        moving_dot2 = Dot(color=WHITE, radius=0.2)
        moving_dot1.move_to(v2 + np.array([-3.2, 0, 0]))
        moving_dot2.move_to(v1+np.array([0.36, 0.637267082, 0]))
        lineMN = Line(moving_dot1.get_center(), moving_dot2.get_center(), color=BLUE, stroke_width=8)
        lineBN  = Line(v2, moving_dot2.get_center(), color=RED,stroke_width=8)
        lineCM = Line(v3, moving_dot1.get_center(), color=YELLOW,stroke_width=8)
        self.attach_line_updater(lineMN, moving_dot1, moving_dot2, is_dot=True)
        self.attach_line_updater(lineBN, v2, moving_dot2, is_dot=False)
        self.attach_line_updater(lineCM, v3, moving_dot1, is_dot=False)
        lineMN.z_index = 0
        lineBN.z_index = 0
        lineCM.z_index = 0
        self.add(lineMN, lineBN, lineCM)
        def line_intersection(p1, p2, p3, p4):
            """Finds the intersection point of lines (p1-p2) and (p3-p4) in 2D."""
            A1, B1 = p1[:2], p2[:2]
            A2, B2 = p3[:2], p4[:2]

            def perp(a):
                return np.array([-a[1], a[0]])

            da = B1 - A1
            db = B2 - A2
            dp = A1 - A2
            dap = perp(da)
            denom = np.dot(dap, db)
            if denom == 0:
                return None  # Parallel lines
            num = np.dot(dap, dp)
            intersection = (num / denom)*db + A2
            return np.array([*intersection, 0])
        intersection_point = always_redraw(lambda: Dot(
            line_intersection(v3, moving_dot1.get_center(), v2, moving_dot2.get_center()),
            radius=0.08,
            color=WHITE
        ))
        self.add(intersection_point)
        def create_angle_with_label(p1, vertex, p2, radius=0.4, color=BLUE, label_offset=0.4):
            """
            Returns a VGroup of an Angle mobject and a label showing angle value in degrees.
            The label is placed at the arc's midpoint position.
            """
            def get_angle():
                return Angle(
                    Line(vertex(), p1()),
                    Line(vertex(), p2()),
                    radius=radius,
                    color=color,
                    other_angle=False,
                    stroke_width=10  # Increase this value for thicker arcs
                )

            angle = always_redraw(get_angle)

            def get_label():
                # Compute vectors from vertex to points
                vec1 = normalize(p1() - vertex())
                vec2 = normalize(p2() - vertex())

                # Compute the angle between the vectors in radians
                dot = np.clip(np.dot(vec1, vec2), -1.0, 1.0)
                angle_rad = np.arccos(dot)

                # Compute the bisector direction
                bisector = normalize(vec1 + vec2)
                label_position = vertex() + bisector * (radius + label_offset)

                angle_deg = np.degrees(angle_rad)
                return Tex(r"\textbf{" + f"{angle_deg:.0f}" + r"}$^\circ$", color=BLACK).scale(0.5).move_to(label_position)

            # Always redraw the intersection point
            label = always_redraw(get_label)
            label.z_index = 2
            angle.z_index = 2
            return VGroup(angle, label)

        # ∠CMN at M
        angle_M = create_angle_with_label(
            lambda: v3,
            lambda: moving_dot1.get_center(),
            lambda: moving_dot2.get_center(),
            color=BLUE
        )

        # ∠BNM at N
        angle_N = create_angle_with_label(
            lambda: moving_dot1.get_center(),
            lambda: moving_dot2.get_center(),
            lambda: v2,
            color=RED
        )

        # ∠CBN at B
        angle_CBN = create_angle_with_label(
            lambda: v3,
            lambda: v2,
            lambda: moving_dot2.get_center(),
            radius=0.3,
            color=ORANGE
        )

        # ∠ACM at C
        angle_CXN = create_angle_with_label(
            lambda: v3,                                   # Point C
            lambda: intersection_point.get_center(),      # Intersection point (vertex)
            lambda: moving_dot2.get_center(),             # Point N
            color=GREEN,
        )
        self.add(angle_M, angle_N, angle_CBN, angle_CXN)
        # Coordinate labels
        self.add(triangle, labels)
        self.add(moving_dot1, moving_dot2)
        self.add(line1, line2, line3, line4)
        for line in [line1, line2, line3, line4]:
            line.set_opacity(0)
        self.add(line1, line2, line3, line4)
        def project_point_onto_line(P, A, B):
            AP = P - A
            AB = B - A
            t = np.dot(AP, AB) / np.dot(AB, AB)
            projection = A + t * AB
            return projection

            # Always redraw the dashed perpendicular from intersection to blue line (MN)
        perpendicular_line = always_redraw(lambda: DashedLine(
            start=intersection_point.get_center(),
            end=project_point_onto_line(
                intersection_point.get_center(),
                moving_dot1.get_center(),
                moving_dot2.get_center()
            ),
            color=GRAY,
            dash_length=0.1,
            stroke_width=8
        ))
        right_angle = always_redraw(lambda: RightAngle(
            Line(intersection_point.get_center(), projected_point := project_point_onto_line(
                intersection_point.get_center(),
                moving_dot1.get_center(),
                moving_dot2.get_center()
            )),
            Line(projected_point, moving_dot1.get_center()),
            length=0.2,
            quadrant=(-1, -1),
            stroke_width=4,
            color=GRAY
        ))
        self.add(perpendicular_line, right_angle)
        self.play(MoveAlongPath(moving_dot1, line3),
                MoveAlongPath(moving_dot2, line2), run_time=2, rate_func=linear
        )
        self.wait(0.1)
        self.play(MoveAlongPath(moving_dot1, line1),
                  MoveAlongPath(moving_dot2, line4, rate_func=linear), run_time=1.5, rate_func=linear
                  )
    
        self.wait()
    
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
