from manim import *
from typing import TYPE_CHECKING, Callable, Iterable, Sequence
import math
class DrawPolyhedron(AnimationGroup):
    def __init__(self, polyhedron, **kwargs):
        """
        Custom animation to draw a polyhedron step-by-step.
        Args:
            polyhedron: A Polyhedron object with `vertex_coords` and `faces_list` attributes.
        """
        # Extract vertices and faces from the polyhedron
        vertices = polyhedron.vertex_coords
        faces = polyhedron.faces_list

        # Create vertex dots
        vertex_dots = [Dot3D(vertex, color=WHITE) for vertex in vertices]
        vertex_animations = AnimationGroup(*[Create(dot) for dot in vertex_dots], lag_ratio=0.2)
        # Create edges by iterating over faces (avoiding duplicates)
        edges = set()
        for face in faces:
            for i in range(len(face)):
                edge = (face[i], face[(i + 1) % len(face)])  # Wrap around to connect the last to the first
                edges.add(tuple(sorted(edge)))  # Avoid duplicate edges
        self.edge_lines = [Line(vertices[start], vertices[end], color=WHITE) for start, end in edges]
        edge_animations = AnimationGroup(*[Create(line) for line in self.edge_lines], lag_ratio=0.1)
        # Create face polygons
        self.face_polygons = [
            Polygon(*[vertices[vertex] for vertex in face], color=BLUE, fill_opacity=0.5)
            for face in faces if len(face) > 2  # Skip degenerate faces
        ]
        face_animations = AnimationGroup(*[Create(polygon) for polygon in self.face_polygons], lag_ratio=0.1)
        super().__init__(LaggedStart(vertex_animations, edge_animations, face_animations, lag_ratio=0.6))
    
    def animate_faces_and_edges_opacity(self, scene, face_indices, not_face_indices, edge_indices, target_color, target_opacity, run_time=1):
        """
        Animate the opacity change of specific faces and edges of the polyhedron at the same time.
        """
        face_animations = []
        edge_animations = []

        # Add face animations
        for index in face_indices:
            if 0 <= index < len(self.face_polygons):  # Ensure valid face indices
                face = self.face_polygons[index]
                face_animations.append(face.animate(run_time=run_time).set_fill(opacity=target_opacity))
        for index in not_face_indices:
            if 0 <= index < len(self.face_polygons):  # Ensure valid face indices
                face = self.face_polygons[index]
                face_animations.append(
                    face.animate(run_time=run_time).set_fill(opacity=0.75)
                    .set_color(target_color)
                )

        # Add edge animations
        for index in edge_indices:
            if 0 <= index < len(self.edge_lines):  # Ensure valid edge indices
                edge = self.edge_lines[index]
                edge_animations.append(edge.animate(run_time=run_time).set_stroke(width=target_opacity))
        # Play all animations concurrently
        scene.play(*face_animations, *edge_animations)    
    def animate_face_opacity(self, scene, face_indices, target_opacity, run_time=1):
        """Animate the opacity change of specific faces of the polyhedron."""
        animations = []
        for index in face_indices:
            if 0 <= index < len(self.face_polygons):  # Ensure valid indices
                face = self.face_polygons[index]
                animations.append(
                    face.animate(run_time=run_time).set_fill(opacity=target_opacity)
                )
        return animations
    def animate_edge_opacity(self, scene, edge_indices, target_opacity, run_time=1):
        """Animate the opacity change of specific edges of the polyhedron."""
        animations = []
        for index in edge_indices:
            if 0 <= index < len(self.edge_lines):  # Ensure valid indices
                face = self.edge_lines[index]
                animations.append(
                    face.animate(run_time=run_time).set_fill(opacity=target_opacity)
                )
        scene.play(*animations)
