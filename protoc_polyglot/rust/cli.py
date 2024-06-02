#!/usr/bin/python3
import os, sys

sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *

class Lang_UI(Base_UI):
    
    def _compile(self, dir_protos: str, dir_output: str, files: list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)
        
        com = f"""/usr/bin/protoc \
        -I {dir_protos} \
        --plugin=protoc-gen-rust={self.settings.plugin_path_rust} \
        --rust_out={dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(Lang_UI)
