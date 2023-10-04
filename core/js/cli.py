#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *
from os.path import join
import shutil


class UI_lang(Base_UI):
    protoc_plugin:str = path_js_plugin
    language:str = 'js'

    @staticmethod
    def _compile(dir_protos:str, files:list[str]) -> None:
        dir_output = join(dir_protos, "output/js/")

        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)
        
        com = f"""protoc \
        -I={dir_protos} \
        {" ".join(files)} \
        --js_out=import_style=commonjs:{dir_output} \
        --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{dir_output}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_lang)