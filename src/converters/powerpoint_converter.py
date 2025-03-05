import os
from pathlib import Path
import win32com.client
import pythoncom
import atexit

# Biến global để lưu instance của PowerPoint
powerpoint_app = None

def initialize_powerpoint():
    """
    Khởi tạo PowerPoint application
    """
    global powerpoint_app
    if powerpoint_app is None:
        pythoncom.CoInitialize()
        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
    return powerpoint_app

def cleanup_powerpoint():
    """
    Dọn dẹp PowerPoint khi tắt ứng dụng
    """
    global powerpoint_app
    if powerpoint_app:
        try:
            powerpoint_app.Quit()
            pythoncom.CoUninitialize()
            powerpoint_app = None
        except:
            pass

# Đăng ký hàm cleanup để chạy khi tắt ứng dụng
atexit.register(cleanup_powerpoint)

def convert_pptx_to_pdf(file_path, output_path):
    """
    Chuyển đổi PowerPoint sang PDF sử dụng Microsoft PowerPoint
    """
    try:
        print("Đang xử lý file PowerPoint...")
        # Lấy hoặc khởi tạo PowerPoint instance
        powerpoint = initialize_powerpoint()
        
        # Chuyển đổi đường dẫn sang định dạng Windows
        abs_path = str(Path(file_path).resolve())
        output_path_win = str(Path(output_path).resolve())
        
        # Mở file và chuyển đổi
        deck = powerpoint.Presentations.Open(abs_path, WithWindow=False)
        print("Đang chuyển đổi sang PDF...")
        deck.SaveAs(output_path_win, 32)  # 32 = ppSaveAsPDF
        
        # Chỉ đóng presentation, không đóng PowerPoint
        deck.Close()
        
        print("Đã hoàn thành chuyển đổi!")
        return os.path.exists(output_path)
        
    except Exception as e:
        print(f"Lỗi khi chuyển đổi: {str(e)}")
        try:
            deck.Close()
        except:
            pass
        return False 