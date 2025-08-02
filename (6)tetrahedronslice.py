from manim import *
import math
class TetrahedronSlice(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        
        vertex_coords = [
                    [1, -1/math.sqrt(3), 0], #A
                    [0, 2/math.sqrt(3), 0], #B
                    [0, 0, 4/math.sqrt(6)], #C
                    [-1, -1/math.sqrt(3), 0] #D
                ]
        faces_list = [
            [0, 1, 3],
            [1, 2, 3],
            [3, 0, 2],
            [0, 1, 2]
        ]
        edges = [
            [0, 1], [1, 2], [2, 0], [0, 3], [1, 3], [2, 3]
        ]
        labels = "ABCD"
        tex_labels = []
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        for i, vertex in enumerate(vertex_coords):
            # Position the labels outside the tetrahedron
            direction = np.array(vertex)  # Direction is just the vertex position
            label_position = direction / np.linalg.norm(direction) * 1.65  # Move outward by a factor of 1.5
            label = Text(labels[i], weight=BOLD, slant=ITALIC).scale(0.5).move_to(label_position + np.array([0, 0, 0.2]))  # Slight offset in Z direction
            tex_labels.append(label)
        self.add_fixed_orientation_mobjects(*tex_labels)
        self.add(axes)
        polyhedra = Polyhedron(vertex_coords, faces_list)
        polyhedra.z_index = 0
        self.add(polyhedra)

    
        self.add(*tex_labels)

        # self.move_camera(theta=270 *DEGREES, run_time=0.1)
        self.move_camera(zoom = 1.5, run_time=0.1)
        
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
        
        movingdot1.set_opacity(1)
        label1.set_fill(opacity=1)
        self.camera.set_theta(4.712970756802005)
        self.camera.set_phi(2.6101398963575084)
        self.camera.set_gamma(0.0)
        # self.add(label1, label2, movingdot2, movingdot1)
        self.wait()
        self.move_camera(phi=68*DEGREES, run_time = 2)
        self.wait()
        # self.move_camera(theta = 398*DEGREES, run_time = 3)         
        # self.highlight_cross_section(vertex_coords, edges)
        cross_section_vertices = [[0.333,-0.577,0.0],
                                  [-0.333,0.577,0.0],
                                  [-0.333,-0.192,1.089],
                                  [0.211,-0.577,0.0],
                                  [-0.395,0.471,0.0],
                                  [-0.395,-0.228,0.989],
                                  ]
        # print(f"{scaled_poly.z_index=} , {tetra.z_index=}")
        # Create the polyhedron by defining faces from vertices and edges
        faces_list = [
            [0, 1, 2], [3, 4, 5],  # The two triangular faces
            [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]  # The lateral faces
        ]
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()    
        # Create Polyhedron object
        prism = Polyhedron(cross_section_vertices, faces_list)
        prism.set_z_index = 1
        prism.set_fill(GREEN, opacity=1)
        prism.set_stroke(color=GREEN, width=2)
        for x in range(len(cross_section_vertices)):
            prism.graph[x].scale(0)
            # prism.graph[x].set_color(GREEN
        self.play(polyhedra.faces.animate.set_fill(BLUE, opacity=0.2), run_time=2)  # Fade the polyhedron opacity to 0.3

        self.wait()
        theta.animate(run_time=2).set_value(270 * DEGREES),  # This will animate the theta

        self.play(
                FadeIn(prism, run_time=1.5),
                theta.animate(run_time=3).set_value(290 * DEGREES),  # This will animate the theta
        )
        self.bring_to_back(polyhedra)
        self.bring_to_front(prism)
        self.play(
            theta.animate(run_time=3).set_value(389.611301 * DEGREES),  # This will animate the theta

        )
        print(f"{self.camera.get_theta()}, {self.camera.get_phi()}, {self.camera.get_gamma()}")
        self.bring_to_back(polyhedra)
        self.bring_to_front(prism)
        self.wait()
        
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
    def highlight_cross_section(self, vertex_coords, edges):
    # Define the slicing plane: y = -1.73x
        
        def find_intersection(start, end):
            direction = np.array(end) - np.array(start)
            # Calculate the intersection parameter t for the plane equation y = -1.73x
            t = (start[1] - (-1.73 * start[0]) + 0.3) / (-(direction[1] + 1.73 * direction[0]))
            #+0.3 and 0
            
            if t is not None and 0 <= t <= 1:
                return start + t * direction
            return None

        slice_points = []

        # Find intersection points with tetrahedron edges
        for edge in edges:
            start, end = np.array(vertex_coords[edge[0]]), np.array(vertex_coords[edge[1]])
            intersection = find_intersection(start, end)
            if intersection is not None:
                slice_points.append(intersection)

        # Ensure points are in order to create a valid polygon
        slice_points = sorted(slice_points, key=lambda p: (p[0], p[2]))

        # Create the slice polygon
        if len(slice_points) >= 3:

            slice_polygon = Polygon(*slice_points, color=YELLOW, fill_opacity=0.6, stroke_width=2)
            self.add(slice_polygon)
            slice_vertices = slice_polygon.get_vertices()
            print(f"{slice_vertices}")

            # Animate the slice
            self.play(
                FadeIn(slice_polygon),
                run_time=2
            )
            self.wait()

            # Optional: Animate removing the slice
            self.play(
                FadeOut(slice_polygon),
                run_time=2
            )
