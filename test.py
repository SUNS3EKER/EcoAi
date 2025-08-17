from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

load_dotenv()

# Your Prompt
prompt = "What do you see on this image?"

# Image file path
image_path = r"C:\Users\kalel\Desktop\EcoAi\captura.png"

# Initialize Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
# Encode the image
base64_image = encode_image(image_path)

# Create chat completion
try:
    chat_completion = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"An error occured: {e}")