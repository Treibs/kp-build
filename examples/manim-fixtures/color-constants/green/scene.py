from manim import *


class BrownsThatExist(Scene):
    def construct(self):
        # CE's brown constants: LIGHT_BROWN, DARK_BROWN, GRAY_BROWN/GREY_BROWN
        trunk = Rectangle(width=0.6, height=2.0, color=DARK_BROWN,
                          fill_color=LIGHT_BROWN, fill_opacity=1)
        ground = Line(LEFT * 3, RIGHT * 3, color=GREY_BROWN)
        ground.next_to(trunk, DOWN, buff=0)
        self.add(trunk, ground)
        self.wait(0.2)
