#!/usr/bin/python3
import os, sys, shutil, yaml
from os.path import dirname as dirname
from os.path import basename as basename
from os.path import abspath as abspath
from os.path import join as join
from os import chdir as chdir
from fire import Fire

path_cpp_plugin = '/usr/bin/grpc_cpp_plugin'
path_python_plugin = '/usr/bin/grpc_python_plugin'
path_csharp_plugin = '/usr/bin/grpc_csharp_plugin'
path_java_plugin = '/usr/bin/protoc-gen-grpc-java'
path_js_plugin = '/usr/bin/protoc-gen-grpc-web'
path_plugin_doc = '/usr/bin/protoc-gen-doc'

DATA_DIR = '/data'
ROOT_PROTOS = join(DATA_DIR, 'protos')
OUTPUT_ROOT = join(DATA_DIR, 'output')
DOC_OUTPUT_DIR = join(DATA_DIR, 'doc-output')

services_yaml = join(DATA_DIR, 'services.yml')

def get_service_files(name:str) -> dict[str, list[str]]:
    with open(services_yaml, 'r') as file:
        data = yaml.safe_load(file)
        
        if name=="*":
            return {name: data[n]['files'] for n in data}
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
        
        services = get_service_files(name, )
        
        for name, files in services.items():
            self._compile(name, files)

if __name__ == '__main__':
    Fire(Base_UI)