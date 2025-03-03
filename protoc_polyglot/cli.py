#!/usr/bin/python3
from fire import Fire
import importlib
import sys
import os
from os.path import abspath
from os.path import dirname
import argparse
from enum import Enum

from protoc_polyglot.interface_loader import get_language_interface

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

        language_interface = get_language_interface(language)

        if hasattr(language_interface, function):
            fc = getattr(language_interface, function)
            fc(args.service_name)
        else:
            print(f"Function '{function}' not found in '{language}.cli'")

if __name__ == '__main__':
    main()