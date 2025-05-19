import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def meme_generator(image_base64,n_meme:int=4):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a meme line generator. Your task is to create relatable and funny lines for the given meme templates.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a funny and relatable meme using this template. Each text box should feel like a real-life situation, dialogue, or inner thought. Match the tone of Gen Z humor — sarcastic, exaggerated, and meme-friendly. If there are multiple boxes, treat them like parts of a conversation or situation. The final line must deliver the punchline, preferably continuing or twisting the setup in a hilarious or unexpected way. Make sure each meme has the same number of lines as rectangles in the template, not more not less. Dont include the lines or text in the json that is already written on the image. Create {n_meme} memes. Your format must be in json format, and no preamble.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64,
                        },
                    }
                ],
            }
        ],
        temperature=0.7,
        top_p=1,
        model=model
    )

    # print(response.choices[0].message.content)
    return response.choices[0].message.content

import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

if __name__ == "__main__":
    # Example usage
    image_base64 = encode_image(r"C:\AI EVO (Journey)\Ai Agents\AI Meme generator\backend\server\data\eaf1a0d1-407c-4bdd-8fa8-86657c357d33_annotated.png")
    meme_texts = meme_generator(image_base64)
    obj = json.loads(meme_texts)
    print(obj)