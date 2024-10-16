#!/usr/bin/python3
import os, sys, shutil, yaml
from os.path import dirname, basename, abspath, join
from fire import Fire
from zipfile import ZipFile
import requests

from protoc_polyglot.tools import Tools
from protoc_polyglot.settings import *


class CommonInterface:
    def __init__(self, settings: Settings=None):
        self.settings = settings

    def get_plugin_executable_path(self):
        return join(self.get_plugin_dir(), self.plugin_name)

    def get_plugin_dir(self) -> str:
        return join(self.settings.plugins_base_path, self.get_language())

    def get_protobuf_path(self) -> str:
        return join(self.settings.plugins_base_path, self.settings.protobuf_folder)
    
    def get_grpc_path(self) -> str:
        return join(self.settings.plugins_base_path, self.settings.grpc_folder)

    def get_language(self):
        assert hasattr(self, 'plugin_name'), "This function can only be called on LanguageInterface"

        return self.settings.language

    def download_grpc_and_protobuf(self):
        if os.path.exists(self.get_grpc_path()) and os.path.exists(self.get_protobuf_path()):
            return True

        print("gRPC or Protobuf missing, downloading...")
        name = f"grpc-{self.settings.grpc_version}_protobuf-{self.settings.protobuf_version}.zip"
        return Tools.download_file(name, self.get_grpc_path())

    def download_plugin(self):
        assert hasattr(self, 'plugin_name'), "This function can only be called on LanguageInterface"

        if self.get_language() not in self.settings.languages_that_have_external_plugin or os.path.exists(self.get_plugin_dir()):
            return True

        print("Plugin missing, downloading...")
        return Tools.download_file(self.plugin_name, self.get_plugin_dir())

    def list(self):
        print(os.getcwd())
        
        with os.scandir(self.settings.CORE_DIR) as entries:
            print('Supported languages:')
            folders = [entry.name for entry in entries if entry.is_dir() and entry.name not in ['__pycache__']]
            for f in folders:
                print(f)
        
        with open(self.settings.services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            print('Found services:')
            for name in data:
                print(f'- {name}')
                for file in data[name]['files']:
                    print(f'\t- {file}')

    def make(self, dir: str):
        if self.__class__.__name__ == "CommonInterface":
            print("ERROR: Use a language")
            exit(1)

        dir_protos = os.path.abspath(dir)
        files = Tools.get_files_from_directory(dir_protos)
        dir_output = join(dir_protos, "output")
        self._compile(dir_protos, dir_output, files)
        return Tools.zip_directory(dir_output)
    
    def protoc(self, name:str=""):
        assert hasattr(self, 'plugin_name'), "This function can only be called on LanguageInterface"

        if not self.download_grpc_and_protobuf():
            raise RuntimeError("Could not find gRPC and Protobuf package")
        if not self.download_plugin():
            raise RuntimeError(f"Could not find {name} release")
        
        if self.__class__.__name__ == "CommonInterface":
            print("ERROR: Use a language")
            exit(1)
        
        files_dict = Tools.get_service_info(self.settings.services_yaml, name)
        for name, files in files_dict.items():
            self._compile(self.settings.ROOT_PROTOS, self._get_dir_output(name), files)

        self.doc()
        
    def _get_dir_output(self, name:str):
        return join(self.settings.OUTPUT_ROOT, self.get_language(), name)

    def doc(self, md:bool=True, html:bool=False):
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
