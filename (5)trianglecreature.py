from manim import *

class SpeechBubble(Scene):
    def construct(self):
        # Create the speech bubble outline
        bubble = SVGMobject("./speech_bubble.svg")
        # bubble.flip(axis=UP)
        bubble.set_stroke(width=4, color=WHITE)
        bubble.set_fill(color=BLACK, opacity=1)
        bubble.scale(2)

        # Position the bubble
        bubble.to_corner(DOWN + RIGHT)

        # Create the text inside the bubble
        text = Tex(r"Lets Simplify!", font_size=40)
        text.set_color(WHITE)
        print(f"{bubble.get_center()}")

        text.move_to(bubble.get_center() + (0, 0.6, 0))

        # Group the bubble and text together for animation
        bubble_group = VGroup(bubble, text)

        # Animate the bubble appearing
        self.play(DrawBorderThenFill(bubble, run_time=1.5))
        self.play(Write(text), run_time=1.5)

        # Pause to display the bubble
        # self.wait(1)

        # Animate the bubble disappearing
        self.play(FadeOut(bubble_group, shift=DOWN), run_time=1.5)

        # End scene
        self.wait(1)