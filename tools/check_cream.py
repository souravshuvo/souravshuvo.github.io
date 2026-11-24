import os
from PIL import Image

dir_raw = r"D:\souravshuvo.github.io\game_store_assets\Swirl-Studio-Ice-Cream\raw_captures"
for f in sorted(os.listdir(dir_raw)):
    if f.endswith(".png"):
        p = os.path.join(dir_raw, f)
        with Image.open(p) as im:
            print(f"{f:32} : size={im.size}, mode={im.mode}")

ic = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game\store\icon-512.png"
ft = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game\store\feature-1024x500.png"
with Image.open(ic) as im:
    print(f"store icon-512: size={im.size}, format={im.format}")
with Image.open(ft) as im:
    print(f"store feature-1024x500: size={im.size}, format={im.format}")