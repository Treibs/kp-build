Write a Manim CE (v0.20.1) scene. A pixel-art character sprite is in the working directory as
`sprite.png` (16×16). The character, 1 unit tall with crisp pixels, stands at the left among
a scattering of six small gray rocks (circles) spread across the full frame. First the camera
smoothly zooms in on the character (frame about a third of the default width). Then, while
the camera stays zoomed, the character runs a smooth S-curve through the rocks to the right
edge and the camera tracks it continuously, keeping it centered. Finally the camera zooms
back out to the full original frame.
