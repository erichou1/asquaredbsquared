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




        # --- Step 3: Highlight some tetrahedral cells ---
        cells = [
            [4, 0 , 1, 3],
            [0, 1, 2, 4],
            [1, 2, 3, 4]
        ]

        for cell in cells:
            highlight_vertices = [Dot3D(vertices_3d[i], color=GOLD, radius=0.08, z_index=10) for i in cell]

            highlight_faces = []
            for i in range(len(cell)):
                face = [cell[j] for j in range(len(cell)) if j != i]
                poly = Polygon(
                    *[vertices_3d[k] for k in face],
                    color=GOLD,
                    fill_color=GOLD,
                    fill_opacity=0.35,
                    shade_in_3d=True
                )
                poly.z_index = 5
                highlight_faces.append(poly)

            self.play(
                AnimationGroup(
                    *[Create(dot) for dot in highlight_vertices],
                    *[FadeIn(poly) for poly in highlight_faces],
                    run_time=0.8,
                    lag_ratio=0
                )
            )
            self.play(FadeOut(*highlight_vertices), FadeOut(*highlight_faces))

        self.wait(2)
        # --- Step 2: Labels (A–E) ---
        labels = ["A", "C", "D", "B", "E"]
        label_mobs = []
        for i, v in enumerate(vertices_3d):
            lbl = Text(labels[i], font_size=24, color=WHITE, weight=BOLD).move_to(v*1.3)
            if labels[i] == "E":
                lbl.shift(LEFT * 0.5)  # ✅ move E label left
            label_mobs.append(lbl)
        # ✅ Fix orientation
        self.add_fixed_orientation_mobjects(*label_mobs)

        self.play(*[Write(lbl) for lbl in label_mobs])
        self.wait(1)
        pentachoron_polys = [
            Polygon(
                *[vertices_3d[i] for i in face],
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=1,   # ✅ fully solid
                stroke_width=2.5,
                z_index = 1,
                shade_in_3d=True,
            )
            for face in pentachoron_faces
        ]

        self.play(
            *[FadeIn(poly) for poly in pentachoron_polys], 
            FadeOut(label_mobs[4]),
            FadeOut(*draw.face_polygons),
            FadeOut(*draw.edge_lines),
            run_time=1
                  )


        self.add(*pentachoron_polys)
        # self.remove(*draw.face_polygons, *draw.edge_lines)
        # self.play(
        #     FadeOut(*draw.face_polygons),
        #     FadeOut(*draw.edge_lines),
        # )
        self.wait(1)
        self.move_camera(
            phi=120*DEGREES, 
            theta=14*DEGREES,  # tweak until E is hidden
            gamma = 12.5*DEGREES,
            frame_center=([-0.4, 0, 0]),
            run_time=2.9
        )
        
        # --- Animate camera rotation so that E disappears ---
        # Rotates to a viewpoint aligned with ABCD
        dotted_line = DashedLine(
            vertices_3d[3],  # D
            vertices_3d[2],  # C
            color=WHITE,
            dash_length=0.1,
            stroke_width=4,
            fill_opacity =0.2,
            z_index = 2
        )
        # Vertices of tetrahedron ABCD
        tetra_vertices = [0, 1, 2, 3]  # A, B, C, D

        # Create lines for all edges of the tetrahedron
        tetra_edges = []
        for i in range(len(tetra_vertices)):
            for j in range(i+1, len(tetra_vertices)):
                if {tetra_vertices[i], tetra_vertices[j]} == {2, 3}:  # Skip C-D
                    continue
                line = Line(
                    vertices_3d[tetra_vertices[i]],
                    vertices_3d[tetra_vertices[j]],
                    color=WHITE,
                    stroke_width=5,
                    z_index =3
                )
                tetra_edges.append(line)
        # Animate the line
        self.play(
            Create(dotted_line), 
            *[Create(edge) for edge in tetra_edges],
            run_time=1)
        A = np.array([ 1.212047,  0.698410,  0.561484])
        B = np.array([-0.213717, -1.300964,  0.730697])
        C = np.array([ 0.213717, -0.276497, -1.466279])
        D = np.array([-1.212047,  0.879051,  0.174098])

 # Labels that follow
        label_M = Text("M", font_size=24, weight=BOLD)
        label_N = Text("N", font_size=24, weight=BOLD)
        # --- Step 1: Define gliding dots M and N ---
        M = Dot3D(color=WHITE, radius=0.125).move_to(A)
        N = Dot3D(color=WHITE, radius=0.125).move_to(D)
        # --- Make M & N, and their labels always render on top (robust fallback) ---
        M.z_index = 1000
        N.z_index = 1000
        label_M.z_index = 1010
        label_N.z_index = 1010

        # --- Step 2: Glide paths on faces ABC and ADC ---
        path_M = self.create_path_for_face([A,B,C], is_one=True)   # M glides on face ABC
        path_N = self.create_path_for_face([A,D,C], is_one=False)  # N glides on face ADC

        # Try to use bring_to_front if available; otherwise remove+add as fallback.
        def _keep_on_top(mob):
            # prefer built-in bring_to_front (faster if present)
            try:
                self.bring_to_front(mob)
            except Exception:
                # fallback: remove then add so it becomes the last-painted object
                # doing this each frame ensures painter's algorithm draws it last
                try:
                    self.remove(mob)
                    self.add_fixed_orientation_mobjects(mob)
                except Exception:
                    # defensive: ignore failures (shouldn't happen)
                    pass

        # Attach the updater so it runs every frame while the animation runs
        M.add_updater(_keep_on_top)
        N.add_updater(_keep_on_top)
        label_M.add_updater(_keep_on_top)
        label_N.add_updater(_keep_on_top)

        # Optional: small geometric nudge so dots float slightly above the face (prevents flicker)
        def _compute_face_normal(face_verts):
            A_pt, B_pt, C_pt = [np.array(v) for v in face_verts]
            n = np.cross(B_pt - A_pt, C_pt - A_pt)
            n = n / (np.linalg.norm(n) + 1e-9)
            # Make normal point roughly outward (choose direction so it points away from triangle centroid)
            centroid = (A_pt + B_pt + C_pt) / 3
            if np.dot(n, centroid) > 0:
                n = -n
            return n

        # nudge M on face ABC, and N on face ADC by a tiny epsilon
        eps = 0.03
        n_M = _compute_face_normal([A, B, C])
        n_N = _compute_face_normal([A, D, C])
        M.shift(n_M * eps)
        N.shift(n_N * eps)

        self.wait()

        # --- Clean up: remove the keep-on-top updaters once done (important) ---
        for mob in (M, N, label_M, label_N):
            mob.clear_updaters()
            # ensure final frame still shows them on top
            try:
                self.remove(mob)
                self.add_fixed_orientation_mobjects(mob)
            except Exception:
                pass

        self.add_fixed_orientation_mobjects(label_M, label_N)
        label_M.add_updater(lambda mob: mob.move_to(M.get_center() + np.array([0,0,-0.225])))
        label_N.add_updater(lambda mob: mob.move_to(N.get_center() + np.array([0,0.02,0.25])))


