from manim import *
import math
class TetrahedronZoom(ThreeDScene):
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
        self.camera.set_theta(6.8)
        self.camera.set_phi(1.1868238913561442)
        self.camera.set_gamma(0.0)
        # self.add(label1, label2, movingdot2, movingdot1)
        self.wait()
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
        phi, theta, focal_distance, gamma, zoom = self.camera.get_value_trackers()    
        # Create Polyhedron object
        prism = Polyhedron(cross_section_vertices, faces_list)
        prism.set_z_index = 1
        prism.set_fill(GREEN, opacity=1)
        prism.set_stroke(color=GREEN, width=2)
        for x in range(len(cross_section_vertices)):
            prism.graph[x].scale(0)
            # prism.graph[x].set_color(GREEN
        polyhedra.faces.set_fill(BLUE, opacity=0.2)
        self.add(prism)

        self.wait()
        #
        frame_center_tracker = ValueTracker(0)

        # Define a function to update the frame_center
        def update_frame_center():
            t = frame_center_tracker.get_value()  # Get interpolated value
            self.camera.frame_center = np.array([0, 0, t])  # Update the frame center
        
        # Add the updater
        frame_center_tracker.add_updater(lambda m: update_frame_center())

        # Animate phi, zoom, and frame_center simultaneously
        self.play(
            AnimationGroup(
                phi.animate.set_value(74 * DEGREES),  # Animate phi
                zoom.animate.set_value(5),           # Animate zoom
                frame_center_tracker.animate.set_value(0.65),  # Animate the frame center
                polyhedra.animate.set_opacity(0),
                axes.animate.set_opacity(0),
                label.animate.set_opacity(0),
                lag_ratio=0                          # Play all animations at the same time
            ),
            run_time=2.5
        )

        # Remove the updater to avoid unnecessary updates later
        frame_center_tracker.clear_updaters()
        print(f"{self.camera.get_theta()}, {self.camera.get_phi()}, {self.camera.get_gamma()}")

        self.wait(4)