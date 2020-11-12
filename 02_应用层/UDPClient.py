from socket import *

serverName = "localhost"
serverPort = 8888
clientSocket = socket(AF_INET,SOCK_DGRAM)
message = "wybwywbybywbywbyw"
clientSocket.sendto(message.encode(),(serverName,serverPort))
modifiedMessage , serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
print(serverAddress)
clientSocket.close()