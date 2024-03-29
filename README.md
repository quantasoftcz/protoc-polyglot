## All-in-one Protocol Buffers compilation tool
### Supported languages:
Python, JavaScript, C++, Rust, Java, Go, ObjectiveC, PHP, Ruby, C#

### TODO:
Kotlin, Haskell, Perl, Lua, Swift [etc.](https://github.com/protocolbuffers/protobuf/blob/main/docs/third_party.md)

### Supported OS:
Ubuntu 22.04

### Supported architectures:
x86_64

### Getting started
1) Build prepared [docker image](docker/protoc-polyglot-x64.dockerfile)
2) `alias DOCKER_RUN='docker run --rm -v [output dir]:/data/output -v [output doc dir]:/data/doc -v [input protos dir]:/data/protos protoc-polyglot-x64:1.54.3'`
3) `DOCKER_RUN [command]`

### List of commands:
- List available languages and services: \
  `cli.py list`
- Compile a service: \
  `[language]/cli.py protoc [name]`
- Compile all services: \
  `[language]/cli.py protoc`

### Examples:
`alias DOCKER_RUN='docker run --rm -v $(pwd)/output:/data/output -v $(pwd)/doc:/data/doc -v $(pwd)/samples:/data/protos -v $(pwd)/tests:/data/tests protoc-polyglot-x64:1.54.3'`
- `DOCKER_RUN cli.py list`
- `DOCKER_RUN python/cli.py protoc bookclub`
- `DOCKER_RUN js/cli.py protoc`
- `DOCKER_RUN cli.py doc`
