from manim import *

class CounterBarsScene(Scene):
    def construct(self):
        trackers = [ValueTracker(0) for _ in range(3)]
        targets = [50, 75, 100]
        colors = [RED, GREEN, BLUE]
        
        for i, (tracker, target, color) in enumerate(zip(trackers, targets, colors)):
            x_pos = i * 3 - 3
            
            # Live counter display
            number = always_redraw(
                lambda t=tracker, x=x_pos: DecimalNumber(t.get_value(), num_decimal_places=0)
                    .scale(1.5)
                    .move_to([x, 2, 0])
            )
            self.add(number)
            
            # Proportional bar
            bar = always_redraw(
                lambda t=tracker, x=x_pos, col=color: Rectangle(
                    height=max(0.1, 0.05 * t.get_value()),
                    width=0.8,
                    color=col,
                    fill_opacity=0.8
                )
                    .move_to([x, 0, 0])
            )
            self.add(bar)
        
        # Animate all three trackers simultaneously
        self.play(
            *[t.animate.set_value(target) for t, target in zip(trackers, targets)],
            run_time=3
        )
        self.wait(1)
