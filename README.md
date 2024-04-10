# **BTC-like Bittensor Subnet**


Important: the difficulty of calculating the hash is indicated in the blockchain class; for ease of testing, it is set to 5. On my PC, one block takes 2-4 seconds. To increase the counting speed, you need to lower this value.

```python
class Blockchain:
     def __init__(self):
         self.sync_chain()
         self.difficulty = 5
```


The subnet is built on the basis of the repository https://github.com/opentensor/bittensor-subnet-template (main branch). The subnet implements the mechanism of the Bitcoin network, but with adaptations to the Bittensor philosophy. A separate State has been created for storing the Bitcoin blockchain, which is initialized when the validator starts and is transferred to the miners. The validator's job is to send the work of generating blocks to the miners. As soon as one of the miners calculates the required hash for a block, he will send it to the validator for validation and, if successful, will be recorded as a new block in the blockchain. After this, the validator updates the blockchain to the miners and sends them a new task to count the block. The entire reward for the block goes to the Miner who was the first to generate a valid hash.
<br/>
Added Docker-compose for local testing. To build and launch a subnet you need:
1. Build the `docker-compose build` image
2. Run the `docker-compose up` container
3. Open a new terminal and go into the container to start initializing the subnet: `docker exec -it bittensor_subnet bash`
4. Inside the container, execute `./init_subnet.sh` This command will start the creation of owner, miner, miner2, validator wallets. Then he will replenish the wallets. Then it will create a subnet and register miners and validators in it. <br/><br/> **IMPORTANT**: the subnet has a restriction on registering new parts. For example, when starting for the first time, you need to wait until the first tempo has passed (360 blocks will be generated) in order to register the second and third nodes (validator and miner2). <br/> <br/> **IMPORTANT**: subnet boosting can also be done after the first tempo. I specified these restrictions in `init_subnet.sh`. Therefore, if errors appear in it, you must wait until the end of the tempo and manually execute the remaining commands.
5. Once manners and validators are registered in the subnet, you can launch them. To run the validator in a new terminal, go inside the container (`docker exec -it bittensor_subnet bash`) and run the command `python3 neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --wallet.name validator --wallet.hotkey default --logging.debug`
6. To launch the first miner in a new terminal, go inside the container (`docker exec -it bittensor_subnet bash`) and run the command `python3 neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor .network local --wallet.name miner --wallet.hotkey default --logging.debug This will launch the first miner on port 8091`
7. To launch the second miner in a new terminal, go to the container and run the command `python3 neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --wallet.name miner2 --wallet.hotkey default --logging.debug --axon.port 8092` <br/> The difference with the first miner here is the port. The second liner will operate on port *8092*
8. Done, now the miners generate new blocks, and the validator rewards the miners for this and adds new blocks to the blockchain.


Example of work:

Validator logs. At startup we see a blockchain with one block (Genesis Block). The validator then distributed the work of calculating the hash to the validators ([0, 2, 1]). The miner with uid 0 (new block added by 0) calculated the block first. After validation, the block was added to the blockchain and a new bock calculation task was sent to the miners.



```bash
miner uids: tensor([0, 1, 2])
blockchain for sending to miners: {
     "chain": [
         {
             "index": 0,
             "timestamp": "2024-04-09 20:26:58.854760",
             "data": "Genesis Block",
             "previous_hash": "0",
             "nonce": 0,
             "hash": "2df188a10c2960db39293d1261a06c51a5680e7b61724ab663ad33c7aeeb3a77"
         }
     ],
     "difficulty": 5
}
Invalid request. Status code 401, message: Not Verified with error: Signature mismatch with 1712694420209826886.5Ck9vwTTZcfGStiPH32aUR334gsQcMaTMyL7hYK42vKXcx1L.5E51AFzWDh1Gi27mok4rZdJqcZjwaQdMmJfBtw4WrPy4qj FX.83a05d60-f6af-11ee-bebe-0242ac120002.a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a and 0xc6ffcb8ae594e26302d7a444abeb79bba 2d6489670bdb2092699d243edaa5270aa7179efff5b29d63e7712336081b8ed702ed998156641765f164c972b42a187
Invalid request. Status code 503, message: Service at 37.45.217.199:8092/HashProtocol unavailable.
new block added by 0
miner uids: tensor([0, 1, 2])
blockchain for sending to miners: {
     "chain": [
         {
             "index": 0,
             "timestamp": "2024-04-09 20:26:58.854760",
             "data": "Genesis Block",
             "previous_hash": "0",
             "nonce": 0,
             "hash": "2df188a10c2960db39293d1261a06c51a5680e7b61724ab663ad33c7aeeb3a77"
         },
         {
             "index": 1,
             "timestamp":"2024-04-09 20:27:00.243683",
             "data": "Natasha Hernandez",
             "previous_hash": "2df188a10c2960db39293d1261a06c51a5680e7b61724ab663ad33c7aeeb3a77",
             "nonce": 46634,
             "hash": "000000216ccfe1b4dab82acbb03a7370334a95eba24fccfbc8f785763518705c"
         }
     ],
     "difficulty": 5
}
```

