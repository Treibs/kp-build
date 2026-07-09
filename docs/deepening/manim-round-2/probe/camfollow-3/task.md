Write a Manim CE (v0.20.1) scene. A pixel-art character sprite is in the working directory as
`sprite.png` (16×16). A tall ladder (a thin vertical line with rungs) reaches from a ground
line at the bottom up to 3 screen-heights above it. The character, 1.2 units tall with crisp
pixels, climbs from the ground to the top over 6 seconds. The camera follows the climb
vertically, keeping the character vertically centered — EXCEPT at the start: the camera must
never show anything below the ground line, so it only starts moving once the character has
climbed high enough for a centered frame to keep the ground out of view.
