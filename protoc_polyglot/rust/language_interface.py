#!/usr/bin/python3
import os, sys

sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *


class LanguageInterface(CommonInterface):
    plugin_name = 'protoc-gen-rust'

    def _compile(self, dir_protos: str, dir_output: str, files: list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""/usr/bin/protoc \
        -I {dir_protos} \
        --plugin=protoc-gen-rust={self.get_plugin_executable_path()} \
        --rust_out={dir_output} \
        {" ".join(files)}"""

        print(com)
        os.system(com)
