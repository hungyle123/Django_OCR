<div align="center">

# Intelligent Invoice OCR Web Application

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
<br/>
[![PaddleOCR](https://img.shields.io/badge/AI-PaddleOCR-blue?style=for-the-badge)](https://github.com/PaddlePaddle/PaddleOCR)
[![Groq API](https://img.shields.io/badge/LLM-Groq%20(Qwen--32B)-orange?style=for-the-badge)](https://groq.com/)
[![Cloudinary](https://img.shields.io/badge/Cloud-Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com/)

<p align="center">
  <b>Automated invoice digitization system powered by a Hybrid AI Pipeline.</b><br/>
  <i>Transform paper receipts into structured financial data in a matter of seconds.</i>
</p>
</div>

---

## Introduction

**Intelligent Invoice OCR** is a Web Application designed to streamline manual processing receipt image for accounting and personal expense management.

Instead of manually typing numbers from crumpled or faded receipts, this system allows users to upload invoice images and automatically extracts critical information, including: **Purchase Date**, **Seller Name**, and **Total Amount**.

The project leverages a hybrid approach:
* **PaddleOCR**: For high-accuracy optical character recognition (text detection) ***We will deploy the PaddleOCR into hugggingface and call API from it***.
* **Groq API (Qwen-32B)**: LLM to extract information from OCR to structure JSON.

## Features

- Upload image of receipt to the web app.
- All image will then store in **Cloudinary** (still implementing)
- **PaddleOCR** to extract the text from low-quality or angled invoice images
- Use **Groq API (Qwen-32B)** to intelligently parse raw text and identify key entities: *Transaction Date*, *Seller Name*, and *Total Amount*
- Visualizes financial data through dynamic charts

```mermaid
graph TD
    A[👤 User] -->|Upload Invoice Image| B(Django Backend)
    B -->|1. Store Media| C{Cloudinary}
    C -->|2. Return Image URL| B
    B -->|3. Send URL for OCR| D[Hugging Face Spaces<br/>(PaddleOCR)]
    D -->|4. Return Raw Text| B
    B -->|5. Prompt + Raw Text| E[Groq API<br/>(LLM: Qwen-32B)]
    E -->|6. Return Structured JSON| B
    B -->|7. Save Data| F[(PostgreSQL DB)]
    F -->|8. Update View| G[Dashboard UI]
```