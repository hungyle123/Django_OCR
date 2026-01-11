from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document, Invoices, InvoiceItem
# import pytesseract
# from PIL import Image
# from django.conf import settings
import os
# import pprint
from dotenv import load_dotenv
# from google import genai
# from google.genai import types
from groq import Groq
from django.db.models import Sum
import json
# import re
from gradio_client import Client as GradioClient, handle_file # Đổi tên để tránh nhầm với Groq

load_dotenv()
# client = genai.Client()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# pytesseract.pytesseract.tesseract_cmd = r'D:\TesseractOCR\tesseract.exe'

# from paddleocr import PaddleOCR

# ocr_model = PaddleOCR(use_angle_cls=True, lang='vi')

ocr_client = GradioClient("hungnguyen04/invoice-ocr")

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.status = 'processing'
            doc.save()

            try:
                img_path = doc.image.path
                # img = Image.open(img_path)
                # lát nx test = Vie
                # text_result = pytesseract.image_to_string(img, lang='vie+eng')
                # result = ocr_model.ocr(img_path)

                # raw_text_lines = []
                # if result and result[0]:
                #     for i,text in enumerate(result[0]['rec_texts']):
                #         raw_text_lines.append(text)
                #         # print(i)
                #         # print(text)
                
                # text_result = "\n".join(raw_text_lines)

                print("1. Đang gửi sang Hugging Face...")
                ocr_result = ocr_client.predict(
                    img=handle_file(img_path), 
                    api_name="/inference"
                )
                
                text_result = str(ocr_result)
                print("--- OCR Text Result: ---")

                print(text_result)

                system_prompt = """
                    You are an AI assistant specialized in processing Vietnamese invoice data.
                    Task: Extract information from the provided OCR text and return accurate JSON.

                    Requirements:
                    1. Output ONLY the JSON object. Do not include any conversational text, markdown formatting (like ```json), or explanations.
                    2. If a field has no information, set the value to null.
                    3. Strictly adhere to the sample JSON structure provided below.
                """

                prompt = f"""
                Extract the following OCR text to the structure JSON.
                
                OCR Text:
                \"\"\"
                {text_result}
                \"\"\"

                Structure JSON(only JSON, no markdown):
                {{
                    "invoice_no": "Number of the receipt (string or null)",
                    "seller": "Name of the seller or store (string or null)",
                    "date": "YYYY-MM-DD (string or null)",
                    "items": [
                        {{
                            "product_name": Name product (string, please change to correct Vietnamese word if the text recongized as Vietnamese),
                            "quantity": Quantity (number, default 1),
                            "unit_price": Unit price (number, default VND, if the unit price is USD or any concurrency find the exchange into VND),
                            "total_price": Total price (number)
                        }}
                    ]
                }}
                """

                # response = client.models.generate_content(
                #     model='models/gemini-2.5-flash', 
                #     contents=prompt,
                #     config=types.GenerateContentConfig(
                #         response_mime_type='application/json' 
                #     )
                # )

                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="qwen/qwen3-32b",
                    response_format={"type": "json_object"}, 
                    temperature=0, 
                )

                print(response)

                #clean_json_str = response.text.replace('```json', '').replace('```', '').strip()
                clean_json_str = response.choices[0].message.content.replace('```json', '').replace('```', '').strip()
                data = json.loads(clean_json_str)

                print("--- Gemini JSON Result: ---")
                print(data)

                invoice = Invoices.objects.create(
                    document=doc,
                    raw_text=text_result, 
                    invoice_no=data.get('invoice_no'),
                    seller=data.get('seller'),
                    date=data.get('date') if data.get('date') else None
                )

                items_list = data.get('items', [])
                for item in items_list:
                    InvoiceItem.objects.create(
                        invoice=invoice, 
                        product_name=item.get('product_name', 'Unknown product'),
                        quantity=item.get('quantity', 1),
                        unit_price=item.get('unit_price', 0),
                        total_price=item.get('total_price', 0)
                    )
                doc.status = 'completed'
                doc.save()

                print("--- OCR THÀNH CÔNG ---")
                print(text_result) 
            except Exception as e:
                print(f"--- LỖI OCR: {e} ---")
                doc.status = 'failed'
                doc.save()

            return redirect('upload_file')
    else:
        form = DocumentForm()

    return render(request, 'core/upload.html', {'form': form})


@login_required
def report_dashboard(request):

    items = InvoiceItem.objects.filter(
        invoice__document__user=request.user
    ).select_related('invoice').order_by('-invoice__date', '-id')

    total_spent = items.aggregate(Sum('total_price'))['total_price__sum']

    if total_spent is None:
        total_spent = 0

    total_items_count = items.count() 
    total_invoices_count = Invoices.objects.filter(document__user=request.user).count() 

    context = {
        'items': items,
        'total_spent': total_spent,
        'total_items_count': total_items_count,
        'total_invoices_count': total_invoices_count,
    }
    
    return render(request, 'core/report_dashboard.html', context)

@login_required
def list_files(request):
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    return render(request, 'core/list_files.html', {'documents': documents})

def home(request):
    return render(request, 'core/home.html')


from .forms import SignUpForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})