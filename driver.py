from treeParityMachine import tpm
import cryptography
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

N = 101      # Number of input neurons per hidden neuron
K = 2        # Number of neurons in hidden layer
L = 3        # Range of values that weights can take {-L, ..., L}

# Create two tree parity machines
a = tpm(N, K, L)
b = tpm(N, K, L)

# Generate random weights for both machines
a.randomWeights()
b.randomWeights()

# Perform syncing for key exchange
count = 0
while True and count < 500:
    # Create random inputs (same inputs for both machines)
    a.randomInputs()
    b.inputs = a.inputs

    # Calculate outputs for both machines
    a.calcWeights2()
    a.tow()
    
    b.calcWeights2()
    b.tow()

    # Perform Hebbian learning if outputs are the same
    if a.output == b.output:
        a.HebbianLearning(a.output, b.output)
        b.HebbianLearning(b.output, a.output)
    count += 1

# Check whether weights are the same
for i in range(len(a.weights)):
    if a.weights[i] != b.weights[i]:
        print("Weights have not synced.")
        exit()
print("Weights have synced.")

# Create 
l = ''.join([str(x) for x in a.weights])

salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm = hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)

key = base64.urlsafe_b64encode(kdf.derive(l.encode()))
print(key)

f = Fernet(key)

token = input("Enter text: ")

print("E:", f.encrypt(token.encode()))
print("D:", f.decrypt(f.encrypt(token.encode())).decode())
