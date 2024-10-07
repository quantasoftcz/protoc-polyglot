#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *


class LanguageInterface(CommonInterface):
    plugin_name = 'protoc-gen-go'

    def _compile(self, dir_protos:str, dir_output: str, files:list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        -I {ROOT_PROTOS} \
        --plugin=protoc-gen-go={self.get_plugin_executable_path()} \
        --go_out={dir_output} \
        --go_opt=paths=source_relative \
        --go-grpc_out={dir_output} \
        --go-grpc_opt=paths=source_relative \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)
