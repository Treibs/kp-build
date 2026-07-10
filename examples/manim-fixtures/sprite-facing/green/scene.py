from manim import *


class SpriteFacing(Scene):
    def construct(self):
        # an asymmetric "sprite" so facing is visible
        sprite = Triangle(color=RED, fill_opacity=1).scale(0.3).rotate(-PI / 2)
        self.add(sprite)
        # rightward leg: as-is
        self.play(MoveAlongPath(sprite, Line(LEFT * 3, RIGHT * 3)), run_time=0.4)
        # leftward leg: horizontal MIRROR via flip(UP) — not a rotation;
        # rotating 180 degrees would put a walking sprite on its head
        sprite.flip(UP)
        self.play(MoveAlongPath(sprite, Line(RIGHT * 3, LEFT * 3)), run_time=0.4)
        self.wait(0.2)
