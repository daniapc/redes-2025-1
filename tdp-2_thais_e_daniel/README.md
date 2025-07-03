sudo apt install openssl libssl-dev

para rodar servidor:
g++ server.cpp -Wall -O2 -lssl -lcrypto
depois ./a.out

para rodar cliente:
g++ client.cpp -Wall -O2 -lssl -lcrypto
depois ./a.out
