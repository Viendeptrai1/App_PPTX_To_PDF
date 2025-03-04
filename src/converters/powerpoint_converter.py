import io
import tempfile
from pptx import Presentation
import img2pdf
from PIL import Image, ImageDraw
import os

def convert_pptx_to_pdf(file_path, output_path):
    """
    Chuyển đổi file PowerPoint sang PDF bằng cách chuyển từng slide thành ảnh
    """
    prs = Presentation(file_path)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        image_files = []
        
        # Xử lý từng slide
        for i, slide in enumerate(prs.slides):
            # Tạo ảnh trắng với kích thước A4
            img = Image.new('RGB', (2480, 3508), 'white')  # A4 size at 300 DPI
            draw = ImageDraw.Draw(img)
            y_position = 100
            
            # Xử lý text và hình ảnh trong slide
            for shape in slide.shapes:
                if hasattr(shape, 'text'):
                    text = shape.text
                    if text:
                        # Vẽ text lên ảnh
                        draw.text((100, y_position), text, fill='black')
                        y_position += 50
                
                if hasattr(shape, 'image'):
                    try:
                        # Đọc và chèn hình ảnh
                        image_stream = io.BytesIO(shape.image.blob)
                        shape_img = Image.open(image_stream)
                        
                        # Tính toán kích thước mới cho hình ảnh
                        max_width = 2280  # Margin 100px mỗi bên
                        ratio = max_width / shape_img.width
                        new_size = (int(shape_img.width * ratio), int(shape_img.height * ratio))
                        shape_img = shape_img.resize(new_size, Image.Resampling.LANCZOS)
                        
                        # Chèn hình ảnh vào slide
                        img.paste(shape_img, (100, y_position))
                        y_position += shape_img.height + 50
                    except Exception as e:
                        print(f"Lỗi khi xử lý hình ảnh: {str(e)}")
                        continue
            
            # Lưu slide dưới dạng ảnh
            image_path = os.path.join(temp_dir, f'slide_{i}.png')
            img.save(image_path, 'PNG')
            image_files.append(image_path)
        
        # Chuyển đổi tất cả các ảnh thành một file PDF
        if image_files:
            with open(output_path, 'wb') as pdf_file:
                pdf_file.write(img2pdf.convert(image_files))
            return True
    return False 