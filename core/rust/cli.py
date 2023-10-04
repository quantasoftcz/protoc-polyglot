#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from core.cli import *


class Lang_UI(Base_UI):
    protoc_plugin:str = path_rust_plugin

    @staticmethod
    def _compile(dir_protos:str, files:list[str]) -> None:
        dir_output = join(dir_protos, "output/rust/")

        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        -I {dir_protos} \
        --plugin=protoc-gen-rust={Lang_UI.protoc_plugin} \
        --rust_out={dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(Lang_UI)