FROM ubuntu:14.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    mongodb-clients \
    openssh-server \
    && \
    apt-get clean

RUN locale-gen en_US.UTF-8