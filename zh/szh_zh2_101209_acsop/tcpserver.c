#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>

void printServerInfo(int sock);

int main()
{
  int sock;
  struct sockaddr_in server;	
  struct sockaddr_in client;
  int conn;
  char buf[1024];
  int rval;			
  socklen_t length;
  
  sock = socket( AF_INET, SOCK_STREAM, 0 );
  if( sock == -1 ) 
  {
	   perror( "opening stream socket" );
	   exit(1);
  }
 
  server.sin_family = AF_INET;
  server.sin_addr.s_addr = INADDR_ANY;
  server.sin_port = 0; 

  if( bind( sock, (struct sockaddr *) &server, sizeof server ) == -1 ) 
  {
	   perror( "binding stream socket" );
	   exit(2);
  }
  printServerInfo( sock );

  listen( sock, 3 );
  printf("Start listening...\n");

  do {
	   length = sizeof client;
	   conn = accept( sock, (struct sockaddr *) &client, &length );
     if( conn == -1 )
     {
     		perror( "accept" );
     }
	   else
	   {
    		printf( "A client has arrived.\n");
		    printf( "\t From IP:port: %s:%d\n", inet_ntoa( client.sin_addr ), ntohs( client.sin_port ) );
        memset( (void *)buf, 0, sizeof buf );
        if(( rval = recv( conn, buf, 1024, 0 )) == -1 )
		    {
			     perror( "reading stream socket" );
        }
		    else 
        {
			     printf( "Message from the above client:\"%s\"\n", buf );
				   if( send( conn, buf, rval, 0 ) == -1 )
			           perror( "writing on stream socket" );
			  }

        close( conn ); 
	   }
  } while(1);

  exit(0);
}

void printServerInfo(int sock)
{
	struct sockaddr_in server_info;
	socklen_t length = sizeof server_info;
  
	if( getsockname( sock, (struct sockaddr *) &server_info, &length ) == -1 ) 
  {
		perror( "getting socket name" );
		exit( 3 );
  }

  printf( "Server IP: %s\n", inet_ntoa( server_info.sin_addr ) );
  printf( "Server port: %d\n", ntohs( server_info.sin_port ) );
}