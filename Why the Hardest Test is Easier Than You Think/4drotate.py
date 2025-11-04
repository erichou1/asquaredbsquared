from manim import *
import math
import numpy as np

from manim import *

class DrawPolyhedron(AnimationGroup):
    def __init__(self, vertices, faces, **kwargs):
        # --- Vertices ---
        self.vertex_dots = [Dot3D(v, color=WHITE) for v in vertices]
        vertex_anims = AnimationGroup(*[Create(dot) for dot in self.vertex_dots], lag_ratio=0.1)

        # --- Edges ---
        edges = set()
        for face in faces:
            for i in range(len(face)):
                edge = (face[i], face[(i + 1) % len(face)])
                edges.add(tuple(sorted(edge)))

        self.edge_lines = [
            Line(vertices[s], vertices[e], color=BLUE, stroke_width=2.5, stroke_opacity=1)
            for s, e in edges
        ]
        edge_anims = AnimationGroup(*[Create(l) for l in self.edge_lines], lag_ratio=0.05)

        # --- Faces ---
        self.face_polygons = []
        for face in faces:
            if len(face) < 3:
                continue
            poly = Polygon(
                *[vertices[i] for i in face],
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.35,
                shade_in_3d=True,
            )
            self.face_polygons.append(poly)

        face_anims = AnimationGroup(*[Create(p) for p in self.face_polygons], lag_ratio=0.05)

        # --- Run animations in sequence ---
        super().__init__(LaggedStart(vertex_anims, edge_anims, face_anims, lag_ratio=0.5), **kwargs)

class TetraToPentachoron(ThreeDScene):
    def construct(self):
        # Adjusted camera so more faces are visible
        self.set_camera_orientation(phi=70*DEGREES, theta=-22.5*DEGREES, gamma=5*DEGREES, frame_center=([-0.28, -0.1, -0.6]), zoom=1.5)

        # --- Step 1: 5-cell (Pentachoron) ---
        vertices_4d = np.array([
            [1, 1, 1, -1/math.sqrt(5)],   # A
            [1, -1, -1, -1/math.sqrt(5)], # C
            [-1, 1, -1, -1/math.sqrt(5)], # D
            [-1, -1, 1, -1/math.sqrt(5)], # B
            [0, 0, 0, 4/math.sqrt(5)]     # E
        ])

        # Perspective projection 4D → 3D
        def project_4d_to_3d(v, d=3.0):
            w = d / (d - v[3])
            return np.array([v[0]*w, v[1]*w, v[2]*w])

        vertices_3d = np.array([project_4d_to_3d(v) for v in vertices_4d])

        # Center the shape
        centroid = np.mean(vertices_3d, axis=0)
        vertices_3d = vertices_3d - centroid

        # Rotate into a "show more faces" orientation
        def rotate(vec, axis, angle):
            axis = axis/np.linalg.norm(axis)
            cos, sin = np.cos(angle), np.sin(angle)
            return (vec*cos +
                    np.cross(axis, vec)*sin +
                    axis*np.dot(axis, vec)*(1-cos))

        vertices_3d = np.array([rotate(v, np.array([0,1,0]), 35*DEGREES) for v in vertices_3d])
        vertices_3d = np.array([rotate(v, np.array([1,0,0]), 25*DEGREES) for v in vertices_3d])

        # Faces of the 5-cell
        pentachoron_faces = [
            [0, 1, 2],
            [0, 1, 3],
            [0, 1, 4],
            [0, 2, 3],
            [0, 2, 4],
            [0, 3, 4],
            [1, 2, 3],
            [1, 2, 4],
            [1, 3, 4],
            [2, 3, 4],
        ]
        
        draw = DrawPolyhedron(vertices_3d, pentachoron_faces)
        self.play(draw, run_time = 2)
        self.wait(1)
        self.move_camera(
            theta=325*DEGREES,
            phi=70*DEGREES,
            # Set frame_center back to the origin [0, 0, 0] to maintain centering
            frame_center=[0, 0, 0], 
            run_time=13
        )