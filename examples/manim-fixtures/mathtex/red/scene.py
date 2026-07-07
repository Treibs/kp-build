from manim import *


class DollarMathTex(Scene):
    def construct(self):
        formula = MathTex(r"$e^{i\pi} + 1 = 0$")
        self.play(Write(formula), run_time=0.5)
