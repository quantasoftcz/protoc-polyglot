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
2) `alias DOCKER_RUN='docker run -it --rm -v $(pwd):/workspace -v $(pwd)/output:/data/output -v [path to protos]:/data protoc-polyglot-x64:1.54.3'`
3) `DOCKER_RUN [command]`

#### List of commands:
- List available services: \
  `./cli.py protoc`
- Compile services: \
  `./[language]/cli.py protoc [name]` \
  `./[language]/cli.py protoc *`

#### Examples:
`alias DOCKER_RUN='docker run -it --rm -v $(pwd)/tools:/workspace -v $(pwd)/output:/data/output -v $(pwd)/protos:/data/protos protoc-polyglot-x64:1.54.3'`
- `DOCKER_RUN ./cli.py protoc`
- `DOCKER_RUN ./python/cli.py protoc bookclub`
- `DOCKER_RUN ./js/cli.py protoc \*`