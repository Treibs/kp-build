from manim import *


class SceneAnatomy(Scene):
    def construct(self):
        square = Square(color=BLUE)
        self.add(square)
        self.play(square.animate.rotate(PI / 4), run_time=0.5)
        self.wait(0.2)
