#!/bin/sh

echo "creating owner wallet..."
btcli wallet new_coldkey --no_password --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating miner wallet..."
btcli wallet new_coldkey --no_password --wallet.name miner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet new_hotkey --no_password --wallet.name miner --wallet.hotkey default --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating miner2 wallet..."
btcli wallet new_coldkey --no_password --wallet.name miner2 --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet new_hotkey --no_password --wallet.name miner2 --wallet.hotkey default --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating validator wallet..."
btcli wallet new_coldkey --no_password --wallet.name validator --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet new_hotkey --no_password --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "minting tokens for owner..."
btcli wallet faucet --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet faucet --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet faucet --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet faucet --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "minting tokens for miner..."
btcli wallet faucet --wallet.name miner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "minting tokens for miner2..."
btcli wallet faucet --wallet.name miner2 --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "minting tokens for validator..."
btcli wallet faucet --wallet.name validator --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating subnet..."
btcli subnet create --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "registering miner in subnet..."
btcli subnet register --wallet.name miner --wallet.hotkey default --netuid 1 --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "registering validator in subnet..."
# NOTE: it can be registered only after the first tempo is complete because of the subnetwork limitations
btcli subnet register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "registering 2nd miner in subnet..."
btcli subnet register --wallet.name miner2 --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "Staking validator ..."
btcli stake add --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "registering validator in the root subnet..."
btcli root register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "boosting subnet..."
# NOTE: it can be successfully applied after blockchain works for a while
btcli root boost --netuid 1 --increase 1 --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt
