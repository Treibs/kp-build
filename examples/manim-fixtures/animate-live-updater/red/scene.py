from manim import *


class AnimateLiveCounter(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        counter = DecimalNumber(0, num_decimal_places=0)
        counter.add_updater(lambda m: m.set_value(tracker.get_value()))
        self.add(counter)
        # Animating the carrier of a live structure-changing updater crashes
        # mid-interpolation (manim's own ValueError) — and on 0.20.1 the crash
        # also strands the file writer's non-daemon thread, hanging the process
        # forever post-traceback. The except block releases that thread with the
        # writer's own sentinel so the failure EXITS instead of hanging; the
        # weakness itself still fires unmodified inside manim.
        try:
            self.play(counter.animate.shift(RIGHT * 2),
                      tracker.animate.set_value(100), run_time=0.5)
        except Exception:
            self.renderer.file_writer.queue.put((-1, None))
            raise
