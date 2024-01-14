# build: docker build -t protoc-polyglot-server-x64:1.54.3 -f protoc-polyglot-server-x64.dockerfile .
# run: docker run -it --rm -p 8000:8000 -v [path to protoc-polyglot]:/workspace protoc-polyglot-server-x64:1.54.3
ARG base_image_tag=1.54.3
FROM protoc-polyglot-x64:$base_image_tag

# setup envirnment
WORKDIR /env
COPY api-server/requierements.txt .
RUN pip install -r requierements.txt

# set alias for frequent commands
RUN echo 'alias p=python3' >> ~/.bashrc

WORKDIR /workspace