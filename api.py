from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from src.processor import OCRProcessor
import tempfile
import os

app = FastAPI(title="OCR Processing API")
processor = OCRProcessor()


@app.post("/process")
async def process_document(file: UploadFile = File('C:/Users/Casper/Desktop/Github/ocr_processor/test/python_alistirmalar.pdf')):
    """
    Yüklenen belgeyi işleme ve çıkarılan metni döndürmesi
    """
    try:
        # Yüklenen dosyayı geçici olarak kaydetme
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # dökümanı işleme
        result = processor.process_document(temp_file_path)

        # temizleme
        os.unlink(temp_file_path)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)