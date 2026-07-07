from manim import *


class ZoomBoxes(MovingCameraScene):
    def construct(self):
        box_configs = [
            ("Box A", LEFT * 4.5, BLUE),
            ("Box B", ORIGIN,     GREEN),
            ("Box C", RIGHT * 4.5, RED),
        ]

        groups = VGroup()
        for label, pos, color in box_configs:
            rect = Rectangle(width=2.8, height=2.0, color=color, stroke_width=3)
            text = Text(label, font_size=42, color=color)
            grp = VGroup(rect, text)
            grp.move_to(pos)
            groups.add(grp)

        self.play(FadeIn(groups))
        self.wait(0.4)

        self.camera.frame.save_state()

        for grp in groups:
            self.play(
                self.camera.frame.animate
                    .move_to(grp)
                    .set_width(grp.width + 2.0),
                run_time=1.2,
            )
            self.wait(0.8)

        self.play(Restore(self.camera.frame), run_time=1.5)
        self.wait(1)
