from manim import *


class TableStringLabels(Scene):
    def construct(self):
        table = Table(
            [["1", "2"], ["3", "4"]],
            row_labels=["R1", "R2"],
            col_labels=["C1", "C2"],
        ).scale(0.6)
        self.play(FadeIn(table), run_time=0.5)
