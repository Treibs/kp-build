Write a Manim CE (v0.20.1) scene. A 4-frame pixel-art walk cycle is in the working directory
as `sprite_0.png` … `sprite_3.png` (16×16 each). The character starts at the left edge,
2 units tall, crisp pixels. It walks to the right edge over 3 seconds with its walk frames
cycling every 0.2 seconds while it moves. When it arrives it STOPS: the frame cycling ends
and the character rests on `sprite_1.png` (the standing pose), holding for a second — no
residual animation may keep running after the stop.
