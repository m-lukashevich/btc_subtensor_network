import bittensor as bt

# miner
# hotkey = "0x32d97a987f84319912863b7d44abec3ec40d480e8dd5f62ab174d80bd0a46e16"
# validator
hotkey = "0xd4521f1120f013befe293e767b5eb1680067f59f99154a3a3ede1b7fc7385a14"


network = "ws://0.0.0.0:9946"
netuid = 1
sub = bt.subtensor(network)
mg = sub.metagraph(netuid)


# hotkeys registered in the subnetwork
# print(mg.hotkeys)


sub.is_hotkey_registered(hotkey)
