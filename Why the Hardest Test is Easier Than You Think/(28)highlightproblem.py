from manim import *
import numpy as np
import os
from PIL import Image

# === Setup asset paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def get_image_asset(image_filename, height=1.0):
    image_path = os.path.join(IMAGES_DIR, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img_array = np.array(img)
    image_mobject = ImageMobject(img_array)
    image_mobject.set_height(height)
    return image_mobject


class HighlightProblemText(Scene):
    def construct(self):
        # === Load the problem image ===
        problem_image = get_image_asset("image.png", height=1.5)
        self.add(problem_image)

        # === Coordinates for highlights ===
        highlights = [
            {"shift": LEFT*1.03 + UP * 0.4, "width": 5.75, "height": 0.37},  # Line 1
            {"shift": RIGHT*3.8+UP * 0.4, "width": 3.95, "height": 0.37},              # Line 2 (two rows)
            {"shift": DOWN*0.05+RIGHT*3.75, "width": 4, "height": 0.37},             # Line 3
        ]

        self.play(FadeIn(problem_image))
        self.wait(0.5)

        # === Step 1: First highlight ===
        h = highlights[0]
        bg1 = Rectangle(width=h["width"], height=h["height"],
                        stroke_width=0, fill_color=BLUE, fill_opacity=0.25).shift(h["shift"])
        underline1 = Line(LEFT * h["width"]/2, RIGHT * h["width"]/2,
                          color=BLUE, stroke_width=5).next_to(bg1, DOWN, buff=0.05)
        self.play(FadeIn(bg1, run_time=0.5))
        self.play(Create(underline1, run_time=0.6))
        self.wait(1)
        self.play(FadeOut(bg1), FadeOut(underline1))

        # === Step 2: Second highlight (two rows) ===
        h = highlights[1]
        # two stacked rectangles
        bg2a = Rectangle(width=h["width"], height=h["height"],
                         stroke_width=0, fill_color=BLUE, fill_opacity=0.25).shift(h["shift"])
        bg2b = Rectangle(width=h["width"]+3.16, height=h["height"],
                         stroke_width=0, fill_color=BLUE, fill_opacity=0.25).shift(h["shift"] +LEFT*5.65+DOWN*0.41)

        underline2a = Line(LEFT * h["width"]/2, RIGHT * h["width"]/2,
                           color=BLUE, stroke_width=5).next_to(bg2a, DOWN, buff=0.05)
        underline2b = Line(LEFT * (h["width"]/2+1.58), RIGHT * (h["width"]/2+1.58),
                           color=BLUE, stroke_width=5).next_to(bg2b, DOWN, buff=0.05)

        self.play(FadeIn(bg2a, run_time=0.5), FadeIn(bg2b, run_time=0.5))
        self.play(
            Succession(
            Create(underline2a, run_time=0.6),
            Create(underline2b, run_time=0.6), 
            )
            )
        self.wait(1)
        self.play(FadeOut(bg2a), FadeOut(bg2b), FadeOut(underline2a), FadeOut(underline2b))

        # === Step 3: Third highlight ===
        h = highlights[2]
        bg3 = Rectangle(width=h["width"], height=h["height"],
                        stroke_width=0, fill_color=BLUE, fill_opacity=0.25).shift(h["shift"])
        underline3 = Line(LEFT * h["width"]/2, RIGHT * h["width"]/2,
                          color=BLUE, stroke_width=5).next_to(bg3, DOWN, buff=0.05)
        bg3b = Rectangle(width=h["width"]+2.35, height=h["height"],
                        stroke_width=0, fill_color=BLUE, fill_opacity=0.25).shift(h["shift"]+DOWN*0.405+LEFT*5.92)
        underline3b = Line(LEFT * (h["width"]/2+1.17500), RIGHT * (h["width"]/2+1.17500),
                          color=BLUE, stroke_width=5).next_to(bg3b, DOWN, buff=0.05)

        self.play(FadeIn(bg3, run_time=0.5), FadeIn(bg3b, run_time=0.5))
        self.play(
            Succession (
            Create(underline3, run_time=0.6),
            Create(underline3b, run_time=0.6),
            )
        )
        self.wait(1)
        self.play(FadeOut(bg3), FadeOut(underline3), FadeOut(bg3b), FadeOut(underline3b))

        self.wait()
