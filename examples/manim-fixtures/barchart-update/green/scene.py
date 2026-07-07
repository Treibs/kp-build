from manim import *


class BarChartValueUpdate(Scene):
    def construct(self):
        chart = BarChart(values=[2, 4, 3], y_range=[0, 6, 2],
                         x_length=6, y_length=4)
        self.add(chart)
        self.play(chart.animate.change_bar_values([5, 1, 4]), run_time=0.5)
