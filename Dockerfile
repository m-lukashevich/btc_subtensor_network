FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install bittensor

RUN apt install --assume-yes  \
    make  \
    build-essential  \
    git  \
    clang  \
    curl  \
    libssl-dev  \
    llvm  \
    libudev-dev  \
    protobuf-compiler

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH"
# TODO: checkif cargo installed correctly by manually setting its path
#    source "$HOME/.cargo/env"

WORKDIR /app

RUN git clone https://github.com/opentensor/subtensor.git && \
    ls -lah

RUN echo "1"
# Adjust the PATH in order to let the bash know how to run cargo without reloading
ENV PATH="/root/.cargo/bin:${PATH}"

RUN echo $PATH && sleep 4

RUN ./subtensor/scripts/init.sh

WORKDIR /app/subtensor

RUN cargo build --release --features pow-faucet

#RUN BUILD_BINARY=0 ./scripts/localnet.sh

# TODO: this should be mounted to the container
WORKDIR /app

#RUN git clone https://github.com/opentensor/bittensor-subnet-template.git

#WORKDIR /app/bittensor-subnet-template

COPY bittensor-subnet-template/requirements.txt .

RUN python3 -m pip install -r ./requirements.txt

RUN echo "aa"
COPY docker_entrypoint.sh .
COPY init_subnet.sh .

WORKDIR /app/subtensor

ENTRYPOINT ["/app/docker_entrypoint.sh"]

#EXPOSE 5000

#ENTRYPOINT ["/app/docker_entrypoint.sh"]
