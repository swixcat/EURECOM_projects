
// INCLUDES
/* to use the provided parse_commandline function. */
#include "../include/utilities.h"
/* user defined library for sending and receiving packets */
#include "../uinclude/communication.h"
/* for stdin,...*/
#include <stdio.h>
/* for memcpy,...*/
#include <string.h>
/* to modify SIGPIPE signal handling, as default behaviour makes
 * the program exit when trying to write to a closed socket. 
 * We don't want this.
 */
#include <signal.h>

#include "../uinclude/client_functions.h"

#include <dirent.h>


int student_client(int channel, int argc, char *argv[]) {
    // Writing to a closed socket causes a SIGPIPE signal, which makes 
    // the program exit. The following line inhibits this default behaviour.
    // Then, these problematic writes will simply return -1 with the EPIPE
    // error in errno and not cause an exit. 
    // (cf the line with "EPIPE" in send_pkt in usrc/communication.c).
    signal(SIGPIPE, SIG_IGN);

    //buffer to receive the command line
    char cmdline[128];

    //buffer to build the packet to send (max size: 81)
    char sendbuf[4096];

    // structure to fill with parse_commandline
    usercommand parsed_cmd;


    // Options flags
    int analyze_flag = 0;
    int interactive_flag = 0;
    int directory_flag = 0;

    // Directory to be used for client side files
    char directory[128] = "";  

    // filename for the analyze option
    char analyze_filename[128];

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-analyze") == 0) {
            if (analyze_flag) {
                // Option provided more than once, exit immediately
                printf("Error: -analyze option provided more than once.\n");
                return 0;
            }
            analyze_flag = 1;

            // Execute the command from the file specified in the next argument
            if (i + 1 < argc) {
                memcpy(analyze_filename,argv[i+1],128);
            } 
            else {
                printf("Error: -analyze option requires a file argument.\n");
                return 0;
            }
        } 
        else if (strcmp(argv[i], "-interactive") == 0) {
            if (interactive_flag) {
                // Option provided more than once, exit immediately
                printf("Error: -interactive option provided more than once.\n");
                return 0;
            }
            interactive_flag = 1;

        } else if (strcmp(argv[i], "-directory") == 0) {
            if (directory_flag) {
                // Option provided more than once, exit immediately
                printf("Error: -directory option provided more than once.\n");
                return 0;
            }
            directory_flag = 1;

            // Check if a directory is specified in the next argument
            if (i + 1 < argc) {
                // Copy the directory path
                memcpy(directory, argv[i + 1], sizeof(directory) - 1);
            } else {
                printf("Error: -directory option requires a directory argument.\n");
                return 0;
            }
        }
    }

    
    if (analyze_flag)
    {
        FILE *file = fopen(analyze_filename, "r");

        if (!file) {
            perror("Error opening file");
            return 0;
        }

        chdir(directory);

        while (fgets(cmdline, sizeof(cmdline), file) != NULL) {
            // Remove trailing newline character
            
            size_t len = strlen(cmdline);
            if (len > 0 && cmdline[len - 1] == '\n') {
                cmdline[len - 1] = '\0';
            }


            if (strlen(cmdline) == 0) {
                fprintf(stdout, "\n");
                continue;}

            // parse it
            int test = parse_commandline(&parsed_cmd, cmdline);
            if (test == 0){
                fprintf(stdout, "KO -6\n");
                continue;
            }

            printf("%s", cmdline);
            fprintf(stdout, "\n");
            if (test) { // parsing successful
                int err;
                

                if ( strcmp(parsed_cmd.cmd,"put") == 0){
                    err = client_put(sendbuf, &parsed_cmd,channel);
    
                    }

                else if ( strcmp(parsed_cmd.cmd,"rm") == 0){
                    err = client_rm(sendbuf, &parsed_cmd, channel);

                    }

                else if ( strcmp(parsed_cmd.cmd,"get") == 0){
                    err = client_get(sendbuf, &parsed_cmd,channel);

                    }

                else if ( strcmp(parsed_cmd.cmd,"ls") == 0){
                    err = client_ls(sendbuf, channel);

                    }

                else if ( strcmp(parsed_cmd.cmd,"cat") == 0){
                    err = client_cat(sendbuf, &parsed_cmd, channel);
                    }

                else if ( strcmp(parsed_cmd.cmd,"cp") == 0){
                    err = client_cp(sendbuf, &parsed_cmd,channel);
                    }

                else if ( strcmp(parsed_cmd.cmd,"restart") == 0){
                    return 1;
                }

                else if ( strcmp(parsed_cmd.cmd,"help") == 0){
                    client_help(&parsed_cmd);
                }


                // This part will deal with error codes that can potentially lead to the "KO x message"


                if (err < 0)
                    fprintf(stdout, "KO %d\n", err);
                
                if (err >= 0)
                    printf("OK\n");

                if (err == -1 || err == -7 || err == -8 ){
                    fclose(file); 
                    return 0;
                }

                else if (( strcmp(parsed_cmd.cmd,"quit") == 0) ) {
                    fclose(file); 
                    return 0;
                }

            }

        }  
        fclose(file);

    }


    if (interactive_flag || (analyze_flag == 0))
    {
    // print info to terminal
    printf("(^C to exit)\n\n");
    // infinite loop -> use ^C to exit the program 
    while (1) {
        // get the command from user, exit if it fails
        printf("type a command > ");
        if(! fgets(cmdline, 128, stdin)){
            printf("cannot read command line\n");
            // return 0 to exit
            return 0;
        }

        chdir(directory);
        // parse it
        int test = parse_commandline(&parsed_cmd, cmdline);
        if (test) { // parsing successful
            int err;

            if ( strcmp(parsed_cmd.cmd,"put") == 0){
                err = client_put(sendbuf, &parsed_cmd,channel);
 
                }

            else if ( strcmp(parsed_cmd.cmd,"rm") == 0){
                err = client_rm(sendbuf, &parsed_cmd, channel);

                }

            else if ( strcmp(parsed_cmd.cmd,"get") == 0){
                err = client_get(sendbuf, &parsed_cmd,channel);

                }

            else if ( strcmp(parsed_cmd.cmd,"ls") == 0){
                err = client_ls(sendbuf, channel);

                }

            else if ( strcmp(parsed_cmd.cmd,"cat") == 0){
                err = client_cat(sendbuf, &parsed_cmd, channel);
                }

            else if ( strcmp(parsed_cmd.cmd,"cp") == 0){
                err = client_cp(sendbuf, &parsed_cmd,channel);
                }

            // This part will deal with error codes that can potentially lead to the "KO x message"

            if (err < 0)
                fprintf(stderr, "KO %d\n", err);
            
            if (err == -1 || err == -7 || err == -8 )
                return 0;
            
            if (err >= 0)
                printf("OK\n");

            else if ( strcmp(parsed_cmd.cmd,"help") == 0){
                client_help();
                }

            else if ( strcmp(parsed_cmd.cmd,"restart") == 0){
                return 1;
                }

            else if (( strcmp(parsed_cmd.cmd,"quit") == 0) ||( strcmp(parsed_cmd.cmd,"exit"))) {
                return 0;
                }

            // 3. try to send the packet

            /* NOTE FROM KHADIM : I'm testing some stuff here since the provided client don't work on my computer :)
             * Don't worry, I know what I'm doing.
             * Ask me if you have any questions :))
             */
            /*sendbuf[0] = 'E';
            sendbuf[1] = 'D';
            sendbuf[2] = 1;
            int res = send_pkt(sendbuf, channel);
            */
            // return 1 to restart if somme communication error occured
            //return 1;  

        }  
    }
    }
return 0;
}
