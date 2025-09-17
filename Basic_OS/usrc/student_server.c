// INCLUDES
/* user defined library for sending and receiving packets */
#include "../uinclude/communication.h"
/* for printf,...*/
#include <stdio.h>
/* to modify SIGPIPE signal handling, as default behaviour makes
 * the program exit when trying to write to a closed socket. 
 * We don't want this.
 */
#include <signal.h>

#include "../uinclude/server_functions.h"
#include <stdlib.h>

// "return makes the server wait for next client."
void student_server(int channel, int argc, char *argv[]) {
    // Writing to a closed socket causes a SIGPIPE signal, which makes 
    // the program exit. The following line inhibits this default behaviour.
    // Then, these problematic writes will simply return -1, put the EPIPE
    // in errno, and not cause an exit. 
    // (cf the line with "EPIPE" in send_pkt in usrc/communication.c).
    signal(SIGPIPE, SIG_IGN);

    // Default values
    size_t quotasize = 4000000000; // To store the maximum number of bytes (set from cmdline)
    int quotanumber = 1000; // ...the maximum number of files (set from cmdline)

    size_t total_bytes = 0; // To store the maximum number of bytes
    int nb_files = 0; // ...the maximum number of files


    printf("argc : %d\n", argc);
    if(argc > 1)
    {
        for(int i = 1; i < argc; i++)
        {
            if(strcmp(argv[i], "-quotasize") == 0)
            {
                // We use strtoul() to get the number (which can be big)
                quotasize = strtoul(argv[i+1], NULL, 10);
                if(quotasize == 0 || errno == EINVAL || errno == ERANGE)
                {
                    fprintf(stderr, "Wrong number after -quotasize option.");
                    return;
                }
            }
            else if(strcmp(argv[i], "-quotanumber") == 0)
            {
                quotanumber = atoi(argv[i+1]);
                if(quotanumber == 0)
                {
                    fprintf(stderr, "Wrong number after -quotasize option.");
                    return;
                }
            }
            else if(strcmp(argv[i], "-directory") == 0)
            {
                chdir(argv[i+1]);
            }
            else
            {
                //Ignoring argvs otherwise
                //fprintf(stderr, "Format : -quotasize <int> -quotanumber <int> -directory <int>\n");
                //return;
            }
        }

        printf("Quotanumber : %d \n", quotanumber);
        printf("Quotasize : %ld \n", quotasize);
    }

    //buffer to receive packets (max size: MAX_PACKET_SIZE)
    char recvbuf[MAX_PACKET_SIZE];
    char err_pkt[HEADER_SIZE];

    while (1) {
        // get the command from user, exit if it fails
        printf(" -- wait a packet (^C to exit) --\n");
        if (!recv_pkt(recvbuf, channel))
        {
            //printf("fail...\n");
            break;
        }

        get_dir_stats(".", &total_bytes, &nb_files);
        printf("Bytes : %ld, number of files : %d\n", total_bytes, nb_files);
        printf("Quotanumber : %d \n", quotanumber);
        printf("Quotasize : %ld \n", quotasize);

        //printf("Here is the packet I received : %s [END] \n", recvbuf);
        int cmd = recvbuf[2]; // To decide which funtion to call

        unsigned int file_size;
        memcpy(&file_size, recvbuf+37, 4);
        printf("FILE SIZE : %d\n", file_size);

        switch(cmd)
        {
            case PUT:
                printf("[--- PUT :) ---]\n");
                if((total_bytes + file_size < quotasize) && (nb_files < quotanumber))
                {
                    server_put(recvbuf, channel);
                }
                else
                {
                    set_pkt_header(err_pkt, QUOTA, 0, NULL, NULL);
                    send_pkt(err_pkt, channel);
                }
            break;

            case REMOVE:
                printf("[--- Remove >:) ---]\n");
                server_remove(recvbuf, channel);
                break;

            case GET:
                printf("[--- GET :O ---]\n");
                server_get(recvbuf, channel);
                break;

            case LIST:
                printf("[--- ~ LS ~ ---]\n");
                server_list(recvbuf, channel);
                break;

            case PRINT:
                printf("[--- CAAAAT meow :3 ---]\n");
                server_cat(recvbuf, channel);
                break;

            case COPY:
                if((total_bytes < quotasize) && (nb_files < quotanumber))
                    server_cp(recvbuf, channel, quotasize, total_bytes);
                else
                {
                    set_pkt_header(err_pkt, QUOTA, 0, NULL, NULL);
                    send_pkt(err_pkt, channel);
                }
            break;

            default:
                printf("Unrecognised command !\n");
            break;
        }
    }
}

