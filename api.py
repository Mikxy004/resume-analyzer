from fastapi import FastAPI, UploadFile, File, HTTPException
from main import analyze_resume

app = FastAPI()


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()


        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)

        results = analyze_resume(temp_path)

        return {
            "filename": file.filename,
            "resume_text": results.get("text", ""),
            "skills": results.get("skills", []),
            "score": results.get("score", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
