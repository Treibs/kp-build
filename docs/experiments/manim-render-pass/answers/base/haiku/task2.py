from manim import *

class CountersWithBars(Scene):
    def construct(self):
        targets = [100, 250, 50]
        max_target = max(targets)
        colors = [BLUE, GREEN, RED]
        
        # Create counter+bar groups
        groups = []
        for i, target in enumerate(targets):
            label = Text(f"Counter {i+1}").scale(0.6)
            counter = DecimalNumber(0, num_decimal_places=0).scale(0.8)
            bar_bg = Rectangle(width=3, height=0.3, color=GRAY, fill_opacity=0.3)
            bar = Rectangle(width=0, height=0.3, color=colors[i], fill_opacity=0.8)
            
            group = VGroup(label, counter, bar_bg)
            group.arrange(DOWN, buff=0.2)
            bar.next_to(bar_bg, LEFT, buff=0)
            
            groups.append({
                'group': group,
                'counter': counter,
                'bar': bar,
                'target': target
            })
        
        # Arrange all groups horizontally
        all_groups = VGroup(*[g['group'] for g in groups])
        all_groups.arrange(RIGHT, buff=1.5)
        
        # Add to scene
        for g in groups:
            self.add(g['group'], g['bar'])
        
        # Value tracker synchronizes all animations
        progress = ValueTracker(0)
        
        def make_counter_updater(target):
            return lambda m: m.set_value(progress.get_value() * target)
        
        def make_bar_updater(target):
            def updater(mob):
                width = 3 * progress.get_value() * target / max_target
                mob.set_width(width, about_edge=LEFT)
            return updater
        
        for g in groups:
            g['counter'].add_updater(make_counter_updater(g['target']))
            g['bar'].add_updater(make_bar_updater(g['target']))
        
        self.play(progress.animate.set_value(1), run_time=3)
        self.wait()
