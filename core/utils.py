# core/utils.py
import re
from datetime import datetime

def clean_currency(money_str):
    if not money_str:
        return None
    clean_str = re.sub(r'[^\d.,]', '', money_str)
    clean_str = re.sub(r'[.,]', '', clean_str)
    try:
        return float(clean_str)
    except ValueError:
        return None

def extract_invoice_data(text):
    data = {
        'invoice_no': None,
        'date': None,
        'total_amount': None
    }

    # 1. TÌM NGÀY THÁNG
    # Regex tìm dạng dd/mm/yyyy hoặc dd-mm-yyyy
    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text)
    if date_match:
        date_str = date_match.group(1)
        # Chuyển đổi string sang object date của Python để lưu vào DB
        try:
            # Thử format dd/mm/yyyy
            data['date'] = datetime.strptime(date_str.replace('-', '/'), '%d/%m/%Y').date()
        except:
            pass # Nếu lỗi format thì bỏ qua

    # 2. TÌM TỔNG TIỀN
    # Tìm các dòng có chữ Tổng, Total, Payment...
    lines = text.split('\n') # Cần text có xuống dòng mới chuẩn
    for line in lines:
        lower_line = line.lower()
        if any(x in lower_line for x in ['tổng', 'total', 'thành tiền', 'phải thu']):
            # Tìm chuỗi số trong dòng đó
            numbers = re.findall(r'[\d.,]+', line)
            if numbers:
                # Lấy số cuối cùng tìm thấy (thường là tổng tiền) và độ dài > 3
                valid_numbers = [n for n in numbers if len(n) > 3]
                if valid_numbers:
                    data['total_amount'] = clean_currency(valid_numbers[-1])
                    break # Tìm thấy rồi thì thôi
    
    # 3. TÌM SỐ HÓA ĐƠN (Thường sau chữ Số, No., Invoice...)
    invoice_no_match = re.search(r'(?:Số|No|Invoice)\.?\s*[:#]?\s*([A-Za-z0-9-]+)', text, re.IGNORECASE)
    if invoice_no_match:
        data['invoice_no'] = invoice_no_match.group(1)

    return data