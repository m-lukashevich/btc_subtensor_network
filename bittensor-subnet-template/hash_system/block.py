import hashlib
import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(d):
        block = Block(
            d['index'],
            datetime.datetime.strptime(d['timestamp'], "%Y-%m-%d %H:%M:%S.%f"),
            d['data'],
            d['previous_hash']
        )
        block.nonce = d['nonce']
        block.hash = d['hash']
        return block
