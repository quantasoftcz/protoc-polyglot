#!/usr/bin/python3
import os, sys, shutil
from os.path import dirname as getdir
from os.path import basename as getbase
from os.path import join as pjoin
from fire import Fire
from glob import glob
from termcolor import colored

os.chdir(getdir(os.path.abspath(sys.argv[0]))) # go to dir with script
sys.path.insert(0, os.path.abspath('..'))
from cli import *
from generateConanFiles import generateConanFiles


class UI_cpp(Base_UI):
    dir_output_base = pjoin(dir_output, 'cpp') # e.g. /workspace/output/cpp

    def make(self, name:str, version:str=default_version):
        check_version_and_name(version, name)
        dir_protos = os.path.abspath(pjoin(root_protos, version)) # e.g. /workspace/protos/v1
        ret = self.compile(dir_protos, name, services_files[version][name]['files'], version)
        if ret:
            exit(ret)

    def make_all(self, version:str=default_version):
        check_version(version)
        for version, services in services_files.items():
            dir_protos = os.path.abspath(pjoin(root_protos, version))
            for name, params in services.items():
                self.compile(dir_protos, name, params['files'], version)

    def clean(self):
        print(f'deleting {self.dir_output_base}')
        shutil.rmtree(self.dir_output_base, ignore_errors=True)

    def info(self):
        for version in services_files:
            print(colored(f'Version {version}', 'red'))
            for name in services_files[version]:
                print(f'- {colored(name, "green")} -> conan package:', colored(services_files[version][name]["conan-settings"]["package-name"], 'cyan'))
                for file in services_files[version][name]['files']:
                    print(f'\t- {file}')

    def upload(self, name:str, version:str):
        dir_cur_output = pjoin(self.dir_output_base, name, version)
        if not os.path.exists(dir_cur_output):
            print(f'missing folder {dir_cur_output}, compile protos first')
            exit()
        shutil.rmtree(name, ignore_errors=True)
        generateConanFiles(name, services_files[version][name]['conan-settings'])
        shutil.copyfile(pjoin(name, 'conanfile.py'), pjoin(dir_cur_output, 'conanfile.py'))
        shutil.copyfile(pjoin(name, 'conan-upload.sh'), pjoin(dir_cur_output, 'conan-upload.sh'))
        shutil.copyfile(pjoin(name, 'CMakeLists.txt'), pjoin(dir_cur_output, 'CMakeLists.txt'))
        os.system('bash ' + pjoin(dir_cur_output, 'conan-upload.sh'))

    def conan(self, name:str, version:str=default_version):
        check_version_and_name(version, name)
        self.make(name, version)
        self.upload(name, version)

    @staticmethod
    def compile(dir_protos, name, files, version):
        dir_output = pjoin(UI_cpp.dir_output_base, name, version) # e.g. /workspace/output/cpp/VideoAnalyticsV2/v1
        os.makedirs(dir_output, exist_ok=True)

        shutil.rmtree(dir_output, ignore_errors=True)
        dir_src = pjoin(dir_output, 'src')
        dir_include = pjoin(dir_output, 'include')
        os.makedirs(dir_src, exist_ok=True)
        os.makedirs(dir_include, exist_ok=True)

        com = f'protoc -I {dir_protos} --plugin=protoc-gen-grpc={path_cpp_plugin} --grpc_out={dir_src} --cpp_out={dir_src} {" ".join(files)}'
        print(com)
        ret = os.system(com)
        if ret:
            return ret

        # move header files to include folder
        for path in glob(pjoin(dir_src, '**/*.pb.h'), recursive=True):
            newpath = path.replace(dir_src, dir_include)
            os.makedirs(getdir(newpath), exist_ok=True)
            shutil.move(path, newpath)

        return ret

if __name__ == '__main__':
    Fire(UI_cpp)
