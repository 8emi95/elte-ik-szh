#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define DATA "Hello"

void printServerInfo(int sock);

int main(int argc, char *argv[])
{
  int server;
  size_t length;
  struct sockaddr_in name, client_name;
  int nbytes;
  char buffer[1024];

  server = socket( AF_INET, SOCK_DGRAM, 0 );
  if( server == -1 ) {
  	 perror( "opening datagram socket" );
  	 return 1;
  }

  name.sin_family = AF_INET;
  name.sin_addr.s_addr = INADDR_ANY;
  name.sin_port = 0;

  if( bind( server, (struct sockaddr *) &name, sizeof name ) == -1 ) {
    	perror( "binding datagram socket" );
    	return 2;
  }

  length = sizeof(name);
    
  printServerInfo(server);
  length = sizeof(client_name);
  do
  {
  	if( (nbytes = recvfrom(server, buffer, sizeof buffer, 0, (struct sockaddr *) &client_name, &length)) == -1 )
		        perror( "receiving datagram socket" ); 
  	buffer[nbytes]='\0';
  	printf("Incoming data from %s:%d\n\tClient say '%s'\n",inet_ntoa(client_name.sin_addr),ntohs(client_name.sin_port),buffer);
  	if((nbytes=sendto(server, DATA, sizeof DATA, 0, (struct sockaddr*) &client_name, sizeof client_name))==-1)
  		  perror("sending datagram");
  	printf("Size of reply %d %s\n",nbytes,DATA);
  }while(1);
  
  close( server );
  return 0;
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