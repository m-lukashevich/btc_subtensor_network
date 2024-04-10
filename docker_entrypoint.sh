#!/bin/sh

echo "starting"
cd ./subtensor
BUILD_BINARY=0 exec "./scripts/localnet.sh" &&
echo "started"