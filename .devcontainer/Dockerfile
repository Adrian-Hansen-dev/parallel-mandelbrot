FROM mcr.microsoft.com/devcontainers/cpp:ubuntu-22.04

# Install OpenMP library
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libomp-dev