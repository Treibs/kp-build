from manim import *


class CodeParagraphConfig(Scene):
    def construct(self):
        block = Code(
            code_string="def add(a, b):\n    return a + b\n",
            language="python",
            paragraph_config={"font_size": 18},
        )
        self.play(FadeIn(block), run_time=0.5)
