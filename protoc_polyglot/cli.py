#!/usr/bin/python3
from fire import Fire
import importlib
import sys
import os
from os.path import abspath
from os.path import dirname
import argparse
from enum import Enum


class Run_mode(Enum):
    DOCKER = 1
    PYPI = 2

# import of core is different based on whether we run in PyPi package or in Docker
run_mode = Run_mode.DOCKER if os.path.abspath(__file__) == '/protoc_polyglot/cli.py' else Run_mode.PYPI

if run_mode == Run_mode.DOCKER:
    sys.path.append('/')

from protoc_polyglot.common_interface import *

def main():
    parser = argparse.ArgumentParser(description="Process protoc-polyglot command-line arguments.")

    parser.add_argument("-l", "--languages", help="Programming languages for protoc generation.", nargs='+', required=True)
    parser.add_argument("-y", "--service-yml", help="Service YAML file, directory or specific file.", required=True)
    parser.add_argument("-n", "--service-name", help="Service name.", default="")
    parser.add_argument("-d", "--directory-input", help="Directory input.")
    parser.add_argument("-f", "--files", nargs='+', help="List of files to process.")
    parser.add_argument("-o", "--output-dir", default="output", help="Output directory (default: output).")

    args = parser.parse_args()

    print(f"Languages: {args.languages}")
    print(f"Services YML: {args.service_yml}")
    if args.service_name:
        print(f"Service Name: {args.service_name}")
    if args.directory_input:
        print(f"Directory Input: {args.directory_input}")
    if args.files:
        print(f"Files: {', '.join(args.files)}")
    print(f"Output Directory: {args.output_dir}")

    for language in args.languages:
        function = 'protoc'

        if run_mode == Run_mode.PYPI:
            setup_module = importlib.import_module('protoc_polyglot.' + language + '.language_interface', package="protoc-polyglot")
            LanguageInterface = getattr(setup_module, 'LanguageInterface')
            settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
            LanguageInterface = LanguageInterface(settings)
        else:
            module_dir = os.path.join(os.path.dirname(__file__), language)

            sys.path.insert(0, module_dir)

            module_path = os.path.join(module_dir, 'language_interface.py')

            spec = importlib.util.spec_from_file_location('cli', module_path)
            setup_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(setup_module)

            LanguageInterface = getattr(setup_module, 'LanguageInterface')
            settings = Settings(language)
            LanguageInterface = LanguageInterface(settings)

            sys.path.pop(0)

        if hasattr(LanguageInterface, function):
            fc = getattr(LanguageInterface, function)
            fc(args.service_name)
        else:
            print(f"Function '{function}' not found in '{language}.cli'")

if __name__ == '__main__':
    main()