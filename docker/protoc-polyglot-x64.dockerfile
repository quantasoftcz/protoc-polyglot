# build: docker build -t protoc-polyglot-x64:1.54.3 -f protoc-polyglot-x64.dockerfile ..
# peek: docker run --rm -v $(pwd)/core:/core -v $(pwd)/output:/data/output -v $(pwd)/samples:/data/protos protoc-polyglot-x64:1.54.3 bash
FROM ubuntu:22.04


ARG CMAKE_VERSION=3.27.6
RUN apt update &&\
    apt install -y git wget g++ build-essential python3-dev python3-pip &&\
    pip install fire cmake==${CMAKE_VERSION}

WORKDIR /opt

# grpc
ARG CONAN_VERSION=2.0.10
ARG GRPC_VERSION=1.54.3
ARG PROTOBUF_VERSION=3.21.12
RUN pip install conan==${CONAN_VERSION} &&\
    conan profile detect &&\
    conan install --requires protobuf/${PROTOBUF_VERSION} -b=missing -of protobuf --deployer direct_deploy -r conancenter &&\
    conan install --requires grpc/${GRPC_VERSION} -b=missing -of grpc --deployer direct_deploy -r conancenter &&\
    mv grpc build; mv build/direct_deploy/grpc .; rm -rf build &&\
    mv protobuf build; mv build/direct_deploy/protobuf .; rm -rf build &&\
    rm -rf /root/.conan2 &&\
    rm -rf /opt/protobuf/lib &&\
    rm -rf /opt/grpc/lib &&\
    ln -s /opt/protobuf/bin/protoc /usr/bin/protoc &&\
    ln -s /opt/grpc/bin/grpc_python_plugin /usr/bin/grpc_python_plugin &&\
    ln -s /opt/grpc/bin/grpc_csharp_plugin /usr/bin/grpc_csharp_plugin &&\
    ln -s /opt/grpc/bin/grpc_cpp_plugin /usr/bin/grpc_cpp_plugin
# location: /opt/protobuf /opt/grpc

# protoc java
ARG PROTOC_JAVA_VER=1.58.0
RUN mkdir java; cd java &&\
    wget https://repo1.maven.org/maven2/io/grpc/protoc-gen-grpc-java/${PROTOC_JAVA_VER}/protoc-gen-grpc-java-${PROTOC_JAVA_VER}-linux-x86_64.exe &&\
    mv protoc-gen-grpc-java-${PROTOC_JAVA_VER}-linux-x86_64.exe protoc-gen-grpc-java &&\
    chmod +x protoc-gen-grpc-java &&\
    ln -s /opt/java/protoc-gen-grpc-java /usr/bin/protoc-gen-grpc-java
# location: /opt/java

# protoc javascript
# https://github.com/grpc/grpc-web/issues/1251
ARG PROTOC_GRPC_JS_VER=1.4.1
ARG PROTOC_PB_JS_VER=3.21.2
RUN mkdir js; cd js &&\
    wget https://github.com/protocolbuffers/protobuf-javascript/releases/download/v${PROTOC_PB_JS_VER}/protobuf-javascript-3.21.2-linux-x86_64.tar.gz &&\
    tar -xzvf protobuf-javascript-3.21.2-linux-x86_64.tar.gz &&\
    rm protobuf-javascript-3.21.2-linux-x86_64.tar.gz &&\
    wget https://github.com/grpc/grpc-web/releases/download/${PROTOC_GRPC_JS_VER}/protoc-gen-grpc-web-${PROTOC_GRPC_JS_VER}-linux-x86_64 &&\
    chmod +x protoc-gen-grpc-web-${PROTOC_GRPC_JS_VER}-linux-x86_64 &&\
    ln -s /opt/js/protoc-gen-grpc-web-${PROTOC_GRPC_JS_VER}-linux-x86_64 /usr/bin/protoc-gen-grpc-web &&\
    ln -s /opt/js/bin/protoc-gen-js /usr/bin/protoc-gen-js
# location: /opt/js

## protoc-gen-doc
ARG PROTOC_GEN_DOC=1.5.1
RUN mkdir doc; cd doc &&\
    wget https://github.com/pseudomuto/protoc-gen-doc/releases/download/v${PROTOC_GEN_DOC}/protoc-gen-doc_${PROTOC_GEN_DOC}_linux_amd64.tar.gz &&\
    tar -xvf protoc-gen-doc_${PROTOC_GEN_DOC}_linux_amd64.tar.gz &&\
    rm protoc-gen-doc_${PROTOC_GEN_DOC}_linux_amd64.tar.gz &&\
    ln -s /opt/doc/protoc-gen-doc /usr/bin/protoc-gen-doc
# location: /opt/doc

# rust
# https://github.com/tafia/quick-protobuf
RUN mkdir rust; cd rust &&\
    apt -y install cargo &&\
    cargo install protobuf-codegen &&\
    cp /root/.cargo/bin/protoc-gen-rust /opt/rust/protoc-gen-rust &&\
    cargo uninstall protobuf-codegen &&\
    ln -s /opt/rust/protoc-gen-rust /usr/bin/protoc-gen-rust &&\
    apt purge cargo -y &&\
    rm -rf /root/.cargo &&\
    apt autoremove -y
# location: /opt/rust

# go
RUN mkdir go; cd go &&\
    apt install -y golang-go &&\
    go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28 &&\
    go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2 &&\
    cp /root/go/bin/protoc-gen-go . &&\
    cp /root/go/bin/protoc-gen-go-grpc . &&\
    apt purge -y golang-go &&\
    apt autoremove -y &&\
    rm -rf /root/go &&\
    ln -s /opt/go/protoc-gen-go /usr/bin/protoc-gen-go &&\
    ln -s /opt/go/protoc-gen-go-grpc /usr/bin/protoc-gen-go-grpc
# location: /opt/go


ENV PATH="$PATH:/root/go/bin:/core"

COPY core /core

WORKDIR /core