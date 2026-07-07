from manim import *

class HighlightedCodeDisplay(Scene):
    def construct(self):
        # Python function to display with syntax highlighting
        python_code = '''def add(a, b):
    return a + b'''
        
        # Create syntax-highlighted code block
        code = Code(
            code_string=python_code,
            language="python",
            font_size=28,
            background="window"
        )
        
        self.add(code)
        self.wait(0.5)
        
        # Rectangle to highlight the first line (function definition)
        highlight_1 = Rectangle(
            width=5,
            height=0.5,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color=YELLOW,
            fill_opacity=0.2
        ).move_to(code).shift(UP * 0.35)
        
        # Rectangle to highlight the second line (return statement)
        highlight_2 = Rectangle(
            width=5,
            height=0.5,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_color=BLUE,
            fill_opacity=0.2
        ).move_to(code).shift(DOWN * 0.35)
        
        # Animate first highlight
        self.play(Create(highlight_1))
        self.wait(1)
        self.play(FadeOut(highlight_1))
        
        # Animate second highlight
        self.play(Create(highlight_2))
        self.wait(1)
        self.play(FadeOut(highlight_2))
        
        self.wait()
