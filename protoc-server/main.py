import sys, os
from fastapi import FastAPI, HTTPException, status
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

import uvicorn

from zipfile import ZipFile

import string
import random
from os import remove
from shutil import rmtree
from os.path import isdir, join

sys.path.insert(0, os.path.abspath('..'))
import core.python.cli

app = FastAPI()

supported_languages = ['cpp', 'python']
work_dir = '/workspace/tmp/'


def extract_zip_file(file: UploadFile) -> str:
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    dirname = join(work_dir, name)
    try:
        zip_name = f"{dirname}.zip"
        with open(zip_name, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
        with ZipFile(zip_name, 'r') as zObject:
            zObject.extractall(f"{dirname}/")
            mac_path = join(dirname, "__MACOSX/")
            if isdir(mac_path):
                rmtree(mac_path)
        remove(zip_name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error uploading the file")
    finally:
        file.file.close()
    return dirname


def clean_dir(dir: str):
    rmtree(dir)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/compile/{language}")
async def compile_type(language: str, file: UploadFile):
    if language not in supported_languages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unsupported compilation language")

    if '.zip' not in file.filename:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unsupported file format")

    dir_name = extract_zip_file(file)
    ui = core.python.cli.Lang_UI()
    zip_file = ui.make(dir_name)

    return FileResponse(zip_file, media_type='application/zip', filename="output.zip", background=BackgroundTask(clean_dir, dir_name))


if __name__ == "__main__":
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=['../core'])