# Example vertices for tetrahedron ABCD
       

        # --- Step 3: Animate dots moving ---
        self.play(
            MoveAlongPath(M, path_M, run_time=8),
            MoveAlongPath(N, path_N, run_time=8),
        )       
        # Get camera direction (points from camera to scene center)
        # Small vector toward camera (roughly along z-axis)
        self.remove(*pentachoron_polys)
        self.remove(M)
        for poly in pentachoron_polys:
            poly.z_index = 0  
        M.z_index = 999
        self.add(M, *pentachoron_polys)
        self.wait()
        # --- Step 2.5: Dynamic lines MN, BN, MD ---
        def line_to_dot_edge(start, end, dot_radius):
            """Return a line from start to end, stopping at dot edge."""
            vec = end - start
            length = np.linalg.norm(vec)
            if length == 0:
                return start, end
            unit = vec / length
            # Shorten both ends by dot radius
            new_start = start + unit * dot_radius
            new_end = end - unit * (dot_radius)
            return new_start, new_end

        dot_radius = 0.05  # your M/N dot radius

        line_MN = always_redraw(lambda: Line(
            *line_to_dot_edge(M.get_center(), N.get_center(), dot_radius),
            color=YELLOW,
            stroke_width=8
        ))

        line_BN = always_redraw(lambda: Line(
            *line_to_dot_edge(B, N.get_center(), dot_radius),
            color=PURPLE,
            stroke_width=8
        ))

        line_MD = always_redraw(lambda: Line(
            *line_to_dot_edge(M.get_center(), D, dot_radius),
            color=RED,
            stroke_width=8
        ))

        self.play(Write(line_MN))
        self.play(Write(line_BN))
        self.play(Write(line_MD))
        self.wait()
        for poly in pentachoron_polys:
            poly.set_fill(opacity=0.5)

        self.play(
            *[poly.animate.set_fill(opacity=0) for poly in pentachoron_polys],
            FadeIn(label_mobs[4]),
            FadeIn(*draw.face_polygons),
            FadeIn(*draw.edge_lines),
            run_time=1,
            )
        self.wait()
        self.move_camera(
            phi=150*DEGREES, 
            theta=109*DEGREES, 
            gamma=110*DEGREES, 
            zoom=1.8,
            frame_center=np.array([0.85,-1.5,3.5]),  # centers A below B–D, pulls E forward
            run_time =4
        )
        self.wait()
        self.play(
            line_MN.animate.set_stroke(opacity=0.5),
            line_BN.animate.set_stroke(opacity=0),
            line_MD.animate.set_stroke(opacity=0),
            label_mobs[4].animate.move_to(vertices_3d[4] + LEFT*0.21),
            label_M.animate.move_to(M.get_center() + np.array([0.15, 0, 0.21])),
            label_N.animate.move_to(N.get_center() + np.array([0.145, 0.05, 0.15])),
            run_time=0.5
        )
        self.wait()
    # --- Helper: Glide inside face ---
    def create_path_for_face(self, face_vertices, is_one):
        A, B, C = [np.array(v) for v in face_vertices]

        def interpolate_inside_triangle(alpha, beta):
            gamma = 1 - alpha - beta
            return alpha*A + beta*B + gamma*C

        # Pick some path points inside triangle
        path_points = [
            interpolate_inside_triangle(0.1, 0.2), ###C
            interpolate_inside_triangle(0.4, 0.3),
            interpolate_inside_triangle(0.2, 0.6),###B
            interpolate_inside_triangle(0.81, 0.1), ### A
            interpolate_inside_triangle(0.25, 0.25),

            # interpolate_inside_triangle(0.6, 0.4),  # loop back
        ]
        path_points2 = [
            interpolate_inside_triangle(0.7, 0.2), ### A
            interpolate_inside_triangle(0.125, 0.125),###B
            
            interpolate_inside_triangle(0.2, 0.5),
            interpolate_inside_triangle(0.2, 0.7),###B
            interpolate_inside_triangle(0.4, 0.45),###B




            # interpolate_inside_triangle(0.6, 0.4),  # loop back
        ]

        path = VMobject()
        if is_one == True:
            path.set_points_smoothly(path_points)
        else:
            path.set_points_smoothly(path_points2)
        return path
        