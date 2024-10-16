#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *


class LanguageInterface(CommonInterface):
    plugin_name = 'protoc-gen-grpc-web'

    def _compile(self, dir_protos:str, dir_output: str, files:list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)
        
        com = f"""protoc \
        -I={dir_protos} \
        {" ".join(files)} \
        --js_out=import_style=commonjs:{dir_output} \
        --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{dir_output}"""
        
        print(com)
        os.system(com)
