from manim import *

class HighlightCodeLines(Scene):
    def construct(self):
        # Code with syntax highlighting
        code = Code(
            code="def greet(name):\n    message = f'Hello, {name}!'\n    print(message)",
            language="python",
            font_size=24,
            background="window"
        )
        
        self.add(code)
        self.wait(0.5)
        
        # Highlight first line (function definition)
        highlight1 = SurroundingRectangle(
            code.code[0], 
            buff=0.1, 
            color=YELLOW, 
            stroke_width=3
        )
        self.play(Create(highlight1))
        self.wait(1)
        
        # Transition to highlighting second line
        highlight2 = SurroundingRectangle(
            code.code[1], 
            buff=0.1, 
            color=CYAN, 
            stroke_width=3
        )
        self.play(Transform(highlight1, highlight2))
        self.wait(1)
        
        self.play(FadeOut(highlight1))
