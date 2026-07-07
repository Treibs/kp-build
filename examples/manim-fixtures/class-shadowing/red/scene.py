from manim import *


class Text(Scene):  # shadows manim.Text under `from manim import *`
    def construct(self):
        label = Text("hello", font_size=40)
        self.add(label)
        self.wait(0.2)
