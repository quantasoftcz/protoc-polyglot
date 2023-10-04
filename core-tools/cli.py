#!/usr/bin/python3
import os, sys, shutil, yaml
from os.path import dirname, basename, abspath, join
from os import chdir
from fire import Fire

plugin_path_cpp     = '/usr/bin/grpc_cpp_plugin'
plugin_path_python  = '/usr/bin/grpc_python_plugin'
plugin_path_csharp  = '/usr/bin/grpc_csharp_plugin'
plugin_path_java    = '/usr/bin/protoc-gen-grpc-java'
plugin_path_js      = '/usr/bin/protoc-gen-grpc-web'
plugin_path_rust    = '/root/.cargo/bin/protoc-gen-rust'
plugin_path_go      = '/root/go/bin/protoc-gen-go'
plugin_path_doc     = '/usr/bin/protoc-gen-doc'

DATA_DIR        = '/data'
ROOT_PROTOS     = join(DATA_DIR, 'protos')
OUTPUT_ROOT     = join(DATA_DIR, 'output')
DOC_OUTPUT_DIR  = join(DATA_DIR, 'doc-output')

services_yaml   = join(ROOT_PROTOS, 'services.yml')

def get_service_files(name:str) -> dict[str, list[str]]:
    with open(services_yaml, 'r') as file:
        data = yaml.safe_load(file)
        
        if name=="*":
            return {n: data[n]['files'] for n in data}
        else:
            return {name: data[name]['files']}

class Base_UI:
    def info(self):
        with open(services_yaml, 'r') as file:
            data = yaml.safe_load(file)
            for name in data:
                print(f'- {name}')
                for file in data[name]['files']:
                    print(f'\t- {file}')
 
    def protoc(self, name:str=""):
        if len(name) == 0:
            self.info()
            exit(0)
            
        if self.__class__.__name__ == "Base_UI":
            print("ERROR: Run this command in selected language subfolder")
            exit(1)
        
        services = get_service_files(name)
        
        for name, files in services.items():
            self._compile(files)

if __name__ == '__main__':
    Fire(Base_UI)