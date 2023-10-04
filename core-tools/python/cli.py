#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class UI_lang(Base_UI):
    protoc_plugin:str = path_python_plugin
    dir_output:str = join(OUTPUT_ROOT, 'python') # e.g. /workspace/output/python

    @staticmethod
    def _compile(files:list[str]) -> None:
        shutil.rmtree(UI_lang.dir_output, ignore_errors=True)
        os.makedirs(UI_lang.dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc={UI_lang.protoc_plugin} \
        --grpc_out={UI_lang.dir_output} \
        --python_out={UI_lang.dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_lang)