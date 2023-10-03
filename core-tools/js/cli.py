#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class UI_lang(Base_UI):
    protoc_plugin:str = path_js_plugin
    dir_output_base:str = join(OUTPUT_ROOT, 'js') # e.g. /workspace/output/python

    @staticmethod
    def _compile(name:str, files:list[str]) -> None:
        dir_output = UI_lang.dir_output_base

        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)
        
        com = f"""protoc \
        -I={ROOT_PROTOS} \
        {" ".join(files)} \
        --js_out=import_style=commonjs:{dir_output} \
        --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{dir_output}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_lang)