import os
import sys
import subprocess

def sanitize_filename(filename):
    """
    Loại bỏ các ký tự không hợp lệ trong tên file, giữ nguyên Unicode
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip('_')

def open_file_location(path):
    """
    Mở thư mục chứa file trong File Explorer
    """
    if sys.platform == 'win32':
        os.startfile(os.path.dirname(path))
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, os.path.dirname(path)])

def ensure_directory_exists(directory_path):
    """
    Đảm bảo thư mục tồn tại, tạo mới nếu chưa có
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def check_write_permission(file_path):
    """
    Kiểm tra quyền ghi file
    """
    try:
        with open(file_path, 'a') as f:
            pass
        os.remove(file_path)
        return True
    except Exception:
        return False 