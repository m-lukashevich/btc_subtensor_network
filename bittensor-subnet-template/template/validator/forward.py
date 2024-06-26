# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 <Lukashevich Matvey>
import time
import json

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import bittensor as bt

from template.protocol import HashProtocol
from template.validator.reward import get_rewards
from template.utils.uids import get_random_uids


async def forward_hash(self):
    # time.sleep(1)
    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

    print("miner uids: ", miner_uids)

    blockchain_json = json.dumps(self.blockchain.to_dict(), indent=4)

    print(f"blockchain for sending to miners: {blockchain_json}")
    responses = await self.dendrite(
        # Send the query to selected miner axons in the network.
        axons=[self.metagraph.axons[uid] for uid in miner_uids],
        # Construct a dummy query. This simply contains a single integer.
        synapse=HashProtocol(blockchain_json=blockchain_json),
        # All responses have the deserialize function called on them before returning.
        # You are encouraged to define your own deserialization function.
        deserialize=False,
        timeout=30,
    )

    for response in responses:
        if response.dendrite.status_code != 200:
            print(f'Invalid request. Status code {response.dendrite.status_code}, message: {response.dendrite.status_message}')

    rewards = get_rewards(self, responses=responses, uids=miner_uids)

    self.update_scores(rewards, miner_uids)
