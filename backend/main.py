import hashlib
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.modules import PDFParser, TextCleaner, InformationExtractor, ResumeMatcher

app = FastAPI(title="简历分析系统 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}


def get_file_hash(file_content: bytes) -> str:
    return hashlib.md5(file_content).hexdigest()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_requirement: str = Form("")
):
    try:
        if not resume.filename.endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "仅支持 PDF 格式文件"}
            )

        file_content = await resume.read()
        file_hash = get_file_hash(file_content)
        cache_key = f"{file_hash}_{hashlib.md5(job_requirement.encode()).hexdigest()}"

        if cache_key in cache:
            return {"success": True, "data": cache[cache_key]}

        raw_text = PDFParser.extract_text(file_content)
        cleaned_text = TextCleaner.clean_text(raw_text)
        info = InformationExtractor.extract_all(cleaned_text)

        match_score = ResumeMatcher.calculate_match_score(cleaned_text, job_requirement)

        result_data = {
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "info": info,
            "match_score": match_score
        }

        cache[cache_key] = result_data

        return {"success": True, "data": result_data}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
