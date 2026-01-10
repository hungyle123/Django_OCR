from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

image_path = 'hoadon_test.jpg'

response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=[
        'Tell me a story based on this image',
        Image.open(image_path)
    ]
)
print(response.text)