import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(),"backend"))
from components.memegenerator import meme_generator
from components.jsonconverter import convert_to_json
from utils.encode_image import encode_image
from utils.place_text import put_text_in_rectangle

def get_meme(rectangled_image_path, original_image_path, rectangle_data):

    with open(rectangled_image_path, "rb") as f:
        rectangled_image = f.read()
    
    with open(original_image_path, "rb") as f:
        original_image = f.read()

    meme_texts = meme_generator(encode_image(rectangled_image))

    meme_json = convert_to_json(meme_texts, encode_image(rectangled_image))
    meme_json = json.loads(meme_json)
    
