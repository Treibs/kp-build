from manim import *


class StaggeredFades(Scene):
    def construct(self):
        dots = VGroup(*[Dot(radius=0.1) for _ in range(3)]).arrange(RIGHT, buff=0.5)
        self.play(
            AnimationGroup(*[FadeIn(d, run_time=0.5) for d in dots], lag_ratio=0.5)
        )
