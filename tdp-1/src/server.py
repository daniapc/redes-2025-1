import socket
import os
import time

localIP     = "127.0.0.1"
localPort   = 20001

PAYLOAD_SYZE = 1232
SEGMENT_LENGTH= PAYLOAD_SYZE+64
bufferSize  = SEGMENT_LENGTH

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

binary_sum = lambda a,b : bin(int(a, 2) + int(b, 2))
def checksum_op(a, b):
    sum = binary_sum(a,b)[2:]
    if len(sum) > 16:
        sum = sum[-16:]
        sum = binary_sum(sum,'1')[2:]
        
    return sum.zfill(16)

def invert_bits(a):
    return ''.join(['1' if bit == '0' else '0' for bit in a])

path = os.getcwd()
path = path[:path.index('/redes-2025-1')] + '/redes-2025-1/tdp-1/src/'

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

src_bin_port = ''.zfill(16)
dst_bin_port = ''.zfill(16)
seg_bin_lgth = bin(SEGMENT_LENGTH)[2:].zfill(16)

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = message.decode("utf-8")
    clientIP  = "Client IP Address:{}".format(address)
    clientPort = address[1]
    # print(clientPort)
    
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
    # print('Arquivo:', arquivo)
    extensao_arquivo = arquivo[arquivo.index('.')+1:]
    # print(extensao_arquivo)

    print(clientIP)

    if tem_flag:
        desc_indexes = get_segmentos_descarte(requisicao=clientMsg)
        desc_indexes.sort()
        # print(desc_indexes)

    if extensao_arquivo not in arquivos_validos or comando not in comandos_validos:
        print('Falha na requisição')
        UDPServerSocket.sendto(str.encode(errorMsg), address)
        continue

    file_path = path+"/data/" + arquivo
    
    if not(os.path.isfile(file_path)):
        print('Falha na requisição')
        UDPServerSocket.sendto(str.encode(errorMsg), address)
        continue

    f =  open(file_path)
    # text = f.read()[0:10000]
    text = f.read()
    bin_text = " ".join(f"{ord(i):08b}" for i in text).split(" ")

    cursor = 0
    text_lenght = len(bin_text)

    # segment loop
    seg = 0

    while cursor < text_lenght:
        payload = ""
        checksum = "0"

        for i in range(PAYLOAD_SYZE):
            if cursor >= text_lenght:
                break

            cur_byte = bin_text[cursor][-8:]

            checksum = checksum_op(checksum, cur_byte)
            payload += cur_byte
        
            cursor += 1
        
        if seg in desc_indexes or (-1 in desc_indexes and seg >= desc_indexes[len(desc_indexes)-1]):
            payload = ''.zfill(8*PAYLOAD_SYZE)

        # calcula headers
        src_bin_port = bin(localPort)[2:].zfill(16)
        dst_bin_port = bin(clientPort)[2:].zfill(16)
        seg_bin_lgth = bin(SEGMENT_LENGTH)[2:].zfill(16)
        checksum = invert_bits(checksum)

        # constroi msg
        header = src_bin_port + dst_bin_port + seg_bin_lgth+ checksum
        msgToSend = header + payload

        #envia msg
        bytesToSend =  bin2text(msgToSend).encode('utf-8')
        UDPServerSocket.sendto(bytesToSend, address)

        #espera enviar confirmação de segmento
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]
        clientMsg = message.decode("utf-8")

        #pega o segmento para confirmar se está certo
        client_seg = clientMsg[clientMsg.index('-n s[') + 5:clientMsg.index(']')]

        if seg == int(client_seg):
            seg += 1
        else:
            print('Falha na requisição')
            UDPServerSocket.sendto(str.encode(errorMsg), address)
            continue

    #manda finalizar (payload de zeros com checksum de zeros)
    header = src_bin_port + dst_bin_port + seg_bin_lgth+''.zfill(16)
    msgToSend = header + ''.zfill(8*PAYLOAD_SYZE)
    bytesToSend =  bin2text(msgToSend).encode('utf-8')
    UDPServerSocket.sendto(bytesToSend, address)

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    clientMsg = message.decode("utf-8")
    client_seg = clientMsg[clientMsg.index('-n s[') + 5:clientMsg.index(']')]

    if seg == int(client_seg):
        print("Requisição de arquivo realizada com sucesso!")

    # Sending a reply to client

    # UDPServerSocket.sendto(bytesToSend, address)