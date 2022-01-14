#!/usr/bin/env python3

from treeParityMachine import tpm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import socket

N = 101      # number of input neurons per hidden neuron
K = 2        # number of neurons in hidden layer
L = 3        # range of values that weights can take {-L, ..., L}

print('\033c')

# create tree parity machine
print("Creating tree parity machine")
tree = tpm(N, K, L)

# Generate random weights for the machine
print("Generating random weights for machine")
tree.randomWeights()

print("Initializing networking")
# get the hostname
host = socket.gethostname()
port = 5000  # initiate port no above 1024

server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)
conn, address = server_socket.accept()  # accept new connection
print("Connected to " + address[0] + ":" + str(address[1]))

# perform key exchange
print("Beginning key exchange")
print(tree.weights)
count = 0
while count < 500:
  # Create random inputs (same inputs for both machines)
  tree.randomInputs()
  message = str(tree.inputs)
  conn.send(message.encode())

  # Calculate output
  tree.calcWeights2()
  tree.tow()

  # send output
  message = str(tree.output)
  conn.send(message.encode())

  # recieve output
  message = conn.recv(1024).decode()
  output = int(message)

  # perform Hebbian learning if outputs are the same
  if output == tree.output:
    tree.HebbianLearning(tree.output, output)
    print("\033[6;0H")
    print(tree.weights)

  count += 1

print("\033[6;0H")
print(tree.weights)
print("Weights synced successfully")

# generate key from weights
print("Generating key from weights")
l = ''.join([str(x) for x in tree.weights])
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=390000)
key = base64.urlsafe_b64encode(kdf.derive(l.encode()))
print("Generated key is")
print(key)

# encryption
f = Fernet(key)

# messaging
print("Starting encrypted chat")
while True:
  message = input("> ")
  message = f.encrypt(message.encode())
  conn.send(message)  # send data to the client
  
  # receive data stream. it won't accept data packet greater than 1024 bytes
  data = conn.recv(1024)
  if not data:
    break

  data = f.decrypt(data).decode()
  print(data)

  # exit if 'bye'
  if data == "bye":
    break

print("Closing connection")
conn.close()  # close the connection
