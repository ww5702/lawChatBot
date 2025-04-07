import base64

def get_image_as_base64(file_path):
    """이미지를 base64로 인코딩하는 함수"""
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None 