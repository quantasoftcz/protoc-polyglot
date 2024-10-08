#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *


class LanguageInterface(CommonInterface):
    def _compile(self, dir_protos:str, dir_output: str, files:list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        --proto_path {dir_protos} \
        --php_out={dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)
