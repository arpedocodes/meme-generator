import sys
import os
import json
from typing import List
import cv2  
sys.path.append(os.path.join(os.getcwd(), "backend"))
from components.memegenerator import meme_generator
from utils.encode_image import encode_image
from utils.place_text import put_text_in_rectangle

def get_meme(rectangled_image_path:str, original_image_path:str) -> List[str]:

    encoding = encode_image(rectangled_image_path)
    meme_texts = meme_generator(encoding)
    meme_json = json.loads(meme_texts)
    print(meme_json)
    meme_lines = [list(line.values()) for line in meme_json]
    org_img_array = cv2.imread(original_image_path)
    rectangle_data_path = os.path.join(os.getcwd(), "backend", "server", "data", "rectangleData.json")

    output_image_path = []

    with open(rectangle_data_path) as f:
        data = json.load(f)

    for idx, lines in enumerate(meme_lines):
        org_img_array_copy = org_img_array.copy()

        for text, coords in zip(lines, data):
            top_left = tuple(int(v) for v in coords['leftTop'].values())
            bottom_right = tuple(int(v) for v in coords['rightBottom'].values())
            put_text_in_rectangle(org_img_array_copy, str(text).replace("’","\'"), top_left, bottom_right)

        output_path = os.path.join(os.getcwd(), "backend", "server", "output", f"meme{idx}.png")
        output_image_path.append(output_path)
        cv2.imwrite(output_path, org_img_array_copy)

    return output_image_path