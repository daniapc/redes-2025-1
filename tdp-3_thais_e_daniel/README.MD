# Servidor HTTP Simplificado com Sockets TCP

Trabalho da disciplina de Redes de Computadores — UTFPR

## Alunos

- Thaís Say de Carvalho
- Daniel Augusto Pires de Castro

## Descrição

Este projeto consiste em um **servidor HTTP simplificado** implementado em Python utilizando **sockets TCP com multithreading**, sem uso de bibliotecas de alto nível para tratamento de HTTP.

O servidor é capaz de:

- Aceitar conexões simultâneas via múltiplas threads
- Receber requisições HTTP no formato `GET /arquivo.html HTTP/1.1`
- Retornar arquivos HTML e JPEG armazenados localmente
- Responder com erro 404 quando o arquivo não for encontrado

## Como usar

1. Coloque os arquivos HTML e JPEG desejados na pasta `arquivos/`
2. Execute o servidor:
   ```bash
   cd src
   ```
   ```bash
   python3 servidor.py
   ```
3. No navegador, acesse:
   ```bash
   http://localhost:8089/escreva-a-pagina.html
   ```
