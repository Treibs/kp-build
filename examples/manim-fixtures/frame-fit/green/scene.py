from manim import *


class FitsTheFrame(Scene):
    def construct(self):
        # compose against config.frame_height / frame_width so content
        # stays inside the visible frame — off-frame content renders
        # exit 0 and is only caught on video
        tower = Rectangle(width=1, height=config.frame_height * 3)
        tower.scale_to_fit_height(config.frame_height - 1)
        label = Text("fits").next_to(tower, RIGHT)
        self.add(tower, label)
        self.wait(0.2)
