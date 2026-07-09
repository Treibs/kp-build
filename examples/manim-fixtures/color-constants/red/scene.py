from manim import *


class BareBrown(Scene):
    def construct(self):
        # plain BROWN is not a Manim CE color constant
        trunk = Rectangle(width=0.6, height=2.0, color=BROWN)
        self.add(trunk)
        self.wait(0.2)