Miner logs:

The miner logs the initial state of the blockchain. After calculating a new block, it also writes it to the logs. Doping to simplify testing.
```bash
Received blockchain: {
     "chain": [
         {
             "index": 0,
             "timestamp": "2024-04-09 20:26:58.854760",
             "data": "Genesis Block",
             "previous_hash": "0",
             "nonce": 0,
             "hash": "2df188a10c2960db39293d1261a06c51a5680e7b61724ab663ad33c7aeeb3a77"
         }
     ],
     "difficulty": 5
}
2024-04-09 20:27:00.242 | WARNING | - save_state() not implemented for this neuron. You can implement this function to save model checkpoints or other useful data. -
New Blockchain: {
     "chain": [
         {
             "index": 0,
             "timestamp": "2024-04-09 20:26:58.854760",
             "data": "Genesis Block",
             "previous_hash": "0",
             "nonce": 0,
             "hash": "2df188a10c2960db39293d1261a06c51a5680e7b61724ab663ad33c7aeeb3a77"
         },
         {
             "index": 1,
             "timestamp": "2024-04-09 20:27:00.243683",
             "data": "Natasha Hernandez",
             "previous_hash": "2df188a10c2960db39293d1261a06c51a5680e7b61724ab663ad33c7aeeb3a77",
             "nonce": 46634,
             "hash": "000000216ccfe1b4dab82acbb03a7370334a95eba24fccfbc8f785763518705c"
         }
     ],
     "difficulty": 5
}
```

For calculating a block in a mainer, a reward is awarded. Upon completion of the tempo (360 blocks) - the reward is poured into wallets: 
```bash

                                                                       Wallet - miner:5ECWGqBqwnX86DgH1qBz4XSFGXeYMwTWV15zhikYew3ZdXxZ
Subnet: 1
COLDKEY HOTKEY UID ACTIVE STAKE(τ) RANK TRUST CONSENSUS INCENTIVE DIVIDENDS EMISSION(ρ) VTRUST VPERMIT UPDATED AXON HOTKEY_SS58
miner default 0 True 260.76146 0.49999 1.00000 0.49999 0.49999 0.00000 205_001_144 0.00000 * 1779 37.45.217.199:8091 5E51AFzWDh1Gi27mok4rZdJqc ZjwaQdMmJfBtw4WrPy4qjFX
1 1 1 τ260.76146 0.49999 1.00000 0.49999 0.49999 0.00000 ρ205_001_144 0.00000
                                                                                           Wallet balance: τ299.0
```

```bash

                                                                      Wallet - validator:5HintTeqHKTewce31GEbd6VfVF52Aynsh3LsA8wtgGnbXQyc
Subnet: 0
COLDKEY HOTKEY UID ACTIVE STAKE(τ) RANK TRUST CONSENSUS INCENTIVE DIVIDENDS EMISSION(ρ) VTRUST VPERMIT UPDATED AXON HOTKEY_SS58
validator default 0 True 707.77228 0.00000 0.00000 0.00000 0.00000 0.00000 0 0.00000 1066 none 5Ck9vwTTZcfGStiPH32aUR334gsQcMaTMyL7hYK42vKXcx1L
                     1 0.00000 0.00000 0.00000 0.00000 0.00000 ρ0 0.00000
Subnet: 1
COLDKEY HOTKEY UID ACTIVE STAKE(τ) RANK TRUST CONSENSUS INCENTIVE DIVIDENDS EMISSION(ρ) VTRUST VPERMIT UPDATED AXON HOTKEY_SS58
validator default 1 True 707.77228 0.00000 0.00000 0.00000 0.00000 1.00000 410_002_288 1.00000 * 73 37.45.217.199:8091 5Ck9vwTTZcfGStiPH32aUR334gsQcMa TMyL7hYK42vKXcx1L
2 2 2 τ707.77228 0.00000 0.00000 0.00000 0.00000 1.00000 ρ410_002_288 1.00000
                                                                                            Wallet balance: τ1e-06
```