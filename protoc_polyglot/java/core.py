#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *


class LanguageInterface(Base_UI):
    plugin_name = 'protoc-gen-grpc-java'

    def _compile(self, dir_protos:str, dir_output: str, files:list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=True)
        print(f'mkdir {dir_output}')

        com = f'protoc -I {dir_protos} \
        --plugin=protoc-gen-grpc_java={self.get_plugin_executable_path()} \
        --grpc_java_out={dir_output} \
        --java_out={dir_output} \
        {" ".join(files)}'
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(LanguageInterface)