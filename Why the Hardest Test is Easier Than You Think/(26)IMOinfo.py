from manim import *
import numpy as np
import os
from PIL import Image
import math 
import random # <-- ADDED: For variable team sizes

# Get the base directory of the current script to find asset folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLAGS_DIR = os.path.join(BASE_DIR, "flags")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Helper function to load and process flag images
def get_flag_mobject(image_filename, height=0.35):
    image_path = os.path.join(FLAGS_DIR, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Flag not found at path: {image_path}")

    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    flag_array = np.array(img)
    
    flag_mobject = ImageMobject(flag_array)
    flag_mobject.set_height(height)
    return flag_mobject

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

class IMO_OpeningScene_Final(Scene):
    def construct(self):
        # --- 0. Initial Intro (Pinnacle) ---
        

        # --- 1. IMO Title & Logo Appears (Staging) ---

        imo_text_obj = Text("International Mathematical Olympiad (IMO)", font_size=37, color=WHITE, weight=BOLD)
        imo_logo_image = get_image_asset("imologo.webp", height=0.7) 
        full_imo_title = Group(imo_logo_image, imo_text_obj).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)

        # Fade out the intro and transition to the main title
        self.play(
            FadeIn(full_imo_title, shift=UP), 
            run_time=1.0
        )
        self.wait(0.5)

        # --- 2. Country Flags Slide In ---
        
        flag_filenames = [
            "us.png", "ca.png", "mx.png", "br.png", "gb.png",
            "fr.png", "de.png", "it.png", "cn.png", "jp.png",
            "kr.png", "in.png", "au.png", "nz.png", "za.png",
            "eg.png", "ru.png", "sa.png", "se.png", "no.png",
            "dk.png", "fi.png", "ch.png", "at.png", "gr.png",
            "tr.png", "ar.png", "cl.png", "co.png", "pe.png",
            "pk.png", "id.png", "th.png", "vn.png", "ph.png",
            "my.png", "sg.png", "bg.png", "pl.png", "hu.png",
            "cz.png", "sk.png", "ro.png", "ua.png", "ng.png",
            "ke.png", "gh.png", "ma.png", "il.png", "be.png",
            "nl.png", "lu.png", "ie.png", "cu.png", "ve.png",
            "bd.png", "lk.png", "np.png", "et.png", "mz.png",
            "ao.png", "tz.png", "ug.png", "dz.png", "tn.png",
            "ly.png", "ir.png", "iq.png", "sy.png", "lb.png",
            "jo.png", "ye.png", "om.png", "ae.png", "qa.png",
            "kw.png", "bh.png", "cy.png", "ge.png", "am.png",
            "az.png", "kz.png", "uz.png", "tj.png", "tm.png",
            "af.png", "bt.png", "bn.png", "kh.png", "la.png",
            "mm.png", "fj.png", "pg.png", "sb.png", "vu.png",
            "es.png", "pt.png", "cd.png", "by.png"
        ]
        
        num_display_flags = len(flag_filenames)
        flags_per_row = 10
        num_rows = math.ceil(num_display_flags / flags_per_row)

        temp_flags_mobjects = Group() 
        for i in range(num_display_flags):
            temp_flags_mobjects.add(get_flag_mobject(flag_filenames[i]))

        # Arrange them in a grid to get their final positions
        temp_flags_mobjects.arrange_in_grid(rows=num_rows, cols=flags_per_row, buff=(0.6, 0.4)).move_to(ORIGIN)
        temp_flags_mobjects.next_to(full_imo_title, DOWN, buff=0.75) 
        
        # Create the starting position off-screen
        flags_offscreen = temp_flags_mobjects.copy()
        flags_offscreen.shift(RIGHT * (config.frame_width / 2 + temp_flags_mobjects.get_width() / 2))

        slide_in_animations = []
        for i in range(num_display_flags):
            slide_in_animations.append(flags_offscreen.submobjects[i].animate.move_to(temp_flags_mobjects.submobjects[i].get_center()))
        
        self.add(flags_offscreen)
        self.wait(3)
        # Play the staggered slide-in animation
        self.play(
            LaggedStart(*slide_in_animations, lag_ratio=0.015),
            run_time=2.5
        )

        # --- 3. Dots (Contestants) Appear - Organized in Columns ---
        
        dots_per_flag_max = 6
        dot_radius = 0.04
        
        dot_colors = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
            "#FFA500", "#800080", "#008000", "#FFC0CB", "#8B4513", "#4682B4",
            "#D2B48C", "#E6E6FA", "#7CFC00", "#BA55D3", "#808000", "#DC143C",
            "#00BFFF", "#7FFF00"
        ]

        all_dots = VGroup() 
        dot_animations = []
        columns = 2 # Two vertical columns (3 rows)
        
        # Determine the index where we start introducing variable team sizes
        variable_start_index = int(num_display_flags * 0.5) # Start variability after ~65% of the flags

        for i, flag in enumerate(temp_flags_mobjects): 
            current_dot_color = dot_colors[i % len(dot_colors)]
            
            # Variable Team Size Logic
            if i < variable_start_index:
                num_dots_to_show = dots_per_flag_max # Full team
            else:
                # Randomly assign 3, 4, 5, or 6 members for the remaining teams
                num_dots_to_show = random.randint(3, dots_per_flag_max)

            dot_group = VGroup()
            
            # Calculate the overall height of the dot formation (3 rows high)
            dot_formation_height = 3.5 * dot_radius * 3 # 3 rows
            
            # Start position to vertically center the dots next to the flag
            start_y_offset = flag.get_center()[1] + dot_formation_height / 2 - dot_radius * 1.75
            
            for j in range(num_dots_to_show):
                dot = Dot(radius=dot_radius, color=current_dot_color)
                
                # Column and row calculation
                row = j // columns # 0, 0, 1, 1, 2, 2
                col = j % columns  # 0, 1, 0, 1, 0, 1
                
                # Position dots relative to the flag's right edge
                dot_x_pos = flag.get_right()[0] + 0.15 + col * dot_radius * 3.5
                dot_y_pos = start_y_offset - row * dot_radius * 3.5
                
                dot.move_to([dot_x_pos, dot_y_pos, 0])
                
                dot_group.add(dot)

            all_dots.add(dot_group)
            dot_animations.append(GrowFromCenter(dot_group))

        self.play(
            LaggedStart(*dot_animations, lag_ratio=0.01),
            run_time=2.5 
        )
        self.wait(1.5)
        