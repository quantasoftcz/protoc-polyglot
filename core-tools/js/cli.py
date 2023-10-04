#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class Lang_UI(Base_UI):
    protoc_plugin:str = plugin_path_js
    dir_output:str = join(OUTPUT_ROOT, 'js') # e.g. /workspace/output/python

    @staticmethod
    def _compile(files:list[str]) -> None:
        shutil.rmtree(Lang_UI.dir_output, ignore_errors=True)
        os.makedirs(Lang_UI.dir_output, exist_ok=False)
        
        com = f"""protoc \
        -I={ROOT_PROTOS} \
        {" ".join(files)} \
        --js_out=import_style=commonjs:{Lang_UI.dir_output} \
        --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{Lang_UI.dir_output}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(Lang_UI)