import bittensor as bt
import asyncio

from template.api.dummy import DummyAPI, HashAPI

wallet = bt.wallet(name="miner", hotkey="default")
# metagraph = bt.metagraph(netuid=21)

# validator
hotkey = "0xd4521f1120f013befe293e767b5eb1680067f59f99154a3a3ede1b7fc7385a14"


network = "ws://0.0.0.0:9946"
netuid = 1
sub = bt.subtensor(network)
metagraph = sub.metagraph(netuid)


# Miner axon
axons_miner = [metagraph.axons[0]]

api_call = HashAPI(wallet=wallet)
# api_call.query_api(axons=axons_validator, dummy_input=6)


async def a(api_call):
    return await api_call.query_api(axons=axons_miner, deserialize=True, timeout=30, dummy_input=6)

r = asyncio.run(a(api_call))

