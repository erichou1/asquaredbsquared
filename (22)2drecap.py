from manim import *
import math
import numpy as np

class DrawPolyhedron(AnimationGroup):
    def __init__(self, polyhedron, **kwargs):
        vertices = polyhedron.vertex_coords
        faces = polyhedron.faces_list

        # Vertex dots
        vertex_dots = [Dot3D(vertex, color=WHITE) for vertex in vertices]
        vertex_animations = AnimationGroup(*[Create(dot) for dot in vertex_dots], lag_ratio=0.2)

        # Edges
        edges = set()
        for face in faces:
            for i in range(len(face)):
                edge = (face[i], face[(i + 1) % len(face)])
                edges.add(tuple(sorted(edge)))

        self.edge_lines = [
            Line(vertices[s], vertices[e], color=BLUE, stroke_opacity=1, stroke_width=4.5)
            for s, e in edges
        ]
        edge_animations = AnimationGroup(*[Create(l) for l in self.edge_lines], lag_ratio=0.1)

        # Faces
        self.face_polygons = []
        for face in faces:
            if len(face) < 3:
                continue
            polygon = Polygon(
                *[vertices[i] for i in face],
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.4,
                shade_in_3d=True,
            )
            self.face_polygons.append(polygon)

        face_animations = AnimationGroup(*[Create(p) for p in self.face_polygons], lag_ratio=0.1)

        super().__init__(LaggedStart(vertex_animations, edge_animations, face_animations, lag_ratio=0.6))


class TetrahedronZoom(ThreeDScene):
    def construct(self):
        # Camera
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES, zoom=1.2)

        # --- Step 1: Triangle (left) ---
        triangle = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=0.5)
        triangle.scale(1.2)
        self.add_fixed_orientation_mobjects(triangle)
        self.remove(triangle)
        self.play(Write(triangle))
        self.wait(1)

        # --- Step 2: Arrow (center) ---


        # --- Step 2: Arrow in the middle ---
        arrow = Arrow(start=LEFT*1, end=RIGHT*1, buff=0.1,  color=BLUE)
        arrow.tip = arrow.tip.scale(1.5)
        
        arrow.move_to([0, 0, 0])  # center

        self.add_fixed_orientation_mobjects(arrow)

        # Animate strictly left-to-right growth
        self.play(GrowArrow(arrow))
        self.wait(1)
        # --- Step 3: Tetrahedron (right) ---
        vertex_coords = [
            [1, -1/math.sqrt(3), 0], # A
            [0, 2/math.sqrt(3), 0],  # B
            [0, 0, 4/math.sqrt(6)],  # C
            [-1, -1/math.sqrt(3), 0] # D
        ]
        faces_list = [
            [0, 1, 3],
            [1, 2, 3],
            [3, 0, 2],
            [0, 1, 2]
        ]
        labels = "ABCD"

        tetra = Polyhedron(vertex_coords, faces_list)

        # Labels
        tex_labels = []
        # Vertex labels 
        tex_labels = []
        for i, vertex in enumerate(vertex_coords): 
            direction = np.array(vertex) 
            label_position = direction / np.linalg.norm(direction) * 1.65 
            label = Text(labels[i], weight=BOLD, slant=ITALIC).scale(0.5).move_to(label_position + np.array([0, 0, 0.2])) 
            tex_labels.append(label)
        self.add_fixed_orientation_mobjects(*tex_labels)

        # Animate tetrahedron
        self.play(DrawPolyhedron(tetra))
        # self.add(tetra)
        self.add(*tex_labels)

        self.wait(3)
