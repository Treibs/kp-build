from manim import *


class CameraFollow(MovingCameraScene):
    def construct(self):
        runner = Dot(LEFT * 5, color=RED)
        marks = VGroup(*[Line(DOWN * 0.2, UP * 0.2).move_to(RIGHT * x)
                         for x in range(-5, 6, 2)])
        self.add(marks, runner)
        self.camera.frame.set(width=6)
        # continuous follow: an updater on camera.frame tracks the mover
        # (the one-shot form is frame.animate.move_to — see moving-camera)
        self.camera.frame.add_updater(lambda f: f.move_to(runner.get_center()))
        self.play(runner.animate.move_to(RIGHT * 5), run_time=1, rate_func=linear)
        self.camera.frame.clear_updaters()
        self.wait(0.2)
