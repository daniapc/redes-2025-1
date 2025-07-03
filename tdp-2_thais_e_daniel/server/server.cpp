#include <arpa/inet.h>
#include <chrono>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <netinet/in.h>
#include <openssl/sha.h>
#include <pthread.h>
#include <sys/socket.h>
#include <unistd.h>
#include <vector>
#include <queue>
#include <map>
#include <mutex>
#include <algorithm>

#define MAX 1024
#define PORT 8985

std::vector<int> clients;
std::mutex mtx;
std::map<int, std::queue<std::string>> msgs;

void broadcast_msg(const std::string& msg) {
    std::lock_guard<std::mutex> lock(mtx);
    for (int sock : clients) {
        msgs[sock].push(msg);
    }
}

std::string sha256_of_file(const std::string& path) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    std::ifstream in(path, std::ifstream::binary);
    if (!in.good()) return "";
    char buf[MAX];
    while (in.good()) {
        in.read(buf, MAX);
        SHA256_Update(&sha256, buf, in.gcount());
    }
    SHA256_Final(hash, &sha256);
    std::ostringstream ss;
    ss << std::hex << std::setfill('0');
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
        ss << std::setw(2) << (int)hash[i];
    in.close();
    return ss.str();
}

void* handle_client(void* _sock) {
    int sock = *(int*)_sock;
    delete (int*)_sock;
    std::cout << "cliente " << sock << " conectado.\n";
    {
        std::lock_guard<std::mutex> lock(mtx);
        clients.push_back(sock);
    }

    char buff[MAX];
    while (true) {
        ssize_t len = recv(sock, buff, MAX - 1, 0);
        if (len <= 0) break;
        buff[len] = '\0';
        std::string cmd(buff);

        if (cmd == "sair") {
            std::cout << "Cliente " << sock << " desconectado." << std::endl;
            break;
        } 
        else if (cmd.rfind("arquivo ", 0) == 0) {
            std::string file = cmd.substr(8);
            std::string hash = sha256_of_file(file);
            std::cout << "Requisição do arquivo " << file << " recebida\n";
            if (hash.empty()) {
                std::string err = "erro : arquivo nao encontrado :(\n";
                std::cout << "Arquivo não existe:(\n";
                send(sock, err.c_str(), err.size(), 0);
            }
            else {
                std::string hdr = "HASH:" + hash + "FIM_HASH\n";
                std::cout << "enviando arquivo..\n";
                send(sock, hdr.c_str(), hdr.size(), 0);

                std::ifstream in(file, std::ifstream::binary);
                while (in.good()) {
                    in.read(buff, MAX);
                    send(sock, buff, in.gcount(), 0);
                }
                in.close();
                std::string end_marker = "FIM_ARQUIVO\n";
                send(sock, end_marker.c_str(), end_marker.size(), 0);
            }
        } 
        else if (cmd.rfind("chat ", 0) == 0) {
            std::string msg = cmd.substr(5);
            std::cout << "[CHAT de " << sock << "] " << msg << std::endl;
        }
        {
            std::lock_guard<std::mutex> lock(mtx);
            while(!msgs[sock].empty()) {
                send(sock, msgs[sock].front().c_str(), msgs[sock].front().size(), 0);
                msgs[sock].pop();
            }
        }
    }

    close(sock);
    {
        std::lock_guard<std::mutex> lock(mtx);
        clients.erase(std::remove(clients.begin(), clients.end(), sock), clients.end());
        msgs.erase(msgs.find(sock));
    }
    return nullptr;
}

void* console_thread(void*) {
    std::string line;
    while (std::getline(std::cin, line)) {
        broadcast_msg("chat " + line + "\n");
    }
    return nullptr;
}

int main() {
    int server = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);
    bind(server, (sockaddr*)&addr, sizeof(addr));
    listen(server, 10);
    std::cout << "Servidor ouvindo porta " << PORT << "\n";

    pthread_t th;
    pthread_create(&th, nullptr, console_thread, nullptr);

    while (true) {
        int* client_sock = new int;
        sockaddr_in cli_addr{};
        socklen_t cli_len = sizeof(cli_addr);
        *client_sock = accept(server, (sockaddr*)&cli_addr, &cli_len);
        pthread_t ct;
        pthread_create(&ct, nullptr, handle_client, client_sock);
        pthread_detach(ct);
    }
    return 0;
}
