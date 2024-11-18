import os
import logging
from typing import Union, List
import re


def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """
   logging yapılandırması
    """
    logging_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    logger = logging.getLogger('OCRProcessor')
    level = logging_levels.get(log_level.upper(), logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    return logger


def validate_file(file_path: str) -> bool:
    """
    dosya kontrolü ve uzantıyı doprulama
    """
    supported_extensions = ['.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg']

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"dosya bulunamadı: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in supported_extensions:
        raise ValueError(
            f"desteklenmeyen format: {file_extension}. "
            f"desteklenen format: {', '.join(supported_extensions)}"
        )

    return True


def clean_text(text: str) -> str:
    """
    çıkan metni temizleme
    """
    # fazla boşluk kaldırma
    text = ' '.join(text.split())

    # özel karakter kaldırma
    text = re.sub(r'[^\w\s\.,!?-]', '', text)

    # satır sonu
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Birden fazla satır sonunu kaldırma
    text = re.sub(r'\n+', '\n', text)

    return text.strip()


def get_file_info(file_path: str) -> dict:
    """
    dosya info
    """
    return {
        'name': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'extension': os.path.splitext(file_path)[1].lower(),
        'path': os.path.abspath(file_path)
    }


def create_output_filename(input_file: str, prefix: str = 'processed_') -> str:
    """
    dosya işlemeden sonra output isimleme
    """
    base_name = os.path.basename(input_file)
    name_without_ext = os.path.splitext(base_name)[0]
    return f"{prefix}{name_without_ext}.txt"


def ensure_directory(directory_path: str) -> str:
    """
    dizin var mı diye kontrol yoksa oluştur.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path


def get_supported_languages() -> List[str]:
    """
    OCR dil desteği ing-tur
    """
    return ['eng', 'tur']  # English and Turkish


def validate_image(image_path: str) -> bool:
    """
    image dosyası doğrulama
    """
    supported_formats = ['.png', '.jpg', '.jpeg']
    ext = os.path.splitext(image_path)[1].lower()

    if ext not in supported_formats:
        raise ValueError(f"desteklenmeyen image format: {ext}")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image dosyası bulunamadı: {image_path}")

    return True