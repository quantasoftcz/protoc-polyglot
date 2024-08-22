#!/usr/bin/python3
from fire import Fire
import importlib
from os.path import abspath
from os.path import dirname
from protoc_polyglot.cli import *


def execute(language:str="", function:str="", *args):
    try:
        if language=='':
            setup_module = importlib.import_module('protoc_polyglot.cli', package="protoc_polyglot")
            Lang_UI = getattr(setup_module, 'Base_UI')
            settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
            lang_UI = Lang_UI(settings)
        else:
            setup_module = importlib.import_module('protoc_polyglot.' + language + '.cli', package="protoc_polyglot")
            Lang_UI = getattr(setup_module, 'Lang_UI')
            settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
            lang_UI = Lang_UI(settings)
            
        if hasattr(lang_UI, function):
            fc = getattr(lang_UI, function)
            fc(*args)
        else:
            print(f"Function '{function}' not found in '{language}.cli'")
    except ModuleNotFoundError:
        print(f"Language '{language}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    Fire(execute)
