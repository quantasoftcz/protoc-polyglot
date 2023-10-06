#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from core.cli import *
import shutil


class Lang_UI(Base_UI):
    protoc_plugin:str = plugin_path_js

    @staticmethod
    def _compile(dir_protos:str, output_dir: str, files:list[str]) -> None:
        dir_output = join(output_dir, "js/")

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
    Fire(Lang_UI)