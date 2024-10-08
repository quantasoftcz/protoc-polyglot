#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from protoc_polyglot.cli import *

from glob import glob


class LanguageInterface(CommonInterface):
    plugin_name = 'grpc_cpp_plugin'

    def _compile(self, dir_protos:str, dir_output: str, files:list[str]) -> None:
        dir_src = join(dir_output, 'src')
        dir_include = join(dir_output, 'include')

        shutil.rmtree(dir_output, ignore_errors=True)

        os.makedirs(dir_src, exist_ok=True)
        os.makedirs(dir_include, exist_ok=True)

        com = f'protoc -I {dir_protos} \
        --plugin=protoc-gen-grpc={self.get_plugin_executable_path()} \
        --grpc_out={dir_src} \
        --cpp_out={dir_src} \
        {" ".join(files)}'
        
        print(com)
        ret = os.system(com)
        if ret:
            return ret

        # move header files to include folder
        for path in glob(join(dir_src, '**/*.pb.h'), recursive=True):
            newpath = path.replace(dir_src, dir_include)
            os.makedirs(dirname(newpath), exist_ok=True)
            shutil.move(path, newpath)

        return ret