class SquarePyramidScene(ThreeDScene):
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
        self.remove(*tex_labels)
        plane_vertices = [vertex_coords[i] for i in [2, 1, 3]]  # Triangle ABC
        plane = self.create_plane(plane_vertices)
        scaled_poly = plane.copy().scale(4).set_fill(opacity=0.2)
        self.play(Write(axes))
        self.wait()
        polyhedra = DrawPolyhedron(tetra)
        self.play(LaggedStart(polyhedra))
        self.wait(2)

        # axes.set_z_index = -1  # Below everything
        # tetra.set_z_index = 1  # Above the planes
        # polyhedra.set_z_index = 1

        axes.set_z_index = -1  # Below everything
        self.play(Create(VGroup(*tex_labels)))

        self.move_camera(theta=270 *DEGREES, run_time=2)        
        self.wait(4)
        # self.play(Create(plane))  # Create the plane
        self.move_camera(zoom = 1.5)
        # plane.set_z_index = 0  # Below the tetrahedron
        # scaled_poly.set_z_index = 0  # Same as the plane
        yellow_face_vertices = [vertex_coords[i] for i in faces_list[1]]
        polyhedra.animate_faces_and_edges_opacity(self, face_indices=[0, 2, 3], not_face_indices=[1], edge_indices=[1, 2, 3, 4, 5], target_color=YELLOW, target_opacity=0, run_time=1)
        # A, B, C = [np.array(v) for v in face_vertices]
        #Define a white  dot
        print(f"{self.camera.get_theta()}, {self.camera.get_phi()}, {self.camera.get_gamma()}")

        # movingdot1 = Dot3D(color=WHITE, radius=0.075, shade_in_3d=True)
        # movingdot2 = Dot3D(color=WHITE, radius=0.075, shade_in_3d=True)
        # movingdot1.z_index = 10
        # movingdot2.z_index = 10
        # movingdot1.set_opacity(1)
        # movingdot2.set_opacity(1)
        # label1 = Text("M", weight=BOLD, slant=ITALIC).scale(0.375)
        # label2 = Text("N", weight=BOLD, slant=ITALIC).scale(0.375)
        
        # self.add_fixed_orientation_mobjects(label1, label2)
        # self.remove(label1, label2)

        # # Update function to ensure the label stays 10 units to the left of the dot
        # def update_label(mob):
        #     mob.move_to(movingdot1.get_center() + np.array([-0.2, 0, 0]))  # Move 10 units to the left of the dot
        # def update_label2(mob):
        #     mob.move_to(movingdot2.get_center() + np.array([-0.2, 0, 0]))  # Move 10 units to the left of the dot

        # label1.add_updater(update_label)  # Attach the updater to the label
        # label2.add_updater(update_label2)  # Attach the updater to the label
        # self.wait(1)
        # self.begin_ambient_camera_rotation(2.5*DEGREES, about="theta")
        # self.wait()
        # self.animate_dot_on_face(label1, movingdot1, yellow_face_vertices)
        # self.wait(2)
        # self.stop_ambient_camera_rotation(about='theta')
        
        # self.play(
        #     movingdot1.animate(run_time=1).set_opacity(0.75),
        #     label1.animate(run_time=1).set_fill(opacity=0.5),
        #     polyhedra.animate_face_opacity(self, face_indices=[1], target_opacity=0.5),
        #     run_time =1
        # )

        # self.wait()
        

        # polyhedra.animate_faces_and_edges_opacity(self, face_indices=[0, 2], not_face_indices=[3], edge_indices=[1, 2, 3, 4, 5], target_color=BLUE,  target_opacity=0, run_time=1)
        # self.begin_ambient_camera_rotation(-2.5*DEGREES, about="theta")
        # self.begin_ambient_camera_rotation(12*DEGREES, about="phi")
        # self.wait()        
        # self.animate_dot_on_face(label2, movingdot2, [vertex_coords[i] for i in faces_list[3]])
        # self.wait()
        # self.stop_ambient_camera_rotation(about='phi')
        # self.stop_ambient_camera_rotation(about='theta')
        # lineMN = self.draw_line_between_dots(movingdot1, movingdot2, is_dot=True, color=WHITE)
        # lineBN = self.draw_line_between_dots(vertex_coords[1], movingdot2, is_dot=False, color=RED)
        # lineMD = self.draw_line_between_dots(vertex_coords[3], movingdot1, is_dot=False, color=GREEN)
        # self.play(
        #     movingdot1.animate(run_time=1).set_opacity(1),
        #     label1.animate(run_time=1).set_fill(opacity=1),
        #     run_time=1
        # )
        # self.wait(2)
        
        # self.play(Write(lineMN), Write(lineBN), Write(lineMD))
        # self.wait()
        # self.continue_animate_dot_on_face(label2, movingdot2, [vertex_coords[i] for i in faces_list[3]]),
        # self.continue_animate_dot_on_face(label1, movingdot1, yellow_face_vertices)
        # self.play(ReplacementTransform(plane, scaled_poly, run_time=1))

        self.wait(2)
        # print(f"{scaled_poly.z_index=} , {tetra.z_index=}")
    def create_plane(self, vertices):
        # Create a plane on the face defined by the vertices
        poly = Polygon(*[np.array(v) for v in vertices], color=RED, fill_opacity=0)

        return poly
    def animate_dot_on_face(self, label, movingdot, face_vertices, run_time=3):
        """
        Animates a red dot moving around on a specified face of the tetrahedron.
        The dot starts close to vertex A, moves to vertex B, then vertex C, and finally oscillates around the center.
        
        Args:
            face_vertices: List of vertices defining the face (should be a triangle).
            run_time: Duration of the animation.
        """
        # Convert face vertices to numpy arrays
        A, B, C = [np.array(v) for v in face_vertices]
        start_position = 0.1 * A + 0.1 * B + 0.8 * C  # Weighted near vertex A
        # Define a white  dot
        movingdot.move_to(start_position)


        # Define a label for the moving dot
        movingdot.set_opacity(1)
        self.play(FadeIn(movingdot, label))
        # Define a function to generate points inside the triangle using parametric coordinates
        def interpolate_inside_triangle(alpha, beta):
            # Gamma is implied as 1 - alpha - beta to ensure the point stays inside the triangle
            gamma = 1 - alpha - beta
            return alpha * A + beta * B + gamma * C

        # Define the path for the dot: Start near A, move to B, then C, then oscillate near the center
        path_points = [
            interpolate_inside_triangle(0.1, 0.1),  # Start near Vertex A
            interpolate_inside_triangle(0.4, 0.4),  # Glide near the center
            interpolate_inside_triangle(0.2, 0.4),  # Move closer to Vertex C
        ]

        # Create the path object
        path = VMobject()
        path.set_points_smoothly(path_points)

        # Animate the dot along the path and move the label along with it
        self.play(
            MoveAlongPath(movingdot, path, run_time=run_time),
            MoveAlongPath(label, path, run_time=run_time)
        )
        # Remove the moving dot and label after animation
    def continue_animate_dot_on_face(self, label, movingdot, face_vertices, run_time=3):
        A, B, C = [np.array(v) for v in face_vertices]

        normal = np.cross(B - A, C - A)
        normal = normal / np.linalg.norm(normal)  # Normalize to unit vector
        offset = 10 * normal
        # Define a label for the moving dot
            # Define a function to generate points inside the triangle using parametric coordinates
        def interpolate_inside_triangle(alpha, beta):
            # Gamma is implied as 1 - alpha - beta to ensure the point stays inside the triangle
            gamma = 1 - alpha - beta
            return alpha * A + beta * B + gamma * C + offset

        # Define the path for the dot: Start near A, move to B, then C, then oscillate near the center
        path_points = [
            interpolate_inside_triangle(0.1, 0.1),  # Start near Vertex A
            interpolate_inside_triangle(0.4, 0.4),  # Glide near the center
            interpolate_inside_triangle(0.2, 0.4),  # Move closer to Vertex C
        ]

        # Create the path object
        path = VMobject()
        path.set_points_smoothly(path_points)

        # Animate the dot along the path and move the label along with it
        self.play(
            MoveAlongPath(movingdot, path, run_time=run_time),
            MoveAlongPath(label, path, run_time=run_time)
        )
    def draw_line_between_dots(self, dot1, dot2, is_dot, color=WHITE, stroke_width=2):
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
        line = Line3D(start_pos, end_pos, color=color, stroke_width=stroke_width)

        # Return the line object for potential further use
        return line