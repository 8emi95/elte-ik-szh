#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define MAX_ARUK 32
#define CLI_BUF 32

struct arucikk {
    char nev[28];
    int darab;
};

struct cli_parancs {
    char parancs;
    char nev[28];
};

int main(int argc, char *argv[])
{
	if (argc < 3)
	{
		printf("Az IP-t es a portot meg kell adni argumentumkent!\n");
		return 1;
	}

	// socket

	int clifd;
	clifd = socket(AF_INET, SOCK_DGRAM, 0);

	// sockaddr_in

    struct sockaddr_in srvinfo;
    memset(&srvinfo, '\0', sizeof(srvinfo));

    srvinfo.sin_family = AF_INET;
    srvinfo.sin_port = htons(atoi(argv[2]));
    srvinfo.sin_addr.s_addr = inet_addr(argv[1]);

    // user input

    char sor[64];
    char parancs[64];
    char arunev[64];
    int n;
    struct cli_parancs p;

    int valasz_db;
    char valasz_st;
    struct arucikk valasz_raktar[MAX_ARUK];
    int i;
    int cli_len;

    while (1)
    {
    	printf("Parancs: ");
    	fgets(sor, 64, stdin);
    	n = sscanf(sor, "%s %s", parancs, arunev);
    	memset(&p, 0, sizeof(p));

    	if (n == 2 && !strcmp(parancs, "add"))
    	// új áru
    	{
    		p.parancs = 'a';
    		strcpy(p.nev, arunev);

    		if (sendto(clifd, &p, sizeof(p), 0, (struct sockaddr *) &srvinfo, sizeof(srvinfo)) < 0)
    		{
    			printf("A kuldes sikertelen.\n");
    			return 1;
    		}

    		recvfrom(clifd, &valasz_st, 1, 0, (struct sockaddr *) &srvinfo, &cli_len);

    		if (valasz_st == 'o')
    		{
    			printf("A hozzaadas sikeres.\n");
    		}
    		else
    		{
    			printf("A hozzaadas sikertelen, tele a raktar.\n");
    		}
    	}
    	// áru darabszám lekérése
    	else if (n == 2 && !strcmp(parancs, "list"))
    	{
    		p.parancs = 'c';
    		strcpy(p.nev, arunev);

    		if (sendto(clifd, &p, sizeof(p), 0, (struct sockaddr *) &srvinfo, sizeof(srvinfo)) < 0)
    		{
    			printf("A kuldes sikertelen.\n");
    			return 1;
    		}

    		recvfrom(clifd, &valasz_db, 4, 0, (struct sockaddr *) &srvinfo, &cli_len);

    		if (valasz_db == -1)
    		{
    			printf("Nincs ilyen aru.\n");
    		}
    		else
    		{
    			printf("Darabszam: %i\n", valasz_db);
    		}
    	}
    	// listázás
    	else if (n == 1 && !strcmp(parancs, "list"))
    	{
    		p.parancs = 'l';

    		if (sendto(clifd, &p, sizeof(p), 0, (struct sockaddr *) &srvinfo, sizeof(srvinfo)) < 0)
    		{
    			printf("A kuldes sikertelen.\n");
    			return 1;
    		}

    		recvfrom(clifd, &valasz_raktar, MAX_ARUK * sizeof(struct arucikk), 0, (struct sockaddr *) &srvinfo, &cli_len);
    		printf("Az aruk listaja:\n");

    		i = 0;
    		while (i < MAX_ARUK && valasz_raktar[i].darab != 0)
    		{
    			printf("%s: %i db\n", valasz_raktar[i].nev, valasz_raktar[i].darab);
    			++i;
    		}
    	}
    	else if (n == 1 && !strcmp(parancs, "end"))
    	{
    		close(clifd);
    		printf("Kapcsolat bontva.\n");
    		return 0;
    	}
    	else
    	{
    		printf("Ervenytelen parancs.\n");
    	}
    }
}