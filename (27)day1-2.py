from manim import *
import os
from PIL import Image

# IMPORTANT: Ensure your files 'day1.png' and 'day2.png' are in the 'images' folder.
# Get the base directory of the current script to find asset folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Helper function to load general image assets
def get_image_asset(image_filename, height=5.0): # Using a larger height to fill the screen
    image_path = os.path.join(IMAGES_DIR, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image asset not found at path: {image_path}. Please ensure 'day1.png' and 'day2.png' are in your 'images' folder.")

    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img_array = np.array(img)
    
    image_mobject = ImageMobject(img_array)
    image_mobject.set_height(height)
    return image_mobject

class IMO_Test_Format_Scene(Scene):
    def construct(self):
        # 1. Load Images
        day1_image = get_image_asset("day1.png", height=6)
        day2_image = get_image_asset("day2.png", height=6)
        
        # 2. Define Final Positions
        # Create a Group to manage both images, then arrange and position the group
        image_group = Group(day1_image, day2_image)
        
        # Arrange them horizontally with a specific buffer, then center the group
        image_group.arrange(RIGHT, buff=0.8) 
        
        # Adjust vertical position to make room for text below
        image_group.shift(UP * 0.2)
        
        # 3. Define Text Labels (Day 1:/Day 2: is Blue, 4.5 hours is White)

        # --- CORRECTED TEXT CREATION using t2c ---
        
        # Use t2c to map the '4.5 hours' substring to WHITE. 
        # The default color for the rest of the text will be BLUE.
        t2c_map = {"4.5 hours": WHITE}

        day1_text = Text(
            "Day 1: 4.5 hours", 
            font_size=40, 
            color=BLUE,       # Default color for the whole string (i.e., "Day 1:")
            t2c=t2c_map,      # Overrides the color for "4.5 hours"
            weight=BOLD
        ) 

        day2_text = Text(
            "Day 2: 4.5 hours", 
            font_size=40, 
            color=BLUE,       # Default color for the whole string (i.e., "Day 2:")
            t2c=t2c_map,      # Overrides the color for "4.5 hours"
            weight=BOLD
        ) 
        
        # --- END CORRECTED TEXT CREATION ---

        # Position text directly below their respective images
        day1_text.next_to(day1_image, DOWN, buff=0.4)
        day2_text.next_to(day2_image, DOWN, buff=0.4)
        
        # 4. Prepare Off-Screen Starting Positions for a smooth slide-in
        day1_start_pos = day1_image.copy().shift(LEFT * (config.frame_width / 2 + day1_image.get_width() / 2 + 1))
        day2_start_pos = day2_image.copy().shift(RIGHT * (config.frame_width / 2 + day2_image.get_width() / 2 + 1))
        
        # Add the starting Mobjects to the scene for transformation
        self.add(day1_start_pos, day2_start_pos)

        # --- Animation Sequence ---
        
        # Slide Images In
        self.play(
            Transform(day1_start_pos, day1_image, run_time=1.5, path_arc=0),
            Transform(day2_start_pos, day2_image, run_time=1.5, path_arc=0),
        )
        self.wait(0.5)
        
        # Write Text Labels
        self.play(
            # Wrap the sequential animations in an AnimationGroup and set the lag_ratio
            AnimationGroup(
                Write(day1_text),
                Write(day2_text),
                # A lag_ratio of 1.0 means the second animation starts exactly when the first one finishes.
                # A lag_ratio of 0.5 means the second one starts halfway through the first's run_time.
                lag_ratio=0.6 # This ensures a clean sequential start
            ),
            run_time=1.0 # The run_time now dictates the time for the entire group
        )
        
        self.wait(3)
        
        # Clean up
        self.play(
            FadeOut(Group(day1_start_pos, day2_start_pos, day1_text, day2_text)),
            run_time=1.0
        )
        self.wait(1)