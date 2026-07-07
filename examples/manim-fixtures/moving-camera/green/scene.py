from manim import *


class CameraZoom(MovingCameraScene):
    def construct(self):
        dot = Dot(RIGHT * 2, color=RED)
        self.add(dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(dot), run_time=0.5)
