import google.generativeai as genai
import os
import time

# ==============================================================================
# CẤU HÌNH (BẠN CẦN SỬA 2 DÒNG NÀY)
# ==============================================================================
# 1. Dán API Key của bạn vào đây (trong dấu nháy kép)
GOOGLE_API_KEY = "AIzaSyA36v6yRKsaAlVymRJOPiD59wreXmkZ8rM"

# 2. Tên file ảnh bạn muốn test (để cùng thư mục với file code này)
IMAGE_PATH = "hoadon_test.jpg"
# ==============================================================================


def test_inference():
    print("--- BẮT ĐẦU TEST GEMINI VISION ---")
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('deep-research-pro-preview-12-2025')
        print("-> Đã kết nối thành công với Google API.")
    except Exception as e:
        print(f"LỖI CẤU HÌNH API: {e}")
        return

    try:
        print(f"-> Đang tải ảnh '{IMAGE_PATH}' lên Google (Waiting)...")
        sample_file = genai.upload_file(path=IMAGE_PATH, display_name="Test Image")
        print(f"-> Upload xong. File URI: {sample_file.uri}")
        time.sleep(2) 
        
    except Exception as e:
        print(f"LỖI UPLOAD ẢNH: {e}")
        return

    prompt = """
    Bạn là một chuyên gia kế toán AI. Hãy nhìn vào hình ảnh hóa đơn này và thực hiện các nhiệm vụ sau:

    1. Xác định đây có phải là hóa đơn hợp lệ không.
    2. Trích xuất các thông tin quan trọng sau đây và trình bày dưới dạng JSON thuần túy (không dùng markdown ```json):
       - seller_name: Tên nơi bán hàng (cửa hàng, công ty)
       - total_amount: Tổng số tiền thanh toán cuối cùng (chỉ lấy số, ví dụ: 150000)
       - date: Ngày mua hàng (định dạng chuẩn YYYY-MM-DD nếu tìm thấy, ví dụ: 2023-10-25)
       - invoice_no: Số hóa đơn hoặc mã giao dịch (nếu có)
       - items_summary: Tóm tắt ngắn gọn mua những gì (ví dụ: "3 món ăn", "Xăng A95")

    Nếu thông tin nào không tìm thấy trong ảnh, hãy để giá trị là null trong JSON.
    """
    try:
        print("\n-> Đang yêu cầu AI phân tích hình ảnh... (Vui lòng đợi vài giây)")
        start_time = time.time()
        response = model.generate_content([sample_file, prompt])
        end_time = time.time()
        print(f"-> Hoàn thành trong: {round(end_time - start_time, 2)} giây.")

        print("\n" + "="*30 + " KẾT QUẢ GEMINI TRẢ VỀ " + "="*30)
        print(response.text)
        print("="*80 + "\n")
        print("--- TEST THÀNH CÔNG ---")
    except Exception as e:
        print(f"\nLỖI KHI GỌI API: {e}")
        print("Gợi ý: Kiểm tra lại API Key, kết nối mạng, hoặc ảnh có quá nặng không.")

# Chạy hàm test
if __name__ == "__main__":
    test_inference()