from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os
import tempfile
from src.transcription.parser import TranscriptionParser
from src.transcription.preprocessor import TranscriptionPreprocessor
from src.minutes.generator import MinutesGenerator
from src.minutes.formatter import MinutesFormatter

app = FastAPI(
    title="議事録生成システム",
    description="文字起こしから議事録を自動生成するAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

parser = TranscriptionParser()
preprocessor = TranscriptionPreprocessor()
generator = MinutesGenerator()
formatter = MinutesFormatter()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/info")
async def api_info():
    return {"message": "議事録生成システムAPI", "version": "1.0.0"}

@app.post("/upload-transcription/")
async def upload_transcription(
    file: UploadFile = File(...),
    meeting_title: str = Form("会議"),
    meeting_date: Optional[str] = Form(None),
    output_format: str = Form("html")
):
    """
    文字起こしファイルをアップロードして議事録を生成
    """
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="テキストファイル(.txt, .md)のみサポートしています")
    
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        cleaned_text = preprocessor.clean_text(text)
        normalized_text = preprocessor.normalize_speakers(cleaned_text)
        
        segments = parser.parse_transcription(normalized_text)
        
        if not segments:
            raise HTTPException(status_code=400, detail="有効な文字起こしデータが見つかりませんでした")
        
        minutes_data = generator.generate_minutes(segments, meeting_title, meeting_date)
        
        if output_format.lower() == "html":
            content = formatter.format_to_html(minutes_data)
            return HTMLResponse(content=content)
        elif output_format.lower() == "markdown":
            content = formatter.format_to_markdown(minutes_data)
            return {"content": content, "format": "markdown"}
        elif output_format.lower() == "pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                formatter.format_to_pdf(minutes_data, tmp_file.name)
                return FileResponse(
                    tmp_file.name,
                    media_type="application/pdf",
                    filename=f"{meeting_title}_議事録.pdf"
                )
        else:
            raise HTTPException(status_code=400, detail="サポートされていない出力形式です")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"処理中にエラーが発生しました: {str(e)}")

@app.post("/generate-minutes/")
async def generate_minutes_from_text(
    transcription_text: str = Form(...),
    meeting_title: str = Form("会議"),
    meeting_date: Optional[str] = Form(None),
    output_format: str = Form("html")
):
    """
    テキストから直接議事録を生成
    """
    try:
        cleaned_text = preprocessor.clean_text(transcription_text)
        normalized_text = preprocessor.normalize_speakers(cleaned_text)
        
        segments = parser.parse_transcription(normalized_text)
        
        if not segments:
            raise HTTPException(status_code=400, detail="有効な文字起こしデータが見つかりませんでした")
        
        minutes_data = generator.generate_minutes(segments, meeting_title, meeting_date)
        
        if output_format.lower() == "html":
            content = formatter.format_to_html(minutes_data)
            return HTMLResponse(content=content)
        elif output_format.lower() == "markdown":
            content = formatter.format_to_markdown(minutes_data)
            return {"content": content, "format": "markdown"}
        else:
            return minutes_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"処理中にエラーが発生しました: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "議事録生成システム"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
