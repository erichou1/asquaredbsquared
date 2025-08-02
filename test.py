from manim import *
from typing import TYPE_CHECKING, Callable, Iterable, Sequence
import math
class MyCamera(ThreeDCamera):
    def transform_points_pre_display(self, mobject, points):
        if getattr(mobject, "fixed", False):
            return points
        else:
            return super().transform_points_pre_display(mobject, points)
      
class MyThreeDScene(ThreeDScene):
    def __init__(self, camera_class=MyCamera, ambient_camera_rotation=None,
                 default_angled_camera_orientation_kwargs=None, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)

def make_fixed(*mobs):
    for mob in mobs:
        mob.fixed = True
        for submob in mob.family_members_with_points():
            submob.fixed = True

class Test(MyThreeDScene):
    def construct(self):
        r = Rectangle()
        tex = MathTex("{{f(x,y)}} = {{ e^{-(x^2 + y^2)} }}").to_edge(UP * 1.1)
        tex[2].set_color(YELLOW)
        texN = MathTex( "{{f(x,y)}} = " 
            "{{\\int_{-2}^2 \\int_{-2}^2 f(x,y) dx dy \\approx \\sum_{i=0}^{n-1} \\sum_{j=0}^{m-1} f(i^*,j^*) \\Delta a}}")
        make_fixed(tex, texN)
        texN.to_edge(UP * 1.1)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.5)
        self.add(r)
        self.add(tex)
        self.wait()
        self.play(TransformMatchingTex(tex, texN))
        self.wait()