from manim import *


class AlgorithmComparisonTable(Scene):
    def construct(self):
        title = Text("Algorithm Comparison", font_size=40)
        title.to_edge(UP, buff=0.4)

        table = Table(
            [
                ["O(n log n)", "O(n²)"],
                ["O(1)",       "O(n)"],
                ["Complex",    "Simple"],
            ],
            row_labels=[
                Text("Time Complexity",  font_size=22),
                Text("Space Complexity", font_size=22),
                Text("Simplicity",       font_size=22),
            ],
            col_labels=[
                Text("Merge Sort",     font_size=26),
                Text("Insertion Sort", font_size=26),
            ],
            include_outer_lines=True,
        )
        table.scale(0.65)
        table.next_to(title, DOWN, buff=0.5)
        # Keep table lines and text rendered above the highlight rectangles.
        table.set_z_index(1)

        self.play(Write(title))
        self.play(Create(table))
        self.wait(0.5)

        # Positions are 1-indexed: row 1 = column-header row, col 1 = row-label col.
        # Data cells start at (2, 2).
        # Merge Sort wins Time; Insertion Sort wins Space and Simplicity.
        winners = [
            (2, 2),  # Time Complexity   → Merge Sort
            (3, 3),  # Space Complexity  → Insertion Sort
            (4, 3),  # Simplicity        → Insertion Sort
        ]

        for pos in winners:
            hl = table.get_highlighted_cell(pos, color=GREEN)
            hl.set_z_index(0)
            self.play(FadeIn(hl, run_time=0.5))
            self.wait(0.8)

        self.wait(1.5)
