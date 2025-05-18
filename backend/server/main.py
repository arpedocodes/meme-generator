import sys
import os
import json
import cv2
from colorama import Fore, Style, init

init(autoreset=True)  # Auto-reset colors after each print

sys.path.append(os.path.join(os.getcwd(), "backend"))
print(f"{Fore.GREEN}Backend path added to sys.path")

from components.memegenerator import meme_generator
print(f"{Fore.GREEN}meme_generator imported successfully")

from utils.encode_image import encode_image
print(f"{Fore.GREEN}encode_image imported successfully")

from utils.place_text import put_text_in_rectangle
print(f"{Fore.GREEN}put_text_in_rectangle imported successfully")

def get_meme(rectangled_image_path, original_image_path):
    print(f"{Fore.CYAN}Starting meme generation process...")

    encoding = encode_image(rectangled_image_path)
    print(f"{Fore.GREEN}Image encoded successfully")

    meme_texts = meme_generator(encoding)
    print(f"{Fore.GREEN}Meme text generated successfully")

    meme_json = json.loads(meme_texts)
    print(f"{Fore.GREEN}Meme text parsed to JSON successfully")

    meme_lines = [list(line.values()) for line in meme_json]
    print(f"{Fore.YELLOW}Meme lines extracted: {meme_lines}")

    org_img_array = cv2.imread(original_image_path)
    print(f"{Fore.GREEN}Original image loaded")

    rectangle_data_path = os.path.join(os.getcwd(), "backend", "server", "data", "rectangleData.json")
    print(f"{Fore.CYAN}Loading rectangle data from: {rectangle_data_path}")

    with open(rectangle_data_path) as f:
        data = json.load(f)
    print(f"{Fore.GREEN}Rectangle data loaded: {data}")

    for idx, lines in enumerate(meme_lines):
        print(f"\n{Fore.MAGENTA}Processing meme image {idx}")
        org_img_array_copy = org_img_array.copy()
        print(f"{Fore.GREEN}Created a copy of the original image")

        for text, coords in zip(lines, data):
            print(f"{Fore.YELLOW}Placing text '{text}' in rectangle: {coords}")
            top_left = tuple(int(v) for v in coords['leftTop'].values())
            bottom_right = tuple(int(v) for v in coords['rightBottom'].values())
            print(f"{Fore.YELLOW}Top left: {top_left}, Bottom right: {bottom_right}")
            put_text_in_rectangle(org_img_array_copy, text, top_left, bottom_right)
            print(f"{Fore.GREEN}Text placed successfully")

        output_path = os.path.join(os.getcwd(), "backend", "server", "output", f"meme{idx}.png")
        print(f"{Fore.CYAN}Saving meme image to: {output_path}")
        cv2.imwrite(output_path, org_img_array_copy)
        print(f"{Fore.GREEN}Meme image saved successfully")

    print(f"{Fore.CYAN}\nAll meme images generated successfully")
    return meme_lines

if __name__ == "__main__":
    rectangled_image_path = r"C:\AI EVO (Journey)\Ai Agents\meme-generator\backend\server\data\eaf1a0d1-407c-4bdd-8fa8-86657c357d33_annotated.png"
    print(f"{Fore.CYAN}Using rectangled image: {rectangled_image_path}")

    original_image_path = r"C:\AI EVO (Journey)\Ai Agents\meme-generator\backend\server\data\eaf1a0d1-407c-4bdd-8fa8-86657c357d33_original.png"
    print(f"{Fore.CYAN}Using original image: {original_image_path}")

    meme_lines = get_meme(rectangled_image_path, original_image_path)
    print(f"\n{Fore.LIGHTGREEN_EX}Final meme lines returned:")
    print(meme_lines)
