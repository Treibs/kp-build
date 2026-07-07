from manim import *


class DtUpdaterLifecycle(Scene):
    def construct(self):
        square = Square(side_length=0.5, color=BLUE)

        def spin(mob, dt):
            mob.rotate(2 * dt)

        square.add_updater(spin)
        self.add(square)
        self.wait(0.5)
        square.remove_updater(spin)
        self.play(square.animate.shift(RIGHT), run_time=0.5)
