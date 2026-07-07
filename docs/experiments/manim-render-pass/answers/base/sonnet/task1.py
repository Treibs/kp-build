from manim import *


class CodeLineHighlight(Scene):
    def construct(self):
        code_str = """\
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)"""

        code = Code(
            code=code_str,
            language="python",
            background="window",
            font_size=28,
            insert_line_no=False,
        )
        code.move_to(ORIGIN)

        self.play(FadeIn(code))
        self.wait(0.5)

        # --- Highlight 1: base-case check (line index 1) ---
        hl1 = SurroundingRectangle(
            code.code[1],
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.20,
            buff=0.06,
            corner_radius=0.04,
        )
        label1 = (
            Text("base case", font_size=22, color=YELLOW)
            .next_to(hl1, RIGHT, buff=0.15)
        )
        self.play(Create(hl1), FadeIn(label1))
        self.wait(1.2)

        # --- Highlight 2: recursive call (line index 3) ---
        hl2 = SurroundingRectangle(
            code.code[3],
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.20,
            buff=0.06,
            corner_radius=0.04,
        )
        label2 = (
            Text("recursive call", font_size=22, color=GREEN)
            .next_to(hl2, RIGHT, buff=0.15)
        )
        self.play(
            ReplacementTransform(hl1, hl2),
            FadeOut(label1),
            FadeIn(label2),
        )
        self.wait(1.2)

        self.play(FadeOut(VGroup(hl2, label2, code)))
        self.wait(0.3)
