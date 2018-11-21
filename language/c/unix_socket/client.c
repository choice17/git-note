/* https://users.cs.cf.ac.uk/Dave.Marshall/C/node28.html

struct sockaddr_un{
                short                    sun_family;           //AF_UNIX
                char                     sun_PATH[108];        //path name 
   };

struct sockaddr_in {
                short                     sin_family;          //AF_INET
                u_short                   sin_port;            //16-bit port number
                struct in_addr            sin_addr;
                char                      sin_zero[8];         //unused
   };

struct in_addr {
                u_long                  s_addr;                //32-bit net id
   };
*
*/

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>

//#define NSTRS       3           /* no. of strings  */
#define ADDRESS     "mysocket"  /* addr to connect */

/*
 * Strings we send to the server.
 */
#define TIMESTR_LEN 100
#define MSG_LEN 100


static time_t now;
static char timestr[TIMESTR_LEN];

void getLine(char *msg)
{
	
	now = time(NULL);
	strftime(timestr, sizeof(timestr), "%F %H:%M:%S %Z", localtime(&now));
	printf("client> ");
	scanf("%s", msg);		
	sprintf(msg, "%s sent from client @ %s\n", msg, timestr);
    
}

int main()
{
    char c;
    FILE *fp;
    register int i, s, len;
	char msg[MSG_LEN];

	/*
     * Create the address we will be connecting to.
     */
    const struct sockaddr_un saun = {.sun_family=AF_UNIX,
	                                 .sun_path=ADDRESS};

    /*
     * Get a socket to work with.  This socket will
     * be in the UNIX domain, and will be a
     * stream socket.
     */
    if ((s = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
        perror("client: socket");
        return -1;
    }     
	
    /*
     * Try to connect to the address.  For this to
     * succeed, the server must already have bound
     * this address, and must have issued a listen()
     * request.
     *
     * The third argument indicates the "length" of
     * the structure, not just the length of the
     * socket name.
     */
   
    if (connect(s, (struct sockaddr*) &saun, sizeof(struct sockaddr_un) ) < 0 ) {
        perror("client: connect");
        return -1;
    }

    /*
     * We'll use stdio for reading
     * the socket.
     */
    fp = fdopen(s, "r");

    /*
     * Now we send some strings to the server.
     */
    now = time(NULL);
    strftime(timestr, sizeof(timestr), "%F %H:%M:%S %Z", localtime(&now));
    printf("Starts %s @ %s!\n", __func__, timestr);

	while (1) {

		getLine(&msg[0]);		
		send(s, &msg, strlen(msg), 0);
		sleep(0.5);

		while ((c = fgetc(fp)) != EOF) {
            putchar(c);
            if (c == '\n')
                break;			
        }
	}

    /*
     * We can simply use close() to terminate the
     * connection, since we're done with both sides.
     */
    close(s);

    return 0;
}
