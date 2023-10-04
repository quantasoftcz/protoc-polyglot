#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class Lang_UI(Base_UI):
    protoc_plugin:str = plugin_path_java
    dir_output:str = join(OUTPUT_ROOT, 'java')

    @staticmethod
    def _compile(files):
        os.makedirs(Lang_UI.dir_output, exist_ok=True)
        print(f'mkdir {Lang_UI.dir_output}')

        com = f'protoc -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc_java={Lang_UI.protoc_plugin} \
        --grpc_java_out={Lang_UI.dir_output} \
        --java_out={Lang_UI.dir_output} \
        {" ".join(files)}'
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(Lang_UI)