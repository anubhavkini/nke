import socket

# get the hostname
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
print("Connected to " + host + ":" + str(port))

while True:
  data = client_socket.recv(1024).decode()  # receive response
  if not data:
    break

  data = str(data)
  print(data)

  # exit if 'bye'
  if data == "bye":
    break

  message = input("> ")  # take input

  client_socket.send(message.encode())  # send message

client_socket.close()  # close the connection
