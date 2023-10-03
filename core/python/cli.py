#!/usr/bin/python3
import os, sys, shutil
from os.path import dirname as dirname
from os.path import basename as basename
from os.path import abspath as abspath
from os.path import join as join
from os import chdir as chdir
from fire import Fire

chdir(dirname(abspath(sys.argv[0]))) # go to dir with script
sys.path.insert(0, abspath('..'))
from cli import *


class UI_python(Base_UI):
    protoc_plugin:str = path_python_plugin
    dir_output_base:str = join(OUTPUT_ROOT, 'python') # e.g. /workspace/output/python

    @staticmethod
    def _compile(name:str, files:list[str]) -> None:
        dir_output = UI_python.dir_output_base

        shutil.rmtree(dir_output, ignore_errors=True)
        os.makedirs(dir_output, exist_ok=False)

        com = f"""protoc \
        -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc={UI_python.protoc_plugin} \
        --grpc_out={dir_output} \
        --python_out={dir_output} \
        {" ".join(files)}"""
        
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_python)