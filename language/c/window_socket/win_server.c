/* https://xyz.cinc.biz/2014/02/c-socket-server-client.html */

//#pragma comment(lib, "Ws2_32.lib")
 
#include <WinSock2.h>
#include <stdio.h>

#define IPADDR "127.0.0.1"
#define IPPORT (1234)

int main()
{
    //int r;
    struct WSAData wsaData;
    WORD DLLVSERION;
    DLLVSERION = MAKEWORD(2,1);//Winsocket-DLL
 
    //Use WSAStartup to start Winsocket-DLL
    //r = WSAStartup(DLLVSERION, &wsaData);
    WSAStartup(DLLVSERION, &wsaData);
 
    // declare addr len (different device have difference addr info)
    SOCKADDR_IN addr;
    int addrlen = sizeof(addr);
 
    //create socket
    SOCKET sListen; //listening for an incoming connection
    SOCKET sConnect; //operating if a connection was found
 
    //AF_INET：socket belong to internet family
    //SOCK_STREAM：socket is connection-oriented socket 
    sConnect = socket(AF_INET, SOCK_STREAM, 0);
 
    // Address info
    addr.sin_addr.s_addr = inet_addr(IPADDR);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(IPPORT);
 
    //setup Listen
    sListen = socket(AF_INET, SOCK_STREAM, 0);
    bind(sListen, (SOCKADDR*)&addr, sizeof(addr));
    listen(sListen, SOMAXCONN);//SOMAXCONN: listening without any limit
 
    //waiting connection
    SOCKADDR_IN clinetAddr;
    int cnt = 0;
    while(1)
    {
        printf("waiting...\n");
 
        sConnect = accept(sListen, (SOCKADDR*)&clinetAddr, &addrlen);
        if (sConnect)
        {
            printf("a connection was found\n");
            printf("server: got connection from %s\n", inet_ntoa(addr.sin_addr));
            fflush(stdout);
            //send to client side
            char sendbuf[64];
            sprintf(sendbuf, "sending data test from server cnt:%d\n", ++cnt);
            while (1) {
                printf("Input:\n");
                int sc = 0;
                while (1) {
                    sendbuf[sc++] = getchar();
                    if ((sendbuf[sc-1]) == '\n') {
                        //sendbuf[sc] = 0;
                        break;
                    }
                }
                    //scanf("%s", sendbuf);
                if (send(sConnect, sendbuf, sc, 0) == -1) {
                    printf("server: disconnected from %s\n", inet_ntoa(addr.sin_addr));
                    break;
                }
                /*if (send(sConnect, sendbuf, sc, 0)) {//(int)strlen(sendbuf), 0)) {
                    printf("fail to send! break!\n");
                    break;
                }*/
            }
             
        }
    }
    return 0;
    //getchar();
}