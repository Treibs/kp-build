from manim import *


class AlgorithmComparisonScene(Scene):
    def construct(self):
        title = Text("Algorithm Comparison", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        table = Table(
            [
                ["O(n log n)", "O(n²)"],
                ["O(n)",       "O(1)"],
                ["95%",        "87%"],
            ],
            row_labels=[Text("Speed"), Text("Memory"), Text("Accuracy")],
            col_labels=[Text("Algorithm A"), Text("Algorithm B")],
            include_outer_lines=True,
        )
        table.scale(0.65)
        table.next_to(title, DOWN, buff=0.45)
        self.play(Create(table))
        self.wait(0.5)

        # Indices are 1-based; row 1 = col-header row, col 1 = row-label column.
        # Speed   row=2: col 2 (Alg A) wins   O(n log n) < O(n²)
        # Memory  row=3: col 3 (Alg B) wins   O(1)       < O(n)
        # Accuracy row=4: col 2 (Alg A) wins  95%        > 87%
        winners = [
            (2, 2, "Speed    → Algorithm A wins"),
            (3, 3, "Memory   → Algorithm B wins"),
            (4, 2, "Accuracy → Algorithm A wins"),
        ]

        for row, col, caption in winners:
            cell = table.get_cell((row, col))
            highlight = SurroundingRectangle(cell, color=YELLOW, buff=0, stroke_width=3)
            note = Text(caption, font_size=30, color=YELLOW)
            note.next_to(table, DOWN, buff=0.35)

            self.play(Create(highlight), Write(note))
            self.wait(1.5)
            self.play(FadeOut(note))
            # highlight remains so the winning cell stays marked

        self.wait(1)
