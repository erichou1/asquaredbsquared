from manim import *
from typing import TYPE_CHECKING, Callable, Iterable, Sequence
import math
class Triangle(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        
        vertex_coords = [
                    [1, -1/math.sqrt(3), 0], #A
                    [0, 2/math.sqrt(3), 0], ###B
                    [0, 0, 4/math.sqrt(6)], #C
                    [-1, -1/math.sqrt(3), 0] #D
                ]
        faces_list = [
            [0, 1, 3],
            [1, 2, 3],
            [3, 0, 2],
            [0, 1, 2]
        ]

        labels = "ABCD"
        tex_labels = []
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        tetra = Polyhedron(vertex_coords, faces_list)
        for i, vertex in enumerate(vertex_coords):
            # Position the labels outside the tetrahedron
            direction = np.array(vertex)  # Direction is just the vertex position
            label_position = direction / np.linalg.norm(direction) * 1.65  # Move outward by a factor of 1.5
            label = Text(labels[i], weight=BOLD, slant=ITALIC).scale(0.5).move_to(label_position + np.array([0, 0, 0.2]))  # Slight offset in Z direction
            tex_labels.append(label)
        self.add_fixed_orientation_mobjects(*tex_labels)
        self.add(axes)
        self.wait()
        polyhedra = Polyhedron(vertex_coords, faces_list)
        self.add(polyhedra)

    
        self.add(*tex_labels)

        # self.move_camera(theta=270 *DEGREES, run_time=0.1)
        self.move_camera(zoom = 1.5, run_time=0.1)
        
        yellow_face_vertices = [vertex_coords[i] for i in faces_list[1]]
        polyhedra.faces[1].set_color(YELLOW)
        polyhedra.faces[0].set_fill(opacity=0)
        polyhedra.faces[2].set_fill(opacity=0)
        polyhedra.faces[3].set_fill(opacity=0)
        # A, B, C = [np.array(v) for v in face_vertices]
        #Define a white  dot

        movingdot1 = Dot3D(color=WHITE, radius=0.1, shade_in_3d=True)
        movingdot2 = Dot3D(color=WHITE, radius=0.1, shade_in_3d=True)
        movingdot1.z_index = 10
        movingdot2.z_index = 10
        movingdot1.set_opacity(1)
        movingdot2.set_opacity(1)
        label1 = Text("M", weight=BOLD, slant=ITALIC).scale(0.375)
        label2 = Text("N", weight=BOLD, slant=ITALIC).scale(0.375)
        
        self.add_fixed_orientation_mobjects(label1, label2, movingdot1, movingdot2)
        self.remove(label1, label2, movingdot1, movingdot2)

        # Update function to ensure the label stays 10 units to the left of the dot
        def update_label(mob):
            mob.move_to(movingdot1.get_center() + np.array([-0.2, 0, 0]))  # Move 10 units to the left of the dot
        def update_label2(mob):
            mob.move_to(movingdot2.get_center() + np.array([0.2, 0, 0]))  # Move 10 units to the left of the dot
        label1.add_updater(update_label)  # Attach the updater to the label
        label2.add_updater(update_label2)  # Attach the updater to the label
        polyhedra.faces[3].set_color(BLUE)
        polyhedra.faces[3].set_fill(opacity=1)

        

        movingdot1.set_opacity(1)
        label1.set_fill(opacity=1)
        self.camera.set_theta(4.712970756802005)
        self.camera.set_phi(2.6101398963575084)
        self.camera.set_gamma(0.0)
        self.wait(2)
        self.add(label1, label2, movingdot2, movingdot1)
        lineMN = self.draw_line_between_dots(movingdot1, movingdot2, is_dot=True, color=WHITE)
        lineBN = self.draw_line_between_dots(vertex_coords[1], movingdot2, is_dot=False, color=PURPLE)
        lineMD = self.draw_line_between_dots(vertex_coords[3], movingdot1, is_dot=False, color=GREEN)
        self.attach_line_updater(lineMN, movingdot2, movingdot1, is_dot=True)
        self.attach_line_updater(lineBN, vertex_coords[1], movingdot2, is_dot=False)
        self.attach_line_updater(lineMD, vertex_coords[3], movingdot1, is_dot=False)
        self.move_dot_to_final_position(movingdot1, label1, yellow_face_vertices, is_one=True)
        self.move_dot_to_final_position(movingdot2, label2, [vertex_coords[i] for i in faces_list[3]], is_one=False)
        self.wait()
        self.play(Write(lineMN), Write(lineBN), Write(lineMD), run_time=1.5)
        self.wait()
        self.play(
            MoveAlongPath(movingdot1, self.create_path_for_face(yellow_face_vertices, is_one=True), run_time=7),
            MoveAlongPath(label1, self.create_path_for_face(yellow_face_vertices, is_one=True), run_time=7),
            MoveAlongPath(movingdot2, self.create_path_for_face([vertex_coords[i] for i in faces_list[3]], is_one=False), run_time=7),
            MoveAlongPath(label2, self.create_path_for_face([vertex_coords[i] for i in faces_list[3]], is_one=False), run_time=7),
        )
        self.wait()
        # print(f"{scaled_poly.z_index=} , {tetra.z_index=}")
    def create_path_for_face(self, face_vertices, is_one):
        """
        Creates a VMobject representing a path for a dot to follow on the specified triangle face.

        Args:
            face_vertices: List of vertices defining the face (should be a triangle).

        Returns:
            A VMobject path with interpolated points.
        """
        A, B, C = [np.array(v) for v in face_vertices]

        def interpolate_inside_triangle(alpha, beta):
            # Gamma is implied as 1 - alpha - beta to ensure the point stays inside the triangle
            gamma = 1-alpha-beta
            return alpha * A + beta * B + gamma * C
        start_position = interpolate_inside_triangle(0.3, 0.4)
        start_position_2 = interpolate_inside_triangle(0.3, 0.4)
        # Define the path for the dot: Start near A, move to B, then C, then oscillate near the center
        if is_one == True:
            path_points = [
                start_position,  # C
                interpolate_inside_triangle(0.6, 0.3),  # Moving towards A again
                interpolate_inside_triangle(0.7, 0.1),  # Nearer to A
                interpolate_inside_triangle(0.5, 0.2),  # Back to the center
                interpolate_inside_triangle(0.2, 0.3),  # Close to C
                interpolate_inside_triangle(0.3, 0.4),                               
            ]
        else:
            path_points = [
                start_position,  # C
                interpolate_inside_triangle(0.6, 0.3),  # Moving towards A again
                interpolate_inside_triangle(0.7, 0.1),  # Nearer to A
                interpolate_inside_triangle(0.5, 0.2),  # Back to the center
                interpolate_inside_triangle(0.2, 0.3),  # Close to C 
                interpolate_inside_triangle(0.3, 0.4),                     
            ]
        path = VMobject()
        path.set_points_smoothly(path_points)
        return path
    def draw_line_between_dots(self, dot1, dot2, is_dot, color=WHITE, stroke_width=10):
        """
        Draw a line between two 3D dots.

        Args:
            dot1: The first Dot3D object.
            dot2: The second Dot3D object.
            color: The color of the line (default: WHITE).
            stroke_width: The stroke width of the line (default: 2).
        """
        # Get the positions of the dots
        if is_dot == True:
            start_pos = dot1.get_center()
            end_pos = dot2.get_center()
        else:
            start_pos = dot1
            end_pos = dot2.get_center()
        # Create a line connecting the dots
        
        line = Line(start_pos, end_pos, color=color, stroke_width=stroke_width)
        
        # Return the line object for potential further use
        return line
    def move_dot_to_final_position(self, movingdot, label, face_vertices, is_one):
        # Extract vertices
        A, B, C = [np.array(v) for v in face_vertices]

        # Define the final position inside the triangle
        def interpolate_inside_triangle(alpha, beta):
            # Gamma is implied as 1 - alpha - beta to ensure the point stays inside the triangle
            gamma = 1-alpha-beta
            return alpha * A + beta * B + gamma * C

        # Calculate the final position using the last set of alpha and beta values
        final_position1 = interpolate_inside_triangle(0.3, 0.4)
        final_position2 = interpolate_inside_triangle(0.3, 0.4)
        # Move the dot to the final position
        
        if is_one ==True:
            movingdot.move_to(final_position1)
            label.move_to(final_position1 + np.array([-0.2, 0, 0]))
        else:
            movingdot.move_to(final_position2)
            label.move_to(final_position2 + np.array([0.2, 0, 0]))
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

        # Attach the updater to the line
        line.add_updater(update_line)