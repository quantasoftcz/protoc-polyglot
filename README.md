## All-in-one Protocol Buffers compilation tool
### Supported languages:
Python, JavaScript, C++, Rust, Java, Go, ObjectiveC, PHP, Ruby, C#

### Supported OS:
Ubuntu 22.04

### Supported architectures:
x86_64

## Getting started
First, install the Python package:
`pip install protoc-polyglot`

Then, run a command using this manual:

```bash
protoc-polyglot \
  -l [languages] [service-yml/directory/file] \
  -s [service name] \
  -d [directory input] \
  -f [files] \
  -o [output dir, default protoc-output -> default protoc-output/bookclub/python ...] \
  -c [connection ip+port]
```

Documentation is created automatically in the output folder after each compilation run.

### Examples
- `protoc-polyglot --languages python --service-yml samples/services.yml`
- `protoc-polyglot -l cpp python -y samples/services.yml`

### Optional: bulding Docker image locally
1) Build a [docker image](docker/protoc-polyglot-x64.dockerfile)
2) `alias DOCKER_RUN='docker run --rm -v [output dir]:/data/output -v [output doc dir]:/data/doc -v [input protos dir]:/data/protos protocpolyglot/protoc-polyglot'`
3) `DOCKER_RUN [command arguments]`

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
 

## TODO:
- Add more languages: Kotlin, Haskell, Perl, Lua, Swift [etc.](https://github.com/protocolbuffers/protobuf/blob/main/docs/third_party.md)
- Create web client
- Create CLI client