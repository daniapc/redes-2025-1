import socket
import os

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

PAYLOAD_SYZE = 1232
SEGMENT_LENGTH= PAYLOAD_SYZE+64

def bin2text(s): return "".join([chr(int(s[i:i+8],2)) for i in range(0,len(s),8)])

def get_segmentos_descarte(requisicao):
    seguimentos = requisicao[requisicao.index(' -d s[')+6:requisicao.index(']')]
    # print(seguimentos)
    seguimentos = seguimentos.split(',')
    indexes = []

    for s in seguimentos:
        if ':' in s:
            rvalues = [item for item in s.split(':') if item]

            if len(rvalues) == 2:
                init = int(rvalues[0])
                fin = int(rvalues[1])

                for i in range (init,fin+1):
                    indexes.append(i)
            elif len(rvalues) == 1:
                if s[0] == ':':
                    for i in range (0,int(rvalues[0])+1):
                        indexes.append(i)
                else:
                    indexes.append(int(rvalues[0]))
                    indexes.append(-1)
        else:
            indexes.append(int(s))
    return indexes

path = os.getcwd() + '/tdp-1/src/'

comandos_validos = ['GET']
arquivos_validos = ['txt', 'dat']

msgFromServer       = "Mensagem recebida com sucesso"
bytesToSend         = str.encode(msgFromServer)

errorMsg = "Erro no recebimento da mensagem"

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
    clientPort = address[1]
    print(clientPort)
    
    print("Message from Client:{}".format(message))

    comando = clientMsg[:clientMsg.index('@')-1]
    print('Comando:', comando)
    # servidor = clientMsg[clientMsg.index('@')+1:clientMsg.index(':')]
    # print('Servidor:', servidor)
    # porta = clientMsg[clientMsg.index(':')+1:clientMsg.index('/')]
    # print('Porta:', porta)
    tem_flag = clientMsg.find(' -d s[') != -1
    print('Flag:', tem_flag)
    arquivo = clientMsg[clientMsg.index('/')+1:] if not(tem_flag) else clientMsg[clientMsg.index('/')+1:clientMsg.index(' -d s[')]
    print('Arquivo:', arquivo)
    extensao_arquivo = arquivo[arquivo.index('.')+1:]
    print(extensao_arquivo)

    print(clientIP)

    if tem_flag:
        indexes = get_segmentos_descarte(requisicao=clientMsg)
        print(indexes)

    if extensao_arquivo not in arquivos_validos or comando not in comandos_validos:
        print('Falha na requisição')
        UDPServerSocket.sendto(str.encode(errorMsg), address)
        continue

    file_path = path+"/data/test_file.txt"
    
    if not(os.path.isfile(file_path)):
        print('Falha na requisição')
        UDPServerSocket.sendto(str.encode(errorMsg), address)
        continue

    f =  open(path+"/data/test_file.txt")
    text = f.read()[0:10000]
    bin_text = " ".join(f"{ord(i):08b}" for i in text).split(" ")

    cursor = 0
    text_lenght = len(bin_text)

    # segment loop
    while cursor < text_lenght:
        payload = ""

        src_bin_port = bin(localPort)[2:].zfill(16)
        dst_bin_port = bin(clientPort)[2:].zfill(16)
        seg_bin_lgth = bin(SEGMENT_LENGTH)[2:].zfill(16)
        checksum_bin = bin(0)[2:].zfill(16)

        payload += src_bin_port+dst_bin_port+seg_bin_lgth+checksum_bin

        for i in range(PAYLOAD_SYZE):
            if cursor >= text_lenght:
                break

            cur_byte = bin_text[cursor][-8:]
            payload += cur_byte
        
            cursor += 1

        bytesToSend =  bin2text( payload).encode('utf-8')
        UDPServerSocket.sendto(bytesToSend, address)
    # Sending a reply to client

    # UDPServerSocket.sendto(bytesToSend, address)