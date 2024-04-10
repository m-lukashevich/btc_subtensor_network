# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>
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

import torch
from typing import List

from hash_system.blockchain import Blockchain


def _validate_created_block(blockchain: Blockchain, new_blockchain: Blockchain, uid):
    new_block = new_blockchain.get_latest_block()
    if not blockchain.is_new_block_valid(new_block):
        return 0

    # NOTE: add new block to blockchain if it passed the validation
    print(f"new block added by {uid}")
    blockchain.chain.append(new_block)
    return 1


def get_rewards(
    self,
    responses: List[dict],
    uids
) -> torch.FloatTensor:
    """
    Returns a tensor of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[float]): A list of responses from the miner.

    Returns:
    - torch.FloatTensor: A tensor of rewards for the given query and responses.
    """

    weights = []
    for response, uid in zip(responses, uids):
        weight = 0
        if response.dendrite.status_code == 200:
            new_blockchain = Blockchain.from_dict(json.loads(response.blockchain_json))
            weight = _validate_created_block(self.blockchain, new_blockchain, uid)
        weights.append(weight)

    # Get all the reward results by iteratively calling your reward() function.
    return torch.FloatTensor(weights).to(self.device)
