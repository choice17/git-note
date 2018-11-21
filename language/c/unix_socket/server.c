#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#define NSTRS       3           /* no. of strings  */
#define ADDRESS     "mysocket"  /* addr to connect */


#define MSG_LEN 100
/*
 * Strings we send to the client.
 */
int main()
{
    char c;
    FILE *fp;
    int fromlen;
    register int i, s, ns, len;
    struct sockaddr_un fsaun;
	time_t now;  
    char timestr[MSG_LEN];
	char msg[MSG_LEN];

	/*
     * Create the address we will be binding to.
     */
	const struct sockaddr_un saun = {.sun_family=AF_UNIX,
	                                 .sun_path=ADDRESS};
    /*
     * Get a socket to work with.  This socket will
     * be in the UNIX domain, and will be a
     * stream socket.
     */
    if ((s = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
        perror("server: socket");
        return -1;
    }

    //saun.sun_family = AF_UNIX;
    //strcpy(saun.sun_path, ADDRESS);

    /*
     * Try to bind the address to the socket.  We
     * unlink the name first so that the bind won't
     * fail.
     *
     * The third argument indicates the "length" of
     * the structure, not just the length of the
     * socket name.
     */
    unlink(ADDRESS);
    len = sizeof(saun.sun_family) + strlen(saun.sun_path);

	/*
	 * Cast to struct sockaddr* to avoid warning
     */
    if (bind(s, (struct sockaddr*) &saun, sizeof(struct sockaddr_un) ) < 0) { //len) < 0) {
        perror("server: bind");
        return -1;
    }

    /*
     * Listen on the socket.
     */
    if (listen(s, 5) < 0) {
        perror("server: listen");
        return -1;
    }

    /*
     * Accept connections.  When we accept one, ns
     * will be connected to the client.  fsaun will
     * contain the address of the client.
     */
    if ((ns = accept(s, (struct sockaddr*) &fsaun, &fromlen)) < 0) {
        perror("server: accept");
        return -1;
    }

    /*
     * We'll use stdio for reading the socket.
     */
    fp = fdopen(ns, "r");

    /*
     * Then we read some strings from the client and
     * print them out.
     */
    for (;;) {
	
        while ((c = fgetc(fp)) != EOF) {
            putchar(c);
            if (c == '\n')
                break;			
        }

		now = time(NULL);	
		strftime(timestr, sizeof(timestr), "%F %H:%M:%S %Z", localtime(&now));
		sprintf(msg, "ACK from %s at %s\n", __func__, timestr);
		send(ns, &msg, strlen(msg), 0);

    }

    /*
     * We can simply use close() to terminate the
     * connection, since we're done with both sides.
     */
    close(s);

    return -1;
}
