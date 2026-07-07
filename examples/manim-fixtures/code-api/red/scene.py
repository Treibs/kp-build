from manim import *


class CodeOldApi(Scene):
    def construct(self):
        block = Code(
            code="def add(a, b):\n    return a + b\n",
            language="python",
        )
        self.play(FadeIn(block), run_time=0.5)
