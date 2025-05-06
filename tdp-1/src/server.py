import socket

localIP     = "127.0.0.1"

localPort   = 20001

bufferSize  = 1024

msgFromServer       = "Mensagem recebida com sucesso"

bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = message.decode("utf-8")
    clientIP  = "Client IP Address:{}".format(address)
    
    print("Message from Client:{}".format(message))

    comando = clientMsg[:clientMsg.index('@')-1]
    print('Comando:', comando)
    servidor = clientMsg[clientMsg.index('@')+1:clientMsg.index(':')]
    print('Servidor:', servidor)
    porta = clientMsg[clientMsg.index(':')+1:clientMsg.index('/')]
    print('Porta:', porta)
    tem_flag = clientMsg.find(' -d s[') != -1
    print('Flag:', tem_flag)
    arquivo = clientMsg[clientMsg.index('/')+1:] if not(tem_flag) else clientMsg[clientMsg.index('/')+1:clientMsg.index(' -d s[')]
    print('Arquivo:', arquivo)

    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)