#!/usr/bin/python3
import os, sys, shutil, yaml
from os.path import dirname, basename, abspath, join
from fire import Fire
from zipfile import ZipFile

plugin_path_cpp     = '/usr/bin/grpc_cpp_plugin'
plugin_path_python  = '/usr/bin/grpc_python_plugin'
plugin_path_csharp  = '/usr/bin/grpc_csharp_plugin'
plugin_path_java    = '/usr/bin/protoc-gen-grpc-java'
plugin_path_js      = '/usr/bin/protoc-gen-grpc-web'
plugin_path_rust    = '/root/.cargo/bin/protoc-gen-rust'
plugin_path_go      = '/root/go/bin/protoc-gen-go'
plugin_path_doc     = '/usr/bin/protoc-gen-doc'

DATA_DIR        = '/data'
ROOT_PROTOS     = join(DATA_DIR, 'protos')
OUTPUT_ROOT     = join(DATA_DIR, 'output')
DOC_OUTPUT_DIR  = join(DATA_DIR, 'doc-output')

services_yaml   = join(ROOT_PROTOS, 'services.yml')

def get_service_files(name:str) -> dict[str, list[str]]:
    with open(services_yaml, 'r') as file:
        data = yaml.safe_load(file)
        
        if name=="*":
            return {n: data[n]['files'] for n in data}
        else:
            return {name: data[name]['files']}

def get_files_from_directory(dir: str):
    proto_files = []
    for root, directories, files in os.walk(dir):
        for filename in files:
            if ".proto" in filename:
                proto_files.append(join(root, filename))
    return proto_files

def zip_directory(dir: str):
    zip_file = f'{dir}.zip'
    with ZipFile(zip_file, 'w') as zip:
        for root, directories, files in os.walk(dir):
            for filename in files:
                filepath = join(root, filename)
                zip.write(filepath, filepath[len(dir):])
    return zip_file

class Base_UI:
    def info(self):
        with open(services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            for name in data:
                print(f'- {name}')
                for file in data[name]['files']:
                    print(f'\t- {file}')

    def make(self, dir: str):
        if self.__class__.__name__ == "Base_UI":
            print("ERROR: Use a language")
            exit(1)

        dir_protos = os.path.abspath(dir)
        files = get_files_from_directory(dir_protos)
        dir_output = join(dir_protos, "output")
        self._compile(dir_protos, dir_output, files)
        return zip_directory(dir_output)

    def protoc(self, name:str=""):
        if len(name) == 0:
            self.info()
            exit(0)
            
        if self.__class__.__name__ == "Base_UI":
            print("ERROR: Run this command in selected language subfolder")
            exit(1)
        
        services = get_service_files(name)
        
        for name, files in services.items():
            self._compile(ROOT_PROTOS, OUTPUT_ROOT, files)

if __name__ == '__main__':
    Fire(Base_UI)