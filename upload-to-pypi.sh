
python3 -m pip install -e .
python -m build .
python3 -m build --wheel

twine upload dist/*


ppackage/protobuf/bin/protoc -I ./samples --plugin=protoc-gen-grpc=ppackage/grpc/grpc_python_plugin --grpc_out=./output/python/bookclub --python_out=./output/python/bookclub bookclub/book.proto bookclub/member.proto bookclub/bookclub.proto
