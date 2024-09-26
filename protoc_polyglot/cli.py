#!/usr/bin/python3
from fire import Fire
import importlib
from os.path import abspath
from os.path import dirname
import argparse
from protoc_polyglot.cli import *


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process protoc-polyglot command-line arguments.")

    # Add arguments
    parser.add_argument("language/list-command", help="Programming language for protoc generation.")
    parser.add_argument("-y", "service_yml", help="Service YAML file, directory or specific file.")
    parser.add_argument("-n", "--service_name", help="Service name.")
    parser.add_argument("-d", "--directory_input", help="Directory input.")
    parser.add_argument("-f", "--files", nargs='+', help="List of files to process.")
    parser.add_argument("-o", "--output_dir", default="protoc-output", help="Output directory (default: protoc-output).")

    # Parse the arguments
    args = parser.parse_args()

    # Process the arguments
    print(f"Language: {args.language}")
    print(f"Service YAML/Directory/File: {args.service_yml}")
    if args.service_name:
        print(f"Service Name: {args.service_name}")
    if args.directory_input:
        print(f"Directory Input: {args.directory_input}")
    if args.files:
        print(f"Files: {', '.join(args.files)}")
    print(f"Output Directory: {args.output_dir}")

    # def execute(language: str = "", function: str = "", *args):
    try:
        if args.language == '':
            setup_module = importlib.import_module('protoc_polyglot.cli', package="protoc-polyglot")
            LanguageInterface = getattr(setup_module, 'Base_UI')
            settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
            LanguageInterface = LanguageInterface(settings)
        elif args.language == 'list':
            function = 'list'
            setup_module = importlib.import_module('protoc_polyglot.cli', package="protoc-polyglot")
            LanguageInterface = getattr(setup_module, 'LanguageInterface')
            settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
            LanguageInterface = LanguageInterface(settings)
        else:
            function = 'protoc'
            setup_module = importlib.import_module('protoc_polyglot.' + args.language + '.cli', package="protoc-polyglot")
            LanguageInterface = getattr(setup_module, 'LanguageInterface')
            settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
            LanguageInterface = LanguageInterface(settings)

        if hasattr(LanguageInterface, function):
            fc = getattr(LanguageInterface, function)
            fc(*args)
        else:
            print(f"Function '{function}' not found in '{args.language}.cli'")
    except ModuleNotFoundError:
        print(f"Language '{args.language}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
