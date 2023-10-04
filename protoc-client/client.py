import requests
from os import walk, remove, chdir
from os.path import join
from zipfile import ZipFile

root_dir = "../samples/"
protos_dir = "bookclub"
ip = 'localhost:8000'

file_paths = []

chdir(root_dir)

zip_file = f"{protos_dir}.zip"
zip_name = f"{protos_dir}/output.zip"

try:
    with ZipFile(zip_file, 'w') as zip:
        for root, directories, files in walk(protos_dir):
            for filename in files:
                if ".proto" in filename:
                    filepath = join(root, filename)
                    zip.write(filepath)

    with open(zip_file, 'rb') as f:
        r = requests.post(f'http://{ip}/compile/cpp', files={"file": (zip_file, f)})
        r.raise_for_status()
        print(r.status_code)
        with open(zip_name, "wb") as output:
            output.write(r.content)
            with ZipFile(zip_name, 'r') as zObject:
                zObject.extractall(f"{protos_dir}/output/")
except requests.exceptions.RequestException as e:
    print("Upload failed:", e)
finally:
    remove(zip_file)
    remove(zip_name)