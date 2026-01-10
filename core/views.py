from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document, Invoices
import pytesseract
from PIL import Image
from django.conf import settings
import os
import pprint

pytesseract.pytesseract.tesseract_cmd = r'D:\TesseractOCR\tesseract.exe'

from paddleocr import PaddleOCR

ocr_model = PaddleOCR(use_angle_cls=True, lang='vi')

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
                result = ocr_model.ocr(img_path)

                raw_text_lines = []

                # ['input_path', 'page_index', 'doc_preprocessor_res', 'dt_polys', 'model_settings', 'text_det_params', 'text_type', 'text_rec_score_thresh', 'return_word_box', 'rec_texts', 'rec_scores', 'rec_polys', 'vis_fonts', 'textline_orientation_angles', 'rec_boxes']
                # print("\n" + "="*50)
                # print("--- CẤU TRÚC DỮ LIỆU PADDLE TRẢ VỀ ---")
                # pprint.pprint(result)  # In đẹp (Pretty Print)
                # print("="*50 + "\n")
                if result and result[0]:
                    for i,text in enumerate(result[0]['rec_texts']):
                        raw_text_lines.append(text)
                        # print(i)
                        # print(text)
                
                text_result = " ".join(raw_text_lines)

                Invoices.objects.create(
                    document=doc,
                    raw_text=text_result
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