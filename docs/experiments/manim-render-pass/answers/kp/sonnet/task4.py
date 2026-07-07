from manim import *


class SurfacePlotScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 1, 0.5],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
        )
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[(BLUE, -1), (GREEN, 0), (RED, 1)],
            axis=2,
        )
        surface.set_style(fill_opacity=0.85)

        title = Text("z = sin(x) · cos(y)", font_size=36)
        title.to_corner(UL)

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, surface)
        self.add_fixed_in_frame_mobjects(title)

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(6)
        self.stop_ambient_camera_rotation()
        self.wait(1)
