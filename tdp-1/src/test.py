# @IP_Servidor:Porta_Servidor/nome_do_arquivo.ext).
# GET @127.0.0.1:20001/test_file.txt
# requisicao = input()
requisicao = 'GET @127.0.0.1:20001/test_file.txt'
# requisicao = 'GET @127.0.0.1:20001/test_file.txt -d s[0:5,7,9]'

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
        if ':' in s and len(s) == 3:
            init = int(s.split(':')[0])
            fin = int(s.split(':')[1])

            for i in range (init,fin+1):
                indexes.append(i)
        else:
            indexes.append(int(s))

    print(indexes)


import os
path = os.getcwd() + '/tdp-1/src/'

f = open(path+"/data/test_file.txt")
text = f.read()[0:100]

def text2bin(s): return '{:b}'.format(int(u'{s}'.encode('utf-8').encode('hex'), 16))
# bin_text = " ".join(f"{ord(i):08b}" for i in text).split(" ")
bin_text = text2bin(text)

joined_text = ''.join(bin_text)
print(''.join(bin_text))

# def bin2text(s): return "".join([chr(int(x,2)) for x in [s[i:i+8] for i in range(0,len(s), 8)]])
def bin2text(s): return "".join([chr(int(s[i:i+8],2)) for i in range(0,len(s),8)])


print(bin2text(joined_text))
# bin_text = text.encode("utf-8")

# text = '01101001'
# print(bin(int(text, base=2)))

# bin_array = ' '.join(map(bin,bytearray(bin_text)))

# # print(len(text))
# print(bin_array)