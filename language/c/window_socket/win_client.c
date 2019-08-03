//#pragma comment(lib, "Ws2_32.lib")

// -lWs2_32 
#include <WinSock2.h>
#include <string.h>
#include <stdio.h>

#define IPADDR "127.0.0.1"
#define IPPORT (1234)

int main()
{
    char confirm[20];
    char message[200];
 
    //start Winsock-DLL
    //int r;
    struct WSAData wsaData;
    WORD DLLVersion;
    DLLVersion = MAKEWORD(2,1);
    //r = WSAStartup(DLLVersion, &wsaData);
    WSAStartup(DLLVersion, &wsaData);
 
    //declare socket sockadder_in struct
    SOCKADDR_IN addr;
 
    int addlen = sizeof(addr);
 
    //setup socket
    SOCKET sConnect;
 
    //AF_INET: internet-family
    //SOCKET_STREAM: connection-oriented socket
    sConnect = socket(AF_INET, SOCK_STREAM, 0);
 
    //setup addr info
    addr.sin_addr.s_addr = inet_addr(IPADDR);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(IPPORT);
 
    fprintf(stderr, "connect to server?[Y] or [N]\n");
    //scanf("%s",confirm);
    confirm[0] = 'Y';
    if(!strcmp(confirm, "N"))
    {
        exit(1);
    }else{
        if(!strcmp(confirm,"Y"))
        {
            //connect(sConnect, (SOCKADDR*)&addr, sizeof(addr));
            connect(sConnect, (SOCKADDR*)&addr, addlen);
 
            //recv server side info
            while (1) {
                ZeroMemory(message, 200);
                int r = recv(sConnect, message, sizeof(message), 0);
                if (r >= 0) {
                    fprintf(stdout, "strlen:%d msg:%s", r, message);
                    fflush(stdout);
 
            //when setting up closesocket，close socket witout TIME-WAIT
            //BOOL bDontLinger = FALSE;
            //setsockopt(sConnect,SOL_SOCKET,SO_DONTLINGER,(const char*)&bDontLinger,sizeof(BOOL));
             
            //use closesocket directly if we donot have futher action
                } else {
                    fprintf(stderr, "connection closed!\n");
                    break;
                }
            }
            closesocket(sConnect);
        }
    }
    return 0;
 
}