import base64

def get_image_as_base64(file_path):
    """
    이미지 파일을 base64 문자열로 변환합니다.
    
    Args:
        file_path (str): 이미지 파일의 경로
        
    Returns:
        str: base64로 인코딩된 이미지 문자열
    """
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None 