import os, sys, shutil
from os.path import dirname as dirname
from os.path import basename as basename
from os.path import abspath as abspath
from os.path import join as join
from fire import Fire
from glob import glob

chdir(dirname(abspath(sys.argv[0]))) # go to dir with script
sys.path.insert(0, abspath('..'))
from core.cli import *


class UI_specific(Base_UI):
    protoc_plugin:str = path_js_plugin
    dir_output_base:str = pjoin(OUTPUT_ROOT, 'java')

    # def compile(self, name, files):
    #     dir_output = pjoin(UI_python.dir_output_base, name)
    #     os.makedirs(dir_output, exist_ok=True)
    #     com = f'protoc -I {dir_protos} --plugin=protoc-gen-grpc={path_python_plugin} --grpc_out={dir_output} --python_out={dir_output} {" ".join(files)}'
    #     print(com)
    #     os.system(com)

    @staticmethod
    def _compile(name, files):
        # files = glob(pjoin(dir_protos, dir, '*.proto'))
        # java_out = pjoin(UI_java.dir_output_base, dir)
        java_out = pjoin(UI_specific.dir_output_base, name)
        os.makedirs(java_out, exist_ok=True)
        print(f'mkdir {java_out}')

        # grpc_out = f'--grpc_out={java_out}' if gen_grpc else ''
        com = f'protoc -I {dir_protos} --plugin=protoc-gen-grpc_java={path_java_plugin} --grpc_java_out={java_out} --java_out={java_out} {" ".join(files)}'
        print(com)
        os.system(com)

if __name__ == '__main__':
    Fire(UI_specific)