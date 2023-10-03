### Compile Protocol Buffers files into any of these languages
Supported languages:
- Python

Requires fixing:
- JavaScript
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
1) `alias DOCKER_RUN='docker run -it --rm -v [real path to protoc-polygot/core dir]:/workspace -v [path to proto files]$(pwd):/data protoc_polyglot_x64:1.54.3'`
2) `DOCKER_RUN [command]`

#### List of commands:
- List available services: \
  `./cli.py protoc`
- Compile services: \
  `./[language]/cli.py protoc [name]` \
  `./[language]/cli.py protoc *`

#### Examples:
`DOCKER_RUN python3 cli.py protoc` \
`DOCKER_RUN python3 python/cli.py protoc first-service`