from cryptos import Bitcoin, sha256
from icecream import ic
import random
import math

def perturb_key(key):
    key_bytes = bytearray.fromhex(key)
    index = random.randint(0, len(key_bytes) - 1)
    key_bytes[index] ^= 1 << random.randint(0, 7)
    return key_bytes.hex()

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) / temperature)

def calculate_cost(address, target):
    return sum(1 for a, b in zip(address, target) if a != b)

def simulated_annealing(target, initial_key, initial_temp, cooling_rate):
    def new_rand(key):
        key = perturb_key(key)
        priv = sha256(key)
        pub = c.privtopub(priv)
        addr = c.pubtoaddr(pub)

        return key, priv, pub, addr

    c = Bitcoin(testnet=True)

    temperature = initial_temp

    old_key, old_priv, old_pub, old_addr = new_rand(initial_key)
    old_cost = calculate_cost(old_addr, target)
    
    iteration = 0
    try:
        while True:
            iteration += 1
            if iteration % 1000 == 0:
                ic(iteration)
            new_key, new_priv, new_pub, new_addr = new_rand(old_key)
            new_cost = calculate_cost(new_addr, target)
            
            if acceptance_probability(old_cost, new_cost, temperature) > random.random():
                old_key, old_priv, old_pub, old_addr = new_rand(new_key)
                old_cost = new_cost
            
            temperature *= cooling_rate
            
            if new_addr == target:
                return new_key, new_priv, new_pub, new_addr, iteration
    except Exception as e:
        ic(e)
        return old_key, old_priv, old_pub, old_addr, iteration
    
if __name__ == '__main__':
    target = 'mscAn4dWmwJkuAR5gDmdXSYS3ampxHC4Ct'
    initial_key = sha256(target)
    initial_temp = 100.0
    cooling_rate = 0.99

    key, priv, pub, addr, iteration = simulated_annealing(target, initial_key, initial_temp, cooling_rate)
    
    ic(key, priv, pub, addr, iteration)