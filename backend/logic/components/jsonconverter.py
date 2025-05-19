import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
key = os.environ["HF_token"]

with open(os.path.join(os.getcwd(), 'backend' ,'config',"prompt.json")) as f:
    prompt = json.load(f)

system_prompt = prompt["system_prompt_json"]

def convert_to_json(raw_text, base_64):
    url = "https://router.huggingface.co/nebius/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36"
    }

    payload = {
        "model": "google/gemma-3-27b-it-fast",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
    },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": raw_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base_64
                        }
                    }
                ]
            }
        ],
        "temperature": 0.5,
        "top_p": 0.7,
        "stream": True
    }

    content = ""

    with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
        for line in response.iter_lines():
            if line:
                try:
                    text = json.loads(line.decode("utf-8").split("data: ")[1]).get("choices")[0].get("delta").get("content")
                    # print(text, end="")
                    content += text
                except:
                    pass

    return content

if __name__ == "__main__":
    text = """
    **Meme 1:**  
    Left: "I only need 6 hours of sleep."  
    Right: "Yeah, but you took 3 naps today."  

    **Meme 2:**  
    Left: "I'm totally overthinking this."  
    Right: "Same, but like, professionally."  

    **Meme 3:**  
    Left: "My life is in shambles."  
    Right: "Nice, mine's in pixels."  

    **Meme 4:**
    Left: "I can totally handle adulthood."
    Right: "Bro, you just Googled 'how to boil water.'"
    """
    import base64

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

    image_base64 = encode_image(r"C:\AI EVO (Journey)\Ai Agents\AI Meme generator\backend\server\data\eaf1a0d1-407c-4bdd-8fa8-86657c357d33_annotated.png")
    meme_json = convert_to_json(text, image_base64)
    print(meme_json)