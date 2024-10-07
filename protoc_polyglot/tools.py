#!/usr/bin/python3
import os
import yaml
from os.path import dirname, join
from zipfile import ZipFile
import requests


class Tools:
    @staticmethod
    def get_service_info(services_yaml, name: str, key: str = 'files') -> dict[str, list[str]]:
        with open(services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            data = data['services']

            if name == "":
                return {n: data[n][key] for n in data}
            else:
                return {name: data[name][key]}

    @staticmethod
    def get_files_from_directory(dir: str):
        proto_files = []
        for root, directories, files in os.walk(dir):
            for filename in files:
                if ".proto" in filename:
                    proto_files.append(join(root, filename))
        return proto_files

    @staticmethod
    def zip_directory(dir: str):
        zip_file = f'{dir}.zip'
        with ZipFile(zip_file, 'w') as zip:
            for root, directories, files in os.walk(dir):
                for filename in files:
                    filepath = join(root, filename)
                    zip.write(filepath, filepath[len(dir):])
        return zip_file

    @staticmethod
    def download_file(name: str, saveto):
        url = f"https://github.com/quantasoftcz/protoc-polyglot/files/{name}"
        response = requests.get(url)

        if response.status_code == 200:
            os.makedirs(dirname(saveto), exist_ok=True)
            with open(saveto, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
            return False
