App_PPTX_To_PDF/
├── app.py                          # File chính để chạy ứng dụng
├── src/                           # Thư mục chứa mã nguồn
│   ├── __init__.py               # File để Python nhận diện là package
│   ├── converters/               # Module xử lý chuyển đổi file
│   │   ├── powerpoint_converter.py
│   │   └── word_converter.py
│   ├── gui/                      # Module giao diện người dùng
│   │   ├── dropzone.py
│   │   └── main_window.py
│   └── utils/                    # Module tiện ích
│       └── file_utils.py