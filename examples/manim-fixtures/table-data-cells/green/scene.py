from manim import *


class MobjectTableData(Scene):
    def construct(self):
        table = MobjectTable(
            [[Text("1"), Text("2")], [Text("3"), Text("4")]],
            row_labels=[Text("R1"), Text("R2")],
            col_labels=[Text("C1"), Text("C2")],
        ).scale(0.6)
        self.play(FadeIn(table), run_time=0.5)
