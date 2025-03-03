#!/usr/bin/python3
import os, sys

sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.common_interface import *


class LanguageInterface(CommonInterface):
    plugin_name = 'grpc_python_plugin'

    def _compile(self, dir_protos: str, dir_output: str, files: list[str]) -> None:
        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""{self.settings.protoc_binary} \
        -I {dir_protos} \
        --plugin=protoc-gen-grpc={self.get_plugin_executable_path()} \
        --grpc_out={dir_output} \
        --python_out={dir_output} \
        {" ".join(files)}"""

        print(com)
        if os.system(com) != 0:
            raise RuntimeError(f"Error compiling {com}")
