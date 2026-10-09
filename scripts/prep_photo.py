from rembg import remove
from PIL import Image, ImageFilter
import cv2
import numpy as np
import sys

def prep_photo(input_path, output_path="source-prepped.png"):
    # Step 1: Remove background
    with open(input_path, "rb") as f:
        img_bytes = remove(f.read())
    
    img = Image.open(__import__("io").BytesIO(img_bytes)).convert("RGBA")
    
    # Step 2: White background composite
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    background.paste(img, mask=img.split()[3])
    img_rgb = background.convert("RGB")
    
    # Step 3: CLAHE contrast boost
    img_cv = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_cv)
    
    Image.fromarray(img_clahe).save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    prep_photo(sys.argv[1])
