from manim import *
import numpy as np
import os
from PIL import Image

# Get the base directory of the current script to find asset folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLAGS_DIR = os.path.join(BASE_DIR, "flags")
IMAGES_DIR = os.path.join(BASE_DIR, "images")


# Helper function to load general image assets (like the IMO logo)
def get_image_asset(image_filename, height=1.0):
    image_path = os.path.join(IMAGES_DIR, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image asset not found at path: {image_path}")

    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img_array = np.array(img)
    
    image_mobject = ImageMobject(img_array)
    image_mobject.set_height(height)
    return image_mobject
class PaneReveal(Scene):
    def construct(self):
        # --- 1. Load Assets ---
        # Note: You may need to adjust the file paths if they are not in the same directory.
        
        # Left Pane (The image will be cropped/resized to fit the screen)
        left_pane = get_image_asset("thumbnail1-1.png")
        
        # Right Pane
        right_pane = get_image_asset("thumbnail1-2.png")
        
        # Middle Polyhedra
        polyhedra = get_image_asset("thumbnail1polyhedra.png")
        
        # --- 2. Positioning and Initial Setup ---
        
        # Scale images to a reasonable size and aspect ratio for the screen
        # Adjust these scale factors as needed to match your desired look
        scale_factor = 8
        left_pane.scale(scale_factor)
        right_pane.scale(scale_factor)
        polyhedra.scale(scale_factor) # Slightly smaller for the center element
        left_pane.z_index = 0
        right_pane.z_index = 0
        polyhedra.z_index = 1  # Ensure polyhedra is on top
        # Calculate the initial position for the three elements to be side-by-side
        # The total width will be roughly: (Image Width * 3) / 2
        # Use VGroup to position them relative to each other easily

        # Group them temporarily to figure out the spacing, then ungroup
        # initial_group = Group(left_pane, polyhedra, right_pane)

        # self.add(initial_group)
        # Ungroup them for the animation
        # self.remove(initial_group) 
        
        # --- 3. Initial Display ---
        # Display all three components together at the start
        self.play(
            AnimationGroup(
                FadeIn(left_pane, shift=LEFT * 0.5),
                FadeIn(right_pane, shift=RIGHT * 0.5),
                FadeIn(polyhedra, scale=0.8), # slight zoom-in effect
                run_time=0.5, lag_ratio=0.1
            )
        )

        self.wait(1) # Hold the assembled image for a moment

        # --- 4. Animation Sequence (Slide & Fade) ---
        
        # Define the target positions for the sliding panes
        # Original was: 
        # left_target_pos = left_pane.get_center() + LEFT * 10
        # right_target_pos = right_pane.get_center() + RIGHT * 10
        
        # MODIFIED: Left pane slides up and left (e.g., -10 units left, +6 units up)
        # Using a diagonal vector LEFT + UP
        left_target_pos = left_pane.get_center() + (LEFT * 10 + UP * 6)
        
        # MODIFIED: Right pane slides down and right (e.g., +10 units right, -6 units down)
        # Using a diagonal vector RIGHT + DOWN
        right_target_pos = right_pane.get_center() + (RIGHT * 10 + DOWN * 6)
         # Define the pane sliding animation
        pane = AnimationGroup(
            left_pane.animate.move_to(left_target_pos),
            right_pane.animate.move_to(right_target_pos),
            run_time=3.5
        )

        # Play both animations with overlap: FadeOut starts 2s into pane motion
        self.play(
            AnimationGroup(
                pane,
                FadeOut(polyhedra, run_time=4.0),
                run_time=6,
                rate_func=smooth,
                lag_ratio=0.4  # Delay FadeOut start by ~2 seconds
            )
        )
        