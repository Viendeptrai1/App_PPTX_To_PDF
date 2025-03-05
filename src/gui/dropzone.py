import os
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QProgressBar, QMessageBox, QApplication
from PyQt6.QtCore import Qt, QTimer
import traceback

from ..utils.file_utils import sanitize_filename, open_file_location, ensure_directory_exists, check_write_permission
from ..converters.powerpoint_converter import convert_pptx_to_pdf
from ..converters.word_converter import convert_word_to_pdf

class DropZone(QLabel):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_pdf_folder()
        
    def init_ui(self):
        """
        Khởi tạo giao diện người dùng
        """
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText('\nKéo và thả file PowerPoint hoặc Word vào đây\n')
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #FF69B4;
                border-radius: 15px;
                background-color: #FFF0F5;
                padding: 30px;
                font-size: 16px;
                color: #FF1493;
            }
            QLabel:hover {
                background-color: #FFB6C1;
                border: 2px solid #FF69B4;
            }
        ''')
        self.setAcceptDrops(True)
        
        # Tạo progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet('''
            QProgressBar {
                border: 2px solid #FF69B4;
                border-radius: 5px;
                text-align: center;
                background-color: #FFF0F5;
            }
            QProgressBar::chunk {
                background-color: #FF69B4;
            }
        ''')
        self.progress.hide()
        
        # Layout cho widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        self.layout.addWidget(self.progress)
        
        # Container widget
        self.container = QWidget()
        self.container.setLayout(self.layout)

    def setup_pdf_folder(self):
        """
        Thiết lập thư mục lưu file PDF
        """
        self.desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.pdf_folder = os.path.join(self.desktop_path, 'PDF_Converted')
        ensure_directory_exists(self.pdf_folder)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.progress.show()
        self.progress.setValue(0)
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        
        successful_conversions = []
        
        # Xử lý từng file
        total_files = len(files)
        for i, file_path in enumerate(files):
            self.setText(f'Đang xử lý file {i+1}/{total_files}...')
            self.progress.setValue((i * 100) // total_files)
            QApplication.processEvents()  # Cập nhật UI
            
            if self.convert_to_pdf(file_path):
                successful_conversions.append(file_path)
            
        self.progress.setValue(100)
        QTimer.singleShot(2000, self.progress.hide)  # Ẩn progress bar sau 2 giây
        
        # Hiển thị thông báo và mở thư mục nếu có file được chuyển đổi thành công
        if successful_conversions:
            self.show_success_message(len(successful_conversions))

    def convert_to_pdf(self, file_path):
        """
        Chuyển đổi file sang PDF
        """
        try:
            # Chuẩn hóa đường dẫn
            file_path = os.path.abspath(file_path)
            
            # Kiểm tra xem file có tồn tại không
            if not os.path.exists(file_path):
                self.setText(f'Lỗi: Không tìm thấy file {file_path}')
                return False

            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Tạo tên file an toàn (giữ nguyên Unicode)
            safe_filename = sanitize_filename(file_name_without_ext)
            
            # Tạo đường dẫn output trong thư mục PDF_Converted
            output_path = os.path.join(self.pdf_folder, safe_filename + '.pdf')

            # Kiểm tra quyền ghi file
            if not check_write_permission(output_path):
                self.setText(f'Lỗi: Không có quyền ghi file tại {self.pdf_folder}')
                return False

            # Chuyển đổi file dựa vào định dạng
            if file_ext in ['.pptx', '.ppt']:
                self.setText('Đang xử lý...\nVui lòng đợi trong giây lát')
                QApplication.processEvents()  # Cập nhật UI ngay lập tức
                success = convert_pptx_to_pdf(file_path, output_path)
            elif file_ext in ['.docx', '.doc']:
                success = convert_word_to_pdf(file_path, output_path)
            else:
                self.setText('Chỉ hỗ trợ file PowerPoint (.ppt, .pptx) và Word (.doc, .docx)')
                return False

            if success and os.path.exists(output_path):
                self.setText(f'Chuyển đổi thành công!\nFile PDF được lưu tại:\n{output_path}')
                return True
            else:
                self.setText('Lỗi: Không thể tạo file PDF')
                return False

        except Exception as e:
            error_msg = f'Lỗi chi tiết:\n{str(e)}\n{traceback.format_exc()}'
            print(error_msg)  # In ra console để debug
            self.setText(f'Lỗi khi chuyển đổi file: {str(e)}')
            return False

    def show_success_message(self, num_files):
        """
        Hiển thị thông báo thành công
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Hoàn thành")
        msg.setText(f"Đã chuyển đổi thành công {num_files} file!")
        msg.setInformativeText(f"File PDF được lưu tại:\n{self.pdf_folder}")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.buttonClicked.connect(lambda: open_file_location(self.pdf_folder))
        msg.exec() 