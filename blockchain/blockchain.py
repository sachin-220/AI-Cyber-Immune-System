import hashlib
import json
from datetime import datetime

class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': str(datetime.now()),
            'data': 'Genesis Block',
            'previous_hash': '0',
            'hash': self.calculate_hash(0, 'Genesis Block', '0')
        }
        self.chain.append(genesis_block)

    def calculate_hash(self, index, data, previous_hash):
        value = str(index) + str(data) + str(previous_hash) + str(datetime.now())
        return hashlib.sha256(value.encode()).hexdigest()

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = {
            'index': last_block['index'] + 1,
            'timestamp': str(datetime.now()),
            'data': data,
            'previous_hash': last_block['hash'],
            'hash': self.calculate_hash(last_block['index'] + 1, data, last_block['hash'])
        }
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current['hash'] != self.calculate_hash(current['index'], current['data'], current['previous_hash']):
                return False
            if current['previous_hash'] != previous['hash']:
                return False
        return True

# Usage example
if __name__ == "__main__":
    blockchain = SimpleBlockchain()
    
    # Add threat logs
    threat_data = {
        "event_type": "anomaly_detected",
        "severity": "high",
        "description": "Low trust score detected",
        "mitre_technique": "T1071",
        "stix_category": "network-traffic-analysis"
    }
    
    blockchain.add_block(json.dumps(threat_data))
    print("Blockchain valid:", blockchain.is_chain_valid())
    print("Latest block:", blockchain.chain[-1])