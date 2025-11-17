from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from batch import run_batch

app = FastAPI()

BASE = Path("/workspace/ffmpegbatch")
INPUT = BASE / "data" / "input"
OUTPUT = BASE / "data" / "output"

app.mount("/", StaticFiles(directory=BASE/"frontend", html=True), name="frontend")


@app.post("/upload")
async def upload_file(file: UploadFile):
    INPUT.mkdir(parents=True, exist_ok=True)
    dest = INPUT / file.filename
    with open(dest, "wb") as f:
        f.write(await file.read())
    return {"ok": True, "file": file.filename}


@app.get("/run-batch")
def run():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = run_batch(str(INPUT))
    return {"generated": results}


@app.get("/files")
def list_files():
    return {"files": [str(p.name) for p in OUTPUT.glob("*.mp4")]}


@app.get("/download/{name}")
def download(name: str):
    f = OUTPUT / name
    if f.exists():
        return FileResponse(f)
    return {"error": "not found"}
