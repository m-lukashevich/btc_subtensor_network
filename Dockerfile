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

WORKDIR /app

RUN git clone https://github.com/opentensor/subtensor.git

# Adjust the PATH in order to let the bash know how to run cargo without reloading
ENV PATH="/root/.cargo/bin:${PATH}"

RUN ./subtensor/scripts/init.sh

WORKDIR /app/subtensor

RUN cargo build --release --features pow-faucet

WORKDIR /app

COPY bittensor-subnet-template/requirements.txt .

RUN python3 -m pip install -r ./requirements.txt

COPY docker_entrypoint.sh .
COPY init_subnet.sh .

ENTRYPOINT ["/app/docker_entrypoint.sh"]
