import os, sys, importlib

from os.path import abspath, dirname
from enum import Enum

from protoc_polyglot.settings import Settings
from protoc_polyglot.common_interface import CommonInterface

class RunMode(Enum):
    DOCKER = 1
    PYPI = 2

# import of core is different based on whether we run in PyPi package or in Docker
run_mode = RunMode.DOCKER if os.path.abspath(__file__) == '/protoc_polyglot/cli.py' else RunMode.PYPI

if run_mode == RunMode.DOCKER:
    sys.path.append('/')


def get_language_interface(language: str) -> CommonInterface:
    if run_mode == RunMode.PYPI:
        setup_module = importlib.import_module('protoc_polyglot.' + language + '.language_interface',
                                               package="protoc-polyglot")
        language_interface_class = getattr(setup_module, 'LanguageInterface')
        settings = Settings('plugins', DATA_DIR='', CORE_DIR=dirname(abspath(__file__)))
        language_interface = language_interface_class(settings)
    else:
        module_dir = os.path.join(os.path.dirname(__file__), language)

        sys.path.insert(0, module_dir)

        module_path = os.path.join(module_dir, 'language_interface.py')

        spec = importlib.util.spec_from_file_location('cli', module_path)
        setup_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup_module)

        language_interface_class = getattr(setup_module, 'LanguageInterface')
        settings = Settings(language)
        language_interface = language_interface_class(settings)

        sys.path.pop(0)
    return language_interface