import os
from PIL import Image

dir_raw = r"D:\souravshuvo.github.io\game_store_assets\Bike-Traffic-Racer\raw_captures"
for f in sorted(os.listdir(dir_raw)):
    if f.endswith(".png"):
        p = os.path.join(dir_raw, f)
        with Image.open(p) as im:
            print(f"{f:30} : size={im.size}, mode={im.mode}")