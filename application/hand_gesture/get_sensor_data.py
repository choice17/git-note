import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 3000
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
server.bind((bind_ip, bind_port))
            
server.listen(5)
 
print("[*] Listening on %s:%d" % (bind_ip, bind_port))
 
def handle_client(client_socket):
    while True:
        request = client_socket.recv(128)
        print ("[*] Received: %s" % request)
    client_socket.close()
    
while True:
    client, addr = server.accept()
    print("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))
    r = client.recv(1024)
    print ("[*] Received: %s" % r)
    client.close()#client.send(b"ACK!")
    #client_handler = threading.Thread(target=handle_client, args=(client,))
    #client_handler.start()