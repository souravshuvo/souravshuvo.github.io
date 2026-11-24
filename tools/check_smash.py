import os
from PIL import Image

dir_raw = r"D:\souravshuvo.github.io\game_store_assets\Smash-DIY-ASMR\raw_captures"
for f in sorted(os.listdir(dir_raw)):
    if f.endswith(".png"):
        p = os.path.join(dir_raw, f)
        with Image.open(p) as im:
            print(f"{f:30} : size={im.size}, mode={im.mode}")

ic = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game\store-listing\play-icon.png"
ft = r"C:\Users\shuvo\.gemini\antigravity\brain\4cb31ef9-08de-4289-b423-520f07e57b82\scratch\project-game\store-listing\feature-graphic.png"
with Image.open(ic) as im:
    print(f"play-icon: size={im.size}, format={im.format}")
with Image.open(ft) as im:
    print(f"feature-graphic: size={im.size}, format={im.format}")