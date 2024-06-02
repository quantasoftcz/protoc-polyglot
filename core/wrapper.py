#!/usr/bin/python3
from fire import Fire
import importlib
from protoc_polyglot.core.cli import *

def execute(language:str="", function:str="", *args):
    try:
        setup_module = importlib.import_module(language + '.cli')
        Lang_UI = getattr(setup_module, 'Lang_UI')
        settings = Settings('plugins')
        lang_UI = Lang_UI(settings)
        
        if hasattr(lang_UI, function):
            fc = getattr(lang_UI, function)
            fc(*args)
        else:
            print(f"Function '{function}' not found in '{language}.cli'")
    except ModuleNotFoundError:
        print(f"Language '{language}' not found.")
    except AttributeError:
        print(f"Function '{function}' not found in '{language}.cli'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
Fire(execute)