#!/usr/bin/env python3
"""Deterministic sprite sheet for round 3: the four committed round-2 frames side by
side (64x16). Byte-identical on every run."""
import pathlib
from PIL import Image
r2 = pathlib.Path(__file__).resolve().parents[2] / "manim-round-2/probe"
frames = [Image.open(r2 / f"sprite_{i}.png") for i in range(4)]
sheet = Image.new("RGBA", (64, 16))
for i, f in enumerate(frames):
    sheet.paste(f, (i * 16, 0))
sheet.save(pathlib.Path(__file__).parent / "sprite_sheet.png")
print("wrote sprite_sheet.png")
