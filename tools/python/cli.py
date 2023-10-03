#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class UI_lang(Base_UI):
    protoc_plugin:str = path_python_plugin
    dir_output_base:str = join(OUTPUT_ROOT, 'python') # e.g. /workspace/output/python

    @staticmethod
    def _compile(name:str, files:list[str]) -> None:
        dir_output = UI_lang.dir_output_base

        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc={UI_lang.protoc_plugin} \
        --grpc_out={dir_output} \
        --python_out={dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_lang)