#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define DATA "Hello"

int main( int argc, char *argv[])
{
  int client;
  struct sockaddr_in name;
  struct sockaddr_in server_name;
  struct hostent *hp;
  int nbytes;
  int length;
  char buffer[1024];

  if((client = socket( AF_INET, SOCK_DGRAM, 0 )) == -1 ) {
  	 perror( "creating socket" );
  	 return 1;
  }
  
  name.sin_family = AF_INET;
  name.sin_addr.s_addr = INADDR_ANY;
  name.sin_port = 0;

  if( bind( client, (struct sockaddr *) &name, sizeof name ) == -1 ) {
  	 perror( "binding failed" );
  	 return 2;
  }

  hp = gethostbyname(argv[1]);
  if( hp == (struct hostent *) 0 ) {
  	 fprintf( stderr, "%s: unknown host name\n", argv[1] );
  	 return 2;
	}

  memcpy( (void *) &server_name.sin_addr, (void *) hp->h_addr, hp->h_length );
  server_name.sin_family = AF_INET;
  server_name.sin_port = htons( atoi ( argv[2] ));

  if( sendto(client, DATA, sizeof DATA, 0, (struct sockaddr *) &server_name, sizeof server_name)==-1)
        perror( "sending data failed" );
  if( (nbytes=recvfrom(client, buffer, sizeof buffer, 0,(struct sockaddr *) &server_name, &length))==-1 )
  		    perror( "recieving data failed" );
  		    
  buffer[nbytes]='\0';			
  printf("Message from server is '%s'.\n",buffer);
  close(client);
  return 0;
};
