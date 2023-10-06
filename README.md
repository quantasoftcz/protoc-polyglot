### Compile Protocol Buffers files into any of these languages
Supported languages: \
Python, JavaScript, C++, Rust, Java, Go

TODO: \
C#, PHP, Ruby, ObjectiveC

### Getting started
1) Build prepared [docker image](docker/protoc-polyglot-x64.dockerfile)
2) `alias DOCKER_RUN='docker run -it --rm -v $(pwd)/core:/core -v [output dir]:/data/output -v [input protos dir]:/data/protos protoc-polyglot-x64:1.54.3'`
3) `DOCKER_RUN [command]`

#### List of commands:
- List available services: \
  `./cli.py protoc`
- Compile services: \
  `./[language]/cli.py protoc [name]` \
  `./[language]/cli.py protoc *`

#### Examples:
`alias DOCKER_RUN='docker run -it --rm -v $(pwd)/core:/core -v $(pwd)/output:/data/output -v $(pwd)/samples:/data/protos protoc-polyglot-x64:1.54.3'`
- `DOCKER_RUN ./cli.py protoc`
- `DOCKER_RUN ./python/cli.py protoc bookclub`
- `DOCKER_RUN ./js/cli.py protoc \*`
