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
1) Build docker image in `docker` folder
2) `alias DOCKER_RUN='docker run -it --rm -v [real path to protoc-polygot/core-tools dir]:/workspace -v [path to proto files]$(pwd):/data protoc-polyglot-x64:1.54.3'`
3) `DOCKER_RUN [command]`

#### List of commands:
- List available services: \
  `python3 cli.py protoc`
- Compile services: \
  `python3 [language]/cli.py protoc [name]` \
  `python3 [language]/cli.py protoc *`

#### Examples:
`alias DOCKER_RUN='docker run -it --rm -v [real path to protoc-polygot/core-tools dir]:/workspace -v [path to proto files]$(pwd):/data protoc-polyglot-x64:1.54.3'`
- `DOCKER_RUN python3 cli.py protoc`
- `DOCKER_RUN python3 python/cli.py protoc bookclub`
- `DOCKER_RUN python3 js/cli.py protoc \*`
