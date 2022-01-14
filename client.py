#!/usr/bin/env python3

import numpy as np
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
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
print("Connected to " + host + ":" + str(port))

# perform key exchange
print("Beginning key exchange")
print(tree.weights)
count = 0
while count < 500:
  message = client_socket.recv(1024).decode()
  message = message.replace('  ', ',').replace(' ', ',')
  if message[1] == ',':
    tree.inputs = eval(message.replace(',', '', 1))
  else:
    tree.inputs = eval(message)

  # calculate output
  tree.calcWeights2()
  tree.tow()

  # recieve output
  message = client_socket.recv(1024).decode()
  output = int(message)

  # send output
  message = client_socket.send(str(tree.output).encode())

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
  data = client_socket.recv(1024)  # receive response
  if not data:
    break

  data = f.decrypt(data).decode()
  print(data)

  # exit if 'bye'
  if data == "bye":
    break

  message = input("> ")  # take input
  message = f.encrypt(message.encode())
  client_socket.send(message)  # send message

print("Closing connection")
client_socket.close()  # close the connection
