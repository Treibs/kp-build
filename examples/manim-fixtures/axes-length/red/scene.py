from manim import *


class AxesWidthHeight(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                    width=6, height=4, tips=False)
        curve = axes.plot(lambda x: 0.4 * x ** 2 - 1, color=BLUE)
        self.play(Create(curve), run_time=0.5)
