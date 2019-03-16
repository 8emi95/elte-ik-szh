#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define DATA "Hello"

int main( int argc, char *argv[])
{
  int sock;			
  struct sockaddr_in server;	
  struct hostent *hp;		
  char buff[1024];		
  int rval;			

  if (argc<3)
  {
	   printf("Usage:\n%s <server's hostname> <port>", argv[0]);
	   exit(-1);
  } 

  sock = socket( AF_INET, SOCK_STREAM, 0 );
  if( sock == -1 ) 
  {
	   perror( "opening stream socket" );
	   exit(1);
  }

  hp = gethostbyname(argv[1]); 
  if ( hp == (struct hostent *) 0 ) 
  {
	   fprintf( stderr, "%s: unknown host \n", argv[1] );
	   exit(2);
  }
  server.sin_family = AF_INET;
  memcpy( (void *) &server.sin_addr, (void *) hp->h_addr, hp->h_length );
  server.sin_port = htons( atoi ( argv[2] ) );

  if( connect( sock, (struct sockaddr *) &server, sizeof server ) == -1 ) 
  {
	   perror( "connecting stream socket" );
	   exit(3);
  }

  if( send( sock, DATA, sizeof DATA, 0 ) == -1 )
  {
	   perror( "writing on stream socket" );
  }

  if(( rval = recv( sock, buff, sizeof buff, 0 )) == -1 )
  {
        perror( "reading stream socket" );
  }
  else 
  { 
     buff[rval] = '\0';
     printf( "Message from the server: %s\n", buff );
  }
  
  close( sock );
  exit(0);
}
