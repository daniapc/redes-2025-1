import socket
import os

serverAddressPort   = ("127.0.0.1", 20001)

PAYLOAD_SYZE = 1232
SEGMENT_LENGTH= PAYLOAD_SYZE+64
bufferSize  = SEGMENT_LENGTH

path = os.getcwd()
path = path[:path.index('/redes-2025-1')] + '/redes-2025-1/tdp-1/src/'

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("Digita ae a Requisição")

# @IP_Servidor:Porta_Servidor/nome_do_arquivo.ext).
# GET @127.0.0.1:20001/test_file.txt
# GET @127.0.0.1:20001/test_file.txt -d s[0:5,7,9]

# requisicao ='GET @127.0.0.1:20001/test_file.txt -d s[0:5,7,9]'
# requisicao ='GET @127.0.0.1:20001/Dickens.txt -d s[0:5,7,9]'
requisicao ='GET @127.0.0.1:20001/Metamorphosis.txt -d s[0:5,7,9,20:]'
# requisicao ='GET @127.0.0.1:20001/Shakespeare.txt -d s[0:5,7,9]'

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

binary_sum = lambda a,b : bin(int(a, 2) + int(b, 2))
def checksum_op(a, b):
    sum = binary_sum(a,b)[2:]
    if len(sum) > 16:
        sum = sum[-16:]
        sum = binary_sum(sum,'1')[2:]
    return sum.zfill(16)
def invert_bits(a):
    return ''.join(['1' if bit == '0' else '0' for bit in a])

if os.path.exists(path + "out/client_file.txt"):
  os.remove(path + "out/client_file.txt")

seg = 0

while (True):
    requisicao ='GET @127.0.0.1:20001/ -n s['+ str(seg) + ']'
    msgFromClient       = requisicao
    bytesToSend         = str.encode(msgFromClient)
    print(requisicao)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "{}".format(msgFromServer[0])

    decoded_msg = msgFromServer[0].decode("utf-8")

    bin_text = " ".join(f"{ord(i):08b}" for i in decoded_msg).split(" ")
    header = bin_text[0:8]

    src_port = int(header[0]+header[1], 2)
    dst_port = int(header[2]+header[3], 2)
    seg_lgth = int(header[4]+header[5], 2)
    hdr_csum = header[6]+header[7]

    if hdr_csum == ''.zfill(16):
        break

    payload = bin_text[8:]

    checksum = "0"

    for cur_byte in payload: 
        checksum = checksum_op(checksum, cur_byte)
    
    checksum = invert_bits(checksum)

    valid = checksum == hdr_csum

    if not(valid):
        if binary_sum(''.join(payload),'0')[2:] == '0':
            seg += 1
            print("-------------------------------------------------------")
            continue
        else:
            print('Erro na requisição')
            break

    print("Source port:", src_port)
    print("Destin port:", dst_port)
    print("Segment Lenght:", seg_lgth)
    print("Header Checksum:", hdr_csum)
    print("Valid message:", valid)
    decoded_msg = decoded_msg[31:]

    f = open(path + "out/client_file.txt", "a") 
    f.write(decoded_msg)

    seg += 1
    print("-------------------------------------------------------")

    