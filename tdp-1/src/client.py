import socket

serverAddressPort   = ("127.0.0.1", 20001)

bufferSize          = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("Digita ae a Requisição")

# @IP_Servidor:Porta_Servidor/nome_do_arquivo.ext).
# GET @127.0.0.1:20001/test_file.txt
# GET @127.0.0.1:20001/test_file.txt -d s[0:5,7,9]

requisicao ='GET @127.0.0.1:20001/test_file.txt -d s[0:5,7,9]'

comando = requisicao[:requisicao.index('@')-1]
print(comando)
print('Comando:', comando)
servidor = requisicao[requisicao.index('@')+1:requisicao.index(':')]
print('Servidor:', servidor)
porta = requisicao[requisicao.index(':')+1:requisicao.index('/')]
print('Porta:', porta)
tem_flag = requisicao.find(' -d s[') != -1
print('Flag:', tem_flag)
arquivo = requisicao[requisicao.index('/')+1:] if not(tem_flag) else requisicao[requisicao.index('/')+1:requisicao.index(' -d s[')]
print('Arquivo:', arquivo)

serverAddressPort = (str(servidor), int(porta))

msgFromClient       = requisicao

bytesToSend         = str.encode(msgFromClient)

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)