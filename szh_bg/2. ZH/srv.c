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

// egész->string: inet_ntoa(srv.sin_addr)
// string->egész: inet_addr(“157.181.161.32”)
// gethostbyname("domain")
//   srvinfo.sin_addr.s_addr = ((struct in_addr*)(hp->h_addr))->s_addr

// UDP-hez: SOCK_DGRAM

// send-recv ugyanúgy, csak egy 0 param a végére


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

int feldolgozas(char * buf, int readbytes, int fd)
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
            write(fd, "o", 1); // ok
            printf("Uj aru: %s\n", p->nev);
        }
        else
        {
            write(fd, "e", 1); // tele
            printf("Uj aru hozzaadasa sikertelen, tele a raktar.\n");
        }
    }
    // áru darabszámának lekérése
    else if (p->parancs == 'c' && p->nev[0] != 0)
    {
        while (i < MAX_ARUK && strcmp(raktar[i].nev, p->nev)) ++i;

        if (i < MAX_ARUK)
        {
            write(fd, &raktar[i].darab, sizeof(int));
            printf("Aru darabszamanak lekererese: %s, %i\n", raktar[i].nev, raktar[i].darab);
        }
        else
        {
            i = -1;
            write(fd, &i, sizeof(int));
            printf("Nem letezo aru darabszamanak lekerese: %s\n", p->nev);
        }
    }
    // árulista
    else if (p->parancs == 'l')
    {
        printf("Arulista\n");
        write(fd, raktar, MAX_ARUK * sizeof(struct arucikk));
    }
    // vége
    else
    {
        return 0;       
    }

    return 1;
}

int main(int argc, char *argv[])
{
    init();

    // socket

    int srvfd;
    srvfd = socket(AF_INET, SOCK_STREAM, 0);

    // sockaddr_in

    struct sockaddr_in srvinfo;
    memset(&srvinfo, '\0', sizeof(srvinfo));

    srvinfo.sin_family = AF_INET;
    srvinfo.sin_port = htons(52943);
    srvinfo.sin_addr.s_addr = htonl(INADDR_ANY);

    // socket bindolása a structhoz

    bind(srvfd, (struct sockaddr *) &srvinfo, sizeof(srvinfo));

    // listen

    listen(srvfd, 5); // hányan állhatnak sorban

    // fd_set-ek

    fd_set fds;         // az acceptált fd-k
    fd_set fds_avail;   // a select által visszaadott fd-k

    FD_ZERO(&fds);
    FD_ZERO(&fds_avail);
    FD_SET(srvfd, &fds);

    // nézzük a beérkező adatokat

    struct sockaddr_in clinfo; // a csatlakozó kliens infója
    socklen_t cli_len = sizeof(clinfo);
    char buf[CLI_BUF];         // a kliens által küldött adat
    int readbytes;             // hány bájtot olvastunk

    while (1)
    {
        // megnézzük, hogy a minket érdeklő socketeken (fds) hol van input (fds_avail)

        memcpy(&fds_avail, &fds, sizeof(fds));
        int sel;
        select(FD_SETSIZE, &fds_avail, NULL, NULL, NULL); // 3. írás, 4. error, 5. timeout

        // végigmegyünk az összes lehetséges fd-n, és amelyik be van állítva, feldolgozzuk

        int i;
        for (i = 0; i < FD_SETSIZE; ++i)
        {
            if (FD_ISSET(i, &fds_avail))
            {
                if (i == srvfd)
                // a szerver saját socketén jön adat -> connect kérelem
                {
                    // accept
                    int clifd;
                    clifd = accept(srvfd, (struct sockaddr *) &clinfo, &cli_len);

                    // beállítjuk az új fd-t
                    FD_SET(clifd, &fds);

                    printf("Uj kliens: %s\n", inet_ntoa(clinfo.sin_addr));
                }
                else
                // valamelyik már csatlakozott kliens küld adatot -> read
                {
                    readbytes = read(i, buf, CLI_BUF);

                    if (readbytes == 0)
                    // a kliens lecsatlakozott
                    {                        
                        close(i);
                        FD_CLR(i, &fds);
                        printf("EOT: %i\n", i);
                    }
                    else
                    // küldött adat feldolgozása
                    {
                        if (!feldolgozas(buf, readbytes, i))
                        {
                            close(i);
                            FD_CLR(i, &fds);
                            printf("Kliens oldalrol 'end': %i\n", i);
                        }
                    }
                }
            }
        }
    }

    close(srvfd);

    return 0;
}