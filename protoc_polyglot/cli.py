#!/usr/bin/python3
import os, sys, shutil, yaml
from os.path import dirname, basename, abspath, join
from fire import Fire
from zipfile import ZipFile
import requests


class Settings:
    def __init__(self,
                 plugins_base_path='/usr/bin',
                 grpc_version="1.54.3",
                 protobuf_version="3.21.12",
                 DATA_DIR='/data',
                 CORE_DIR='/protoc_polyglot'):
        self.plugins_base_path = plugins_base_path
        self.grpc_version = grpc_version
        self.protobuf_version = protobuf_version
        
        self.plugin_path_cpp = f'{plugins_base_path}/grpc_cpp_plugin'
        self.plugin_path_java = f'{plugins_base_path}/protoc-gen-grpc-java'
        self.plugin_path_rust = f'{plugins_base_path}/protoc-gen-rust'
        self.plugin_path_go = f'{plugins_base_path}/protoc-gen-go'
        self.plugin_path_csharp = f'{plugins_base_path}/grpc_csharp_plugin'
        self.plugin_path_doc = f'{plugins_base_path}/protoc-gen-doc'
        
        self.DATA_DIR        = DATA_DIR
        self.CORE_DIR        = CORE_DIR
        self.ROOT_PROTOS     = join(DATA_DIR, 'protos')
        self.OUTPUT_ROOT     = join(DATA_DIR, 'output')
        self.DOC_OUTPUT_DIR  = join(self.OUTPUT_ROOT, 'doc')
        
        self.services_yaml   = join(self.ROOT_PROTOS, 'services.yml')
    
class Tools:
    @staticmethod
    def get_service_info(services_yaml, name:str, key:str = 'files') -> dict[str, list[str]] | list[str]:
        with open(services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            
            if name=="":
                return {n: data[n][key] for n in data}
            else:
                return data[name][key]

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
    def download_file(name, saveto):
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

class Base_UI:
    def __init__(self, settings=None):
        if settings:
            self.settings = settings
        else:
            self.settings = Settings()

    def get_plugin_path(self) -> str:
        return join(self.settings.plugins_base_path, self.plugin_name)
    
    def get_grpc_path(self) -> str:
        return "plugins/grpc"
    
    def download_grpc_and_protobuf(self):
        name = f"15369526/grpc-{self.settings.grpc_version}_protobuf-{self.settings.protobuf_version}.zip"
        if not os.path.exists(self.get_grpc_path()):
            print("gRPC missing, downloading...")
        return Tools.download_file(name, self.get_grpc_path())
        
    def download_plugin(self):
        if not os.path.exists(self.get_plugin_path()):
            print("Plugin missing, downloading...")
        return Tools.download_file("grpc_python_plugin", self.get_plugin_path())
            
    
    def list(self):
        print(os.getcwd())
        
        with os.scandir(self.settings.CORE_DIR) as entries:
            print('Supported languages:')
            folders = [entry.name for entry in entries if entry.is_dir() and entry.name not in ['__pycache__']]
            for f in folders:
                print(f)
        
        # if self.settings.CORE_DIR == '':
        #     print('Hello world from polyglot')
        #     exit()
        
        exit()
        
        with open(self.settings.services_yaml, 'r') as file:
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
        files = Tools.get_files_from_directory(dir_protos)
        dir_output = join(dir_protos, "output")
        self._compile(dir_protos, dir_output, files)
        return Tools.zip_directory(dir_output)
    
    def protoc(self, compile_func, name:str=""):
        if not self.download_grpc_and_protobuf():
            raise RuntimeError("Could not find gRPC and Protobuf package")
        if not self.download_plugin():
            raise RuntimeError(f"Could not find {name} release")
        
        if self.__class__.__name__ == "Base_UI":
            print("ERROR: Use a language")
            exit(1)
        
        files = Tools.get_service_info(self.settings.services_yaml, name)
        compile_func(self.settings.ROOT_PROTOS, self._get_dir_output(name), files)

        self.doc()
        
    def _get_dir_output(self, name):
        lang_name = os.path.basename(os.path.dirname(os.path.realpath(sys.argv[0])))
        # converts ./python/cli.py -> /core/python/cli.py -> /core/python -> python
        
        return join(self.settings.OUTPUT_ROOT, lang_name, name)

    def doc(self, md=True, html=False):
        for name, files in Tools.get_service_info(self.settings.services_yaml, name='').items():
            aux = ' '.join(files)
            os.makedirs(self.settings.DOC_OUTPUT_DIR, exist_ok=True)
            if md:
                com = f'protoc -I {self.settings.ROOT_PROTOS} --plugin=protoc-gen-doc={self.settings.plugin_path_doc} --doc_out={self.settings.DOC_OUTPUT_DIR} --doc_opt=markdown,{name}.md {aux}'
                print(com)
                os.system(com)

                # fix links by "a name" -> "a id"
                text = open(join(self.settings.DOC_OUTPUT_DIR, f'{name}.md'), 'r', encoding="utf-8").read()
                text = text.replace('<a name=', '<a id=')
                text = text.replace(' &lt;br&gt;', ' <br>')
                open(join(self.settings.DOC_OUTPUT_DIR, f'{name}.md'), 'w', encoding="utf-8").write(text)
            if html:
                com = f'protoc -I {self.settings.ROOT_PROTOS} --plugin=protoc-gen-doc={self.settings.plugin_path_doc} --doc_out={self.settings.DOC_OUTPUT_DIR} --doc_opt=html,{name}.html {aux}'
                print(com)
                os.system(com)
        print(f'\ndone, docs saved in {self.settings.DOC_OUTPUT_DIR}')
    

if __name__ == '__main__':
    Fire(Base_UI)