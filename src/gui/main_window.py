from PyQt6.QtWidgets import QMainWindow
from .dropzone import DropZone

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Khởi tạo giao diện người dùng
        """
        self.setWindowTitle('Chuyển đổi PPT/Word sang PDF')
        self.setMinimumSize(500, 300)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #FFF0F5;
            }
        ''')

        dropzone = DropZone()
        self.setCentralWidget(dropzone.container) 