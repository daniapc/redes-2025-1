#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <openssl/sha.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstring>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <vector>

#define MAX 1024

std::string calc_sha256(const std::vector<unsigned char>& data) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256(data.data(), data.size(), hash);
    std::ostringstream ss;
    ss << std::hex << std::setfill('0');
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
        ss << std::setw(2) << (int)hash[i];
    return ss.str();
}

int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main(){
    std::string ip;
    int port;
    std::cout << "IP: "; std::cin >> ip;
    std::cout << "Porta: "; std::cin >> port;
    std::cin.ignore();

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in srv{AF_INET, htons(port)};
    inet_pton(AF_INET, ip.c_str(), &srv.sin_addr);

    if (connect(sock, (sockaddr*)&srv, sizeof(srv)) < 0) {
        perror("connect"); return 1;
    }

    if (set_nonblocking(sock) < 0) perror("fcntl");

    std::cout << "Conectado.\n";

    fd_set readfds;
    std::string line;
    bool receiving_file = false;
    std::vector<unsigned char> filebuf;
    std::string srv_hash;
    while (true) {
        FD_ZERO(&readfds);
        FD_SET(STDIN_FILENO, &readfds);
        FD_SET(sock, &readfds);
        int maxfd = sock;

        if (select(maxfd + 1, &readfds, nullptr, nullptr, nullptr) < 0) {
            perror("select"); break;
        }




        //receber servidor
        if (FD_ISSET(sock, &readfds)) {
            char buf[MAX];
            ssize_t n = recv(sock, buf, MAX, 0);
            if (n <= 0) { std::cout << "Servidor desconectou.\n"; break; }
            std::string s(buf, buf + n);
            if(s.find("erro", 0) == 0) {
                std::cout<<s<<std::endl;
                receiving_file = false;
            }
            else if (s.rfind("chat ", 0) == 0) {
                std::cout << "[CHAT] " << s.substr(5) << "\n";
            }
            else if (!receiving_file) {
                if (s.rfind("HASH:") != std::string::npos) {
                    int end;
                    if(s.rfind("FIM_HASH") != std::string::npos)
                        end = s.rfind("FIM_HASH");
                    else end = n;
                    int begin = s.rfind("HASH:") + 5;
                    srv_hash = s.substr(begin, end - begin);
                    if(srv_hash.rfind('\n') != std::string::npos) srv_hash.erase(srv_hash.find('\n'));
                    std::cout << "[*] Hash servidor: " << srv_hash << "\n";
                    receiving_file = true;
                    char rest[MAX];
                    int sz = int(s.size()) - end - 9;
                    for(int i = 0; i < sz; i++) rest[i] = s[end + 9 + i];
                    if(end < (int)s.size()) filebuf.insert(filebuf.end(), rest, rest + sz);
                }
                /*else {
                    std::cout << s;
                }*/
            }
            else if(receiving_file){
                if (s.rfind("FIM_ARQUIVO") != std::string::npos) {//fimmm do arquivoooo
                    char rest[MAX];
                    int sz = s.rfind("FIM_ARQUIVO");
                    for(int i = 0; i < sz; i++) rest[i] = s[i];
                    filebuf.insert(filebuf.end(), rest, rest + sz);
                    std::string calc = calc_sha256(filebuf);
                    std::string fname = "recv_file";
                    std::ofstream out(fname, std::ios::binary);
                    out.write((char*)filebuf.data(), filebuf.size());
                    out.close();
                    if(!(calc == srv_hash)) std::cout<<"arquivo corrompido! :o\n";
                    else 
                        std::cout << "[*] Arquivo recebido ok!(" << filebuf.size() << " bytes), SHA256=" << calc << "\n";
                    
                    receiving_file = false;
                }
                else {
                    filebuf.insert(filebuf.end(), buf, buf + n);
                }
            }
        }
        //entrada usuário
        if (FD_ISSET(STDIN_FILENO, &readfds)) {
            std::getline(std::cin, line);
            send(sock, line.c_str(), line.size(), 0);
            if (line == "sair") {
                std::cout << "Desconectando..\n";
                break;
            }
            if (line.rfind("arquivo ", 0) == 0) {
                std::cout<< "enviando requisição de arquivo...\n";
                filebuf.clear();
            }
            else if(line.rfind("chat ", 0) == 0) {
                std::cout<<"chat enviado!\n";
            }
            else {
                std::cout << "nao entendi:(, digite chat para mandar mensagens ou arquivo para requisitar arquivo\n";
            }
        }
    }

    close(sock);
    return 0;
}
