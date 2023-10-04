### Compile Protocol Buffers files into any of these languages
Supported languages:
- Python
- JavaScript

Requires fixing:
- C++
- Java
- C#

TODO:
- Rust
- Go
- PHP
- Ruby
- ObjectiveC

### Getting started
1) Build prepared [docker image](docker/protoc-polyglot-x64.dockerfile)
2) `alias DOCKER_RUN='docker run -it --rm -v [real path to protoc-polygot/core-tools dir]:/workspace -v [path to proto files]$(pwd):/data protoc-polyglot-x64:1.54.3'`
3) `DOCKER_RUN [command]`

#### List of commands:
- List available services: \
  `./cli.py protoc`
- Compile services: \
  `./[language]/cli.py protoc [name]` \
  `./[language]/cli.py protoc *`

#### Examples:
`alias DOCKER_RUN='docker run -it --rm -v /home/ubuntu/protoc-polyglot/core-tools:/workspace -v $(pwd):/data protoc-polyglot-x64:1.54.3'`
- `DOCKER_RUN ./cli.py protoc`
- `DOCKER_RUN ./python/cli.py protoc bookclub`
- `DOCKER_RUN ./js/cli.py protoc \*`
