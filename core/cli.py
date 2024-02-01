#!/usr/bin/python3
import os, sys, shutil, yaml
from os.path import dirname, basename, abspath, join
from fire import Fire
from zipfile import ZipFile

plugin_path_cpp     = '/usr/bin/grpc_cpp_plugin'
plugin_path_python  = '/usr/bin/grpc_python_plugin'
plugin_path_java    = '/usr/bin/protoc-gen-grpc-java'
plugin_path_rust    = '/usr/bin/protoc-gen-rust'
plugin_path_go      = '/usr/bin/protoc-gen-go'
plugin_path_doc     = '/usr/bin/protoc-gen-doc'

DATA_DIR        = '/data'
CORE_DIR        = '/core'
ROOT_PROTOS     = join(DATA_DIR, 'protos')
OUTPUT_ROOT     = join(DATA_DIR, 'output')
DOC_OUTPUT_DIR  = join(DATA_DIR, 'doc')

services_yaml   = join(ROOT_PROTOS, 'services.yml')

class Polyglot:
    @staticmethod
    def get_service_info(name:str, key:str='files') -> dict[str, list[str]]:
        with open(services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            
            if name=="":
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

class Base_UI:
    def list(self):
        with os.scandir(CORE_DIR) as entries:
            print('Found languages:')
            folders = [entry.name for entry in entries if entry.is_dir() and entry.name not in ['__pycache__']]
            for f in folders:
                print(f)
        
        print()
        with open(services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            print('Found services:')
            for name in data:
                print(f'- {name}')
                for file in data[name]['files']:
                    print(f'\t- {file}')

    def make(self, dir: str):
        if self.__class__.__name__ == "Base_UI":
            print("ERROR: Use a language")
            exit(1)

        dir_protos = os.path.abspath(dir)
        files = Polyglot.get_files_from_directory(dir_protos)
        dir_output = join(dir_protos, "output")
        self._compile(dir_protos, dir_output, files)
        return Polyglot.zip_directory(dir_output)
    
    def protoc(self, name:str=""):
        if self.__class__.__name__ == "Base_UI":
            print("ERROR: Use a language")
            exit(1)
        
        services = Polyglot.get_service_info(name)
        
        for name, files in services.items():
            self._compile(ROOT_PROTOS, OUTPUT_ROOT, files)

    @staticmethod
    def doc(md=True, html=False):
        for name, files in Polyglot.get_service_info("").items():
            aux = ' '.join(files)
            os.makedirs(DOC_OUTPUT_DIR, exist_ok=True)
            if md:
                com = f'protoc -I {ROOT_PROTOS} --plugin=protoc-gen-doc={plugin_path_doc} --doc_out={DOC_OUTPUT_DIR} --doc_opt=markdown,{name}.md {aux}'
                print(com)
                os.system(com)

                # fix links by "a name" -> "a id"
                text = open(join(DOC_OUTPUT_DIR, f'{name}.md'), 'r', encoding="utf-8").read()
                text = text.replace('<a name=', '<a id=')
                text = text.replace(' &lt;br&gt;', ' <br>')
                open(join(DOC_OUTPUT_DIR, f'{name}.md'), 'w', encoding="utf-8").write(text)
            if html:
                com = f'protoc -I {ROOT_PROTOS} --plugin=protoc-gen-doc={plugin_path_doc} --doc_out={DOC_OUTPUT_DIR} --doc_opt=html,{name}.html {aux}'
                print(com)
                os.system(com)
        print(f'\ndone, docs saved in {DOC_OUTPUT_DIR}')
    

if __name__ == '__main__':
    Fire(Base_UI)