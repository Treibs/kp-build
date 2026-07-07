from manim import *


class MathVsText(Scene):
    def construct(self):
        formula = MathTex(r"e^{i\pi} + 1 = 0")
        caption = Text("Euler's identity", font_size=24).next_to(formula, DOWN)
        self.play(Write(formula), FadeIn(caption), run_time=0.5)
