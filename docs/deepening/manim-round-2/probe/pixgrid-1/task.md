Write a Manim CE (v0.20.1) scene, no image files. Build a pixel-art character entirely from
code: an 8×8 grid of small squares (side 0.4, no gaps, no visible borders between them)
forming a simple person — you choose the pixel map (head, shirt, legs in three colors;
unused cells absent, not black). Behind it, a floor of checkerboard tiles (two alternating
greens, squares of side 0.8) covers the bottom third of the frame. The character stands on
the floor and must render entirely IN FRONT of the tiles. Assemble the character pixel by
pixel with a staggered pop-in, then have it slide 3 units right as one unit — no pixel may
lag behind.
