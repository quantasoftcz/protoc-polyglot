#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from cli import *


class UI_lang(Base_UI):
    protoc_plugin:str = path_java_plugin
    dir_output:str = join(OUTPUT_ROOT, 'java')

    @staticmethod
    def _compile(files):
        os.makedirs(UI_lang.dir_output, exist_ok=True)
        print(f'mkdir {UI_lang.dir_output}')

        com = f'protoc -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc_java={UI_lang.protoc_plugin} \
        --grpc_java_out={UI_lang.dir_output} \
        --java_out={UI_lang.dir_output} \
        {" ".join(files)}'
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_lang)