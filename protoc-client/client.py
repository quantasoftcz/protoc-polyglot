import requests
from os import walk, remove, chdir
from os.path import join, exists
from zipfile import ZipFile
from fire import Fire

ip = 'localhost:8000'


def zipFiles(zip_file: str, protos_dir: str = ""):
    with ZipFile(zip_file, 'w') as zip:
        for root, directories, files in walk(protos_dir):
            for filename in files:
                if ".proto" in filename:
                    filepath = join(root, filename)
                    zip.write(filepath)

def getProtos(zip_file: str, result_zip: str, output_dir: str, language: str):
    r = ""
    try:
        with open(zip_file, 'rb') as f:
            r = requests.post(f'http://{ip}/compile/{language}', files={"file": (zip_file, f)})
            r.raise_for_status()
            print(r.status_code)
            with open(result_zip, "wb") as output:
                output.write(r.content)
                with ZipFile(result_zip, 'r') as zObject:
                    zObject.extractall(output_dir)
    except requests.exceptions.RequestException as e:
        print(e)
        if r.json()['detail']:
            print("Upload failed:", r.json()['detail'])
    finally:
        if exists(zip_file):
            remove(zip_file)
        if exists(result_zip):
            remove(result_zip)


def getProtoFiles(name:str, language: str = "python", root_dir:str = "./"):
    # TODO: Check if name is a directory or a service
    protos_dir = name

    chdir(root_dir)

    zip_file = f"{protos_dir}.zip"
    result_zip = f"{protos_dir}/output.zip"
    output_dir = f"{protos_dir}/output/"

    zipFiles(zip_file, protos_dir)
    getProtos(zip_file, result_zip, output_dir, language)


if __name__ == "__main__":
    Fire(getProtoFiles)