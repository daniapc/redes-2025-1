# @IP_Servidor:Porta_Servidor/nome_do_arquivo.ext).
# GET @127.0.0.1:20001/test_file.txt
# requisicao = input()
# requisicao = 'GET @127.0.0.1:20001/test_file.txt'
requisicao = 'GET @127.0.0.1:20001/test_file.txt -d s[:5,7,9,20:]'

comando = requisicao[:requisicao.index('@')-1]
print(comando)
servidor = requisicao[requisicao.index('@')+1:requisicao.index(':')]
print(servidor)
porta = requisicao[requisicao.index(':')+1:requisicao.index('/')]
print(porta)
tem_flag = requisicao.find(' -d s[') != -1
print(tem_flag)
arquivo = requisicao[requisicao.index('/')+1:] if not(tem_flag) else requisicao[requisicao.index('/')+1:requisicao.index(' -d s[')]
print(arquivo)


if (tem_flag):
    seguimentos = requisicao[requisicao.index(' -d s[')+6:requisicao.index(']')]
    print(seguimentos)
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

    print(indexes)


import os
path = os.getcwd() + '/tdp-1/src/'

f = open(path+"/data/test_file.txt")
text = f.read()[0:100]

# def text2bin(s): return '{:b}'.format(int(u'{s}'.encode('utf-8').encode('hex'), 16))
bin_text = " ".join(f"{ord(i):08b}" for i in text).split(" ")

joined_text = ''.join(bin_text)
print(''.join(bin_text))

# def bin2text(s): return "".join([chr(int(x,2)) for x in [s[i:i+8] for i in range(0,len(s), 8)]])
def bin2text(s): return "".join([chr(int(s[i:i+8],2)) for i in range(0,len(s),8)])

print(bin2text(joined_text))

port   = 20001
bin_port = bin(port)[2:].zfill(16)
print(bin_port)

print(bin_text)

binary_sum = lambda a,b : bin(int(a, 2) + int(b, 2))

a = bin_text[0]
a = '11111111'

b = bin_text[1]

print(a)
print(b)

sum = binary_sum(a,b)[2:]
print(sum)
if len(sum) > 8:
    sum = sum[-8:]
    print(sum)
    sum = binary_sum(sum,'1')[2:].zfill(8)
    print(sum)

def invert_bits(a):
    return ''.join(['1' if bit == '0' else '0' for bit in a])

print(invert_bits(sum))
# print(binary_sum(a,b)[2:])

msg = 'N!\xc3\x86\xc3\xab\x05\x10S/Is it for fear to wet a widow\x19s eye,'
bin_msg = " ".join(f"{ord(i):08b}" for i in msg).split(" ")
print(bin_msg)

req = 'GET @127.0.0.1:20001/ -n s['+ str(1) + ']'

seg = req[req.index('-n s[') + 5:req.index(']')]
print(seg)