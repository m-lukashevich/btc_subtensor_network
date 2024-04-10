import datetime

from hash_system.block import Block


class Blockchain:
    def __init__(self):
        self.sync_chain()
        self.difficulty = 4

    def sync_chain(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_new_block_valid(self, block):
        if block.index != len(self.chain):
            # print('wrong index')
            return False
        if block.hash != block.calculate_hash():
            # print('wrong hash')
            return False
        if block.index > 0 and block.previous_hash != self.chain[block.index - 1].hash:
            # print('wrong prev hash')
            return False
        return True

    def to_dict(self):
        return {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty
        }

    @staticmethod
    def from_dict(d):
        blockchain = Blockchain()
        blockchain.chain = [Block.from_dict(block_dict) for block_dict in d['chain']]
        blockchain.difficulty = d['difficulty']
        return blockchain

