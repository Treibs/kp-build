from manim import *


class GreetingScene(Scene):
    def construct(self):
        label = Text("hello", font_size=40)
        self.play(FadeIn(label), run_time=0.5)
