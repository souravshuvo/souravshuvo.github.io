import os
from PIL import Image

p1 = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game\play-store\app-icon.png"
p2 = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game\play-store\feature-graphic.jpg"

with Image.open(p1) as im1:
    print(f"app-icon: size={im1.size}, format={im1.format}")
with Image.open(p2) as im2:
    print(f"feature-graphic: size={im2.size}, format={im2.format}")