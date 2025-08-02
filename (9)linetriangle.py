from manim import *
import numpy as np

class TwoDTriangle(Scene):
    def construct(self):

        v1 = np.array([-3.22, -3, 0])  # A
        v2 = np.array([3.22, -3, 0])   # B
        v3 = np.array([0.0, 2.7, 0])   # C

        line5 = Line(v2 + np.array([-3.25, 0, 0]), v2 + np.array([-4, 0, 0]))
        line6 = Line(v3 + np.array([-2, -3.54037268, 0]), v3 + np.array([-1.5, -2.38975156, 0]))
        moving_dot1 = Dot(color=WHITE, radius=0.2)
        moving_dot2 = Dot(color=WHITE, radius=0.2)
        label1 = Text("M", weight=BOLD).scale(0.7)
        label2 = Text("N", weight=BOLD).scale(0.7)

        label1.add_updater(lambda m: m.next_to(moving_dot1, UR, buff=0.2))
        label2.add_updater(lambda m: m.next_to(moving_dot2, UR, buff=0.2))

        # --- DYNAMIC SEGMENTS AND MINI TRIANGLE ---
        lineMN = Line(moving_dot1.get_center(), moving_dot2.get_center(), color=BLUE, stroke_width=8)
        lineBN  = Line(v2, moving_dot2.get_center(), color=RED,stroke_width=8)
        lineCM = Line(v3, moving_dot1.get_center(), color=ORANGE,stroke_width=8)
        self.attach_line_updater(lineMN, moving_dot1, moving_dot2, is_dot=True)
        self.attach_line_updater(lineBN, v2, moving_dot2, is_dot=False)
        self.attach_line_updater(lineCM, v3, moving_dot1, is_dot=False)
        new_triangle = VGroup()
        self.add(new_triangle)
        new_triangle.set_fill(GREEN)
        moving_dot1.set_fill(opacity=0)
        moving_dot2.set_fill(opacity=0)
        def update_triangle(triangle):
            # Lengths of lines
            triangle.submobjects = []
            lengthlenMN = np.linalg.norm(moving_dot1.get_center() - moving_dot2.get_center())
            lengthlenBN = np.linalg.norm(v2 - moving_dot2.get_center())
            lengthlenMD = np.linalg.norm(v3 - moving_dot1.get_center())

            # Define triangle vertices (2D for simplicity)
            A = np.array([0, 0, 0])  # Fixed at origin
            B = np.array([lengthlenMN, 0, 0])  # Fixed along x-axis
            # Compute position of third vertex using cosine rule
            angle = np.arccos((lengthlenMN**2 + lengthlenMD**2 - lengthlenBN**2) / (2 * lengthlenMN * lengthlenMD))
            C = np.array([lengthlenMD * np.cos(angle), lengthlenMD * np.sin(angle), 0])
            A_Dot = Dot3D(point=A, color=WHITE, radius=0.075, shade_in_3d=True)
            B_Dot = Dot3D(point=B, color=WHITE, radius=0.075, shade_in_3d=True)
            C_Dot = Dot3D(point=C, color=WHITE, radius=0.075, shade_in_3d=True)

            edge1 = Line(A, B, color=BLUE, stroke_width=10)
            edge2 = Line(B, C, color=RED, stroke_width=10)
            edge3 = Line(C, A, color=GREEN, stroke_width=10)
            triangle.add(edge1, edge2, edge3, A_Dot, B_Dot, C_Dot)
            triangle.move_to(ORIGIN)
            # Update triangle vertices
        new_triangle.add_updater(update_triangle)        
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
            