from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

image_path = r'D:\Folder_code_project\test_django\AnyConv.com__ban-canh-chua-tom-tinh-rieng-tien-tom-880000-dongkg_20150805104451634.png'

response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=[
        'Đọc nội dung trong hình này',
        Image.open(image_path)
    ]
)
print(response.text)