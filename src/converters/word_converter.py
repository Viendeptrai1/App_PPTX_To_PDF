import pythoncom
import win32com.client

def convert_word_to_pdf(file_path, output_path):
    """
    Chuyển đổi file Word sang PDF sử dụng Microsoft Word
    """
    pythoncom.CoInitialize()
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(file_path)
        doc.SaveAs(output_path, FileFormat=17)  # 17 là PDF format
        doc.Close()
        word.Quit()
        return True
    except Exception as e:
        print(f"Lỗi khi chuyển đổi file Word: {str(e)}")
        return False
    finally:
        pythoncom.CoUninitialize() 