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

// nbytes = recvfrom(fd, buf, sizeof(buf), 0 /* flags */, (struct sockaddr*) &cli, &cli_len);
// sendto(sd, (char *)&current_time, (int)sizeof(current_time), 0, (struct sockaddr *)&client, client_length)

struct arucikk {
    char nev[28];
    int darab;
};

struct cli_parancs {
    char parancs;
    char nev[28];
};

struct arucikk raktar[MAX_ARUK];

void init()
{
    memset(raktar, 0, MAX_ARUK * sizeof(struct arucikk));

    raktar[0].darab = 5;
    strcpy(raktar[0].nev, "csoki");

    raktar[1].darab = 16;
    strcpy(raktar[1].nev, "toll");

    raktar[2].darab = 1;
    strcpy(raktar[2].nev, "ethernet-kartya");    
}

int feldolgozas(char * buf, int readbytes, int fd, struct sockaddr * clinfo, int cli_length)
{
    struct cli_parancs * p = (struct cli_parancs *) buf;

    int i; // melyik áruval fogunk dolgozni
    i = 0;

    if (p->parancs == 'a')
    // áru hozzáadása
    {
        while (i < MAX_ARUK
            && raktar[i].darab > 0
            && strcmp(raktar[i].nev, p->nev))
        {
            ++i;
        }

        if (i < MAX_ARUK)
        {
            strcpy(raktar[i].nev, p->nev);
            ++(raktar[i].darab);
            sendto(fd, "o", 1, 0, clinfo, cli_length); // ok
            printf("Uj aru: %s\n", p->nev);
        }
        else
        {
            sendto(fd, "e", 1, 0, clinfo, cli_length); // tele
            printf("Uj aru hozzaadasa sikertelen, tele a raktar.\n");
        }
    }
    // áru darabszámának lekérése
    else if (p->parancs == 'c' && p->nev[0] != 0)
    {
        while (i < MAX_ARUK && strcmp(raktar[i].nev, p->nev)) ++i;

        if (i < MAX_ARUK)
        {
            sendto(fd, &raktar[i].darab, sizeof(int), 0, clinfo, cli_length);
            printf("Aru darabszamanak lekererese: %s, %i\n", raktar[i].nev, raktar[i].darab);
        }
        else
        {
            i = -1;
            sendto(fd, &i, sizeof(int), 0, clinfo, cli_length);
            printf("Nem letezo aru darabszamanak lekerese: %s\n", p->nev);
        }
    }
    // árulista
    else if (p->parancs == 'l')
    {
        printf("Arulista\n");
        sendto(fd, raktar, MAX_ARUK * sizeof(struct arucikk), 0, clinfo, cli_length);
    }

    return 1;
}

int main(int argc, char *argv[])
{
    init();

    // socket

    int srvfd;
    srvfd = socket(AF_INET, SOCK_DGRAM, 0);

    // sockaddr_in

    struct sockaddr_in srvinfo;
    memset(&srvinfo, '\0', sizeof(srvinfo));

    srvinfo.sin_family = AF_INET;
    srvinfo.sin_port = htons(52943);
    srvinfo.sin_addr.s_addr = htonl(INADDR_ANY);

    // socket bindolása a structhoz

    bind(srvfd, (struct sockaddr *) &srvinfo, sizeof(srvinfo));

    // nézzük a beérkező adatokat

    struct sockaddr_in clinfo; // a küldő kliens infója
    socklen_t cli_len = sizeof(clinfo);
    char buf[CLI_BUF];         // a kliens által küldött adat
    int readbytes;             // hány bájtot olvastunk

    while (1)
    {
        // olvasunk adatot

        readbytes = recvfrom(srvfd, buf, CLI_BUF, 0, (struct sockaddr *) &clinfo, &cli_len);
        printf("Bejovo parancs: %s\n", inet_ntoa(clinfo.sin_addr));

        feldolgozas(buf, readbytes, srvfd, (struct sockaddr *) &clinfo, cli_len);
    }

    close(srvfd);

    return 0;
}