import socket

# get the hostname
host = socket.gethostname()
port = 5000  # initiate port no above 1024

server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)
conn, address = server_socket.accept()  # accept new connection
print("Connected to " + address[0] + ":" + str(address[1]))

while True:
  message = input("> ")
  conn.send(message.encode())  # send data to the client
  
  # receive data stream. it won't accept data packet greater than 1024 bytes
  data = conn.recv(1024).decode()
  if not data:
    break

  data = str(data)
  print(data)

  # exit if 'bye'
  if data == "bye":
    break

conn.close()  # close the connection
