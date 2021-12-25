from treeParityMachine import tpm

N = 4      # Number of input neurons per hidden neuron
K = 128    # Number of neurons in hidden layer
L = 1      # Range of values that weights can take {-L, ..., L}

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

# Print final weights
#print(a.weights)
#print(b.weights)

# Check whether weights are the same
for i in range(len(a.weights)):
    if a.weights[i] != b.weights[i]:
        print("Weights have not synced.")
        exit()
print("Weights have synced.")
