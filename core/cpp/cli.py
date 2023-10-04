#!/usr/bin/python3
import os, sys
sys.path.insert(0, os.path.abspath('..'))
from core.cli import *

from glob import glob


class Lang_UI(Base_UI):
    protoc_plugin:str = path_cpp_plugin
    dir_output:str = join(OUTPUT_ROOT, 'cpp') # e.g. /workspace/output/python
    
    @staticmethod
    def _compile(files:list[str]):
        dir_src = join(Lang_UI.dir_output, 'src')
        dir_include = join(Lang_UI.dir_output, 'include')

        shutil.rmtree(Lang_UI.dir_output, ignore_errors=True)
        
        os.makedirs(dir_src, exist_ok=True)
        os.makedirs(dir_include, exist_ok=True)

        com = f'protoc -I {ROOT_PROTOS} \
        --plugin=protoc-gen-grpc={Lang_UI.protoc_plugin} \
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

if __name__ == '__main__':
    Fire(Lang_UI)
