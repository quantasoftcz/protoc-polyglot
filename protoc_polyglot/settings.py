from os.path import join


class Settings:
    def __init__(self,
                 language,
                 plugins_base_path='/opt',
                 grpc_version="1.54.3",
                 protobuf_version="3.21.12",
                 DATA_DIR='/data',
                 CORE_DIR='/protoc-polyglot'):
        self.language = language

        self.plugins_base_path = plugins_base_path
        self.grpc_version = grpc_version
        self.protobuf_version = protobuf_version

        self.plugin_path_doc = f'{plugins_base_path}/doc/protoc-gen-doc'

        self.protobuf_folder = 'protobuf'
        self.grpc_folder = 'grpc'
        self.languages_that_have_external_plugin = ['go', 'java', 'js', 'rust']

        self.DATA_DIR = DATA_DIR
        self.CORE_DIR = CORE_DIR
        self.ROOT_PROTOS = join(DATA_DIR, 'protos')
        self.OUTPUT_ROOT = join(DATA_DIR, 'output')
        self.DOC_OUTPUT_DIR = join(self.OUTPUT_ROOT, 'doc')

        self.services_yaml = join(self.ROOT_PROTOS, 'services.yml')
