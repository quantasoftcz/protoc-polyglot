
#python -m build .
#python3 -m build --wheel

# make sure to increase the "post" number: e.g. from 0.0.1-1 to 0.0.1-2

rm -rf ./dist
hatch build
twine upload -p $PYPI_KEY dist/*

#ppackage/protobuf/bin/protoc -I ./samples --plugin=protoc-gen-grpc=ppackage/grpc/grpc_python_plugin --grpc_out=./output/python/bookclub --python_out=./output/python/bookclub bookclub/book.proto bookclub/member.proto bookclub/bookclub.proto

pip install protoc-polyglot --upgrade
pip install protoc-polyglot --upgrade