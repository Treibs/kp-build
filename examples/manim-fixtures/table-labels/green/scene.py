from manim import *


class TableMobjectLabels(Scene):
    def construct(self):
        table = Table(
            [["1", "2"], ["3", "4"]],
            row_labels=[Text("R1"), Text("R2")],
            col_labels=[Text("C1"), Text("C2")],
        ).scale(0.6)
        self.play(FadeIn(table), run_time=0.5)
