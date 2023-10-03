# build: docker build -t protoc-polyglot-x64:1.54.3 -f protoc-polyglotx64.dockerfile .
FROM ubuntu:22.04

RUN apt update &&\
    apt install -y git wget g++ build-essential python3-dev python3-pip &&\
    pip install -U fire

# cmake
RUN pip install -U cmake

ARG GRPC_VERSION=1.54.3
ARG PROTOBUF_VERSION=3.21.12
ARG CONAN_VERSION=2.0.10

# Conan
RUN pip install -U conan==${CONAN_VERSION} &&\
    conan profile detect

# grpc
WORKDIR /opt
RUN conan install --requires grpc/${GRPC_VERSION} -b=missing -of grpc --deployer direct_deploy -r conancenter &&\
    conan install --requires protobuf/${PROTOBUF_VERSION} -b=missing -of protobuf --deployer direct_deploy -r conancenter &&\
    mv grpc build; mv build/direct_deploy/grpc .; rm -rf build &&\
    mv protobuf build; mv build/direct_deploy/protobuf .; rm -rf build &&\
    ln -s /opt/protobuf/bin/protoc /usr/bin/protoc &&\
    ln -s /opt/grpc/bin/grpc_python_plugin /usr/bin/grpc_python_plugin &&\
    ln -s /opt/grpc/bin/grpc_csharp_plugin /usr/bin/grpc_csharp_plugin &&\
    ln -s /opt/grpc/bin/grpc_cpp_plugin /usr/bin/grpc_cpp_plugin

ARG PROTOC_JAVA_VER=1.58.0
ARG PROTOC_JS_VER=1.4.1
ARG PROTOC_GEN_DOC=1.5.1

# protoc java
RUN wget https://repo1.maven.org/maven2/io/grpc/protoc-gen-grpc-java/${PROTOC_JAVA_VER}/protoc-gen-grpc-java-${PROTOC_JAVA_VER}-linux-x86_64.exe &&\
    chmod +x protoc-gen-grpc-java-${PROTOC_JAVA_VER}-linux-x86_64.exe &&\
    ln -s /opt/protoc-gen-grpc-java-${PROTOC_JAVA_VER}-linux-x86_64.exe /usr/bin/protoc-gen-grpc-java

# protoc javascript
RUN wget https://github.com/grpc/grpc-web/releases/download/${PROTOC_JS_VER}/protoc-gen-grpc-web-${PROTOC_JS_VER}-linux-x86_64 &&\
    chmod +x protoc-gen-grpc-web-${PROTOC_JS_VER}-linux-x86_64 &&\
    ln -s /opt/protoc-gen-grpc-web-${PROTOC_JS_VER}-linux-x86_64 /usr/bin/protoc-gen-grpc-web &&\
    apt install npm -y &&\
    npm install -g protoc-gen-js

# protoc-gen-doc
RUN wget https://github.com/pseudomuto/protoc-gen-doc/releases/download/v${PROTOC_GEN_DOC}/protoc-gen-doc_${PROTOC_GEN_DOC}_linux_amd64.tar.gz &&\
    mkdir protoc-gen-doc &&\
    tar -xvf protoc-gen-doc_${PROTOC_GEN_DOC}_linux_amd64.tar.gz --directory protoc-gen-doc &&\
    mv protoc-gen-doc/protoc-gen-doc /usr/bin/

# dotnet
ENV DEBIAN_FRONTEND=noninteractive
RUN wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb &&\
    dpkg -i packages-microsoft-prod.deb &&\
    apt-get install -y apt-transport-https &&\
    apt-get update &&\
    apt-get install -y dotnet-sdk-7.0

WORKDIR /workspace