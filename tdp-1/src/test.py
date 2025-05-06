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