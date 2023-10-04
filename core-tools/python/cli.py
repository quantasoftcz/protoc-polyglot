#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class Lang_UI(Base_UI):
    protoc_plugin:str = path_python_plugin
    dir_output:str = join(OUTPUT_ROOT, 'python') # e.g. /workspace/output/python

    @staticmethod
    def _compile(files:list[str]) -> None:
        shutil.rmtree(Lang_UI.dir_output, ignore_errors=True)
        os.makedirs(Lang_UI.dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc={Lang_UI.protoc_plugin} \
        --grpc_out={Lang_UI.dir_output} \
        --python_out={Lang_UI.dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(Lang_UI)