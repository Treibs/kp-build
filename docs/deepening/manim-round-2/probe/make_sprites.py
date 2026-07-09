#!/usr/bin/env python3
"""Deterministic sprite-sheet generator for the manim round-2 probe (arm-neutral scaffold).

Generates a 16x16 pixel person in 4 walk frames (sprite_0..3.png) plus sprite.png
(a copy of frame 0). No randomness, no timestamps — byte-identical on every run
(PNGs are written with fixed settings; Pillow writes no time metadata for RGBA PNGs).
Committed next to the PNGs so the assets are reproducible from a clean clone.
"""
from PIL import Image

PALETTE = {
    ".": (0, 0, 0, 0),          # transparent
    "K": (24, 24, 24, 255),     # outline / hair / boots
    "S": (240, 195, 150, 255),  # skin
    "W": (250, 250, 250, 255),  # eye white
    "R": (200, 40, 40, 255),    # shirt
    "B": (40, 70, 180, 255),    # pants
}

TORSO = [
    "................",
    ".....KKKKKK.....",
    "....KSSSSSSK....",
    "....KSWSSWSK....",
    "....KSSSSSSK....",
    ".....KSSSSK.....",
    "....RRRRRRRR....",
    "...SRRRRRRRRS...",
    "...SRRRRRRRRS...",
    "....RRRRRRRR....",
    "....BBBBBBBB....",
]

LEGS_STEP = [
    "....BBB..BBB....",
    "....BBB...BBB...",
    "....BB.....BB...",
    "....KK.....KK...",
    "................",
]

LEGS_TOGETHER = [
    "....BBB..BBB....",
    "....BBB..BBB....",
    "....BBB..BBB....",
    "....KKK..KKK....",
    "................",
]

def frame(rows):
    img = Image.new("RGBA", (16, 16))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            img.putpixel((x, y), PALETTE[ch])
    return img

def mirror_rows(rows):
    return [row[::-1] for row in rows]

frames = [
    TORSO + LEGS_STEP,
    TORSO + LEGS_TOGETHER,
    TORSO + mirror_rows(LEGS_STEP),
    TORSO + LEGS_TOGETHER,
]

if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).parent
    for i, rows in enumerate(frames):
        assert len(rows) == 16 and all(len(r) == 16 for r in rows)
        frame(rows).save(here / f"sprite_{i}.png")
    frame(frames[0]).save(here / "sprite.png")
    print("wrote sprite.png + sprite_0..3.png")
