FROM ubuntu:20.04

LABEL org.opencontainers.image.authors="noslate-support@@list.alibaba-inc.com" \
      org.opencontainers.image.source="https://github.com/noslate-project/build" \
      org.opencontainers.image.licenses="MIT"

ARG LLVM_VERSION=12

RUN apt-get update && \
    # MARK: - Common build tools
    # python for node-gyp
    # python3 for node configure
    apt-get install -y git make python python3 python3-pip ninja-build curl sudo && \
    # MARK: gn
    DEBIAN_FRONTEND=noninteractive apt-get install -y pkg-config vim && \
    # MARK: turf dependencies
    apt-get install -y xxd && \
    # MARK: - LLVM
    DEBIAN_FRONTEND=noninteractive \
      apt-get install -y lsb-release wget software-properties-common && \
    wget https://apt.llvm.org/llvm.sh && \
    chmod +x llvm.sh && \
    ./llvm.sh $LLVM_VERSION && \
    rm llvm.sh && \
    ln -s /usr/bin/clang-12 /usr/bin/clang && \
    ln -s /usr/bin/clang++-12 /usr/bin/clang++ && \
    ln -s /usr/bin/lldb-12 /usr/bin/lldb && \
    # MARK: - Repo
    curl -sLo /usr/bin/repo https://storage.googleapis.com/git-repo-downloads/repo && \
    chmod +x /usr/bin/repo && \
    # MARK: cleanup
    apt-get clean

ENV CC=clang CXX=clang++ LINK=clang++
