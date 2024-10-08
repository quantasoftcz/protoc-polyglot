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
2) `alias DOCKER_RUN='docker run --rm -v [output dir]:/data/output -v [output doc dir]:/data/doc -v [input protos dir]:/data/protos protocpolyglot/protoc-polyglot'`
3) `DOCKER_RUN [command]`

### List of commands:
- Compile all services: \
  `cli.py -l [languages] -y [path to services yml]`

Documentation is create in the output folder after any compilation run.

### Examples:
`alias DOCKER_RUN='docker run --rm -v $(pwd)/output:/data/output -v $(pwd)/doc:/data/doc -v $(pwd)/samples:/data/protos -v $(pwd)/tests:/data/tests protocpolyglot/protoc-polyglot'`
- `DOCKER_RUN cli.py --languages python --service-yml /data/protos/services.yml`
- `DOCKER_RUN cli.py -l cpp python -y /data/protos/services.yml`

## Contribution

We love that you are interested in helping us with the development of the protoc-polyglot project.
To make the process of contributing as simple as possible we have created a couple of guidelines on how to contribute.

### Issue tracking and solving

We track every issue in [YouTrack](https://protopolyglot.youtrack.cloud/dashboard). Before solving any bug, make sure it's
reported in [YouTrack](https://protopolyglot.youtrack.cloud/dashboard) and not already solved.

**Make sure to solve only one issue at a time.**

### Fork & Pull Request

1. Create a fork of this repository
2. Clone your fork to your computer
3. Create a new branch in the forked repository from the base branch `dev` with a meaningful name
4. Solve the issue
5. Push your changes to the Fork repository.
6. Create a Pull Request from your branch to the `dev` branch
 ( GitHub documentation about Pull Requests: https://help.github.com/articles/using-pull-requests)

The Pull Request should have a meaningful title, information about the changes you have made,
and a link to the issue in [YouTrack](https://protopolyglot.youtrack.cloud/dashboard).

Do not add unnecessary files, and make sure not to push any sensitive personal information.

 ```Protoc-polyglot team - protoc-polyglot@proton.me```
 

### Supported commands

protoc-polyglot python protoc

protoc-polyglot -l [languages] [service-yml/directory/file] 
  -s [service name]
  -d [directory input]
  -f [files]
  -o [output dir, default protoc-output -> default protoc-output/bookclub/python ...]
  -c [connection ip+port]

protoc-polyglot list

protoc-polyglot python file.yml