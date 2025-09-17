#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../uinclude/client_functions.h"
#include "../uinclude/communication.h"

/* Client functions implementation */
int isValidFileName(const char *filename)
{
    // Check if the filename is empty
    if (filename[0] == '\0') {
        return 0;
    }

    // Check if the first character is a letter (a-zA-Z)
    if ((filename[0] < 'A' || (filename[0] > 'Z' && filename[0] < 'a') || filename[0] > 'z')) {
        return 0;
    }

    // Check the rest of the filename
    for (size_t i = 1; i < strlen(filename); i++) {
        char c = filename[i];
        if (!((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_' || c == '.')) {
            return 0;
        }
    }
    // If everything is good, then returns 1
    return 1;
}

int client_put(char* sendbuf, usercommand* cmd,int channel)
{   off_t file_size; //size of the file to put
    char filename[32]; // Name of the file to put
    unsigned int remain; // Size of data in the last packet
    unsigned int needed_pkts; // Amount of FULL packets needed to send a complete file

    memcpy(filename, cmd->param1, 32);
    filename[32]='\0';
     // Getting a file descriptor 
    int fd;
    fd = open(filename, O_RDONLY | O_SYNC); // Trying to open the file
    if(fd == -1){
        // Error handling
        //perror("unable to open the file"); 
        return -2;
    }
    // Getting file size
    file_size = lseek(fd, 0, SEEK_END); 
    lseek(fd, 0, SEEK_SET);
    if (file_size == -1)
    {
        // Error handling
        //perror("unable to get file size");
        close(fd); 
        return -8; 
    }

    needed_pkts = (file_size / MAX_DATA_SIZE); // Amount of FULL packets needed
    remain = file_size % MAX_DATA_SIZE; // Remaining data


    
    
    // We send needed_pkts amount of full packets...
    
    // (Won't start the loop if needed_pkts == 0)
    for(int i = 0; i < needed_pkts; i++)
    {
        // Filling in a full packet
        set_pkt_header(sendbuf, PUT, MAX_DATA_SIZE, filename, &file_size);
        if(!read(fd, sendbuf+HEADER_SIZE, MAX_DATA_SIZE))
        {
            //perror("Couldn't read file...");

            return -8;
        }

        if(!send_pkt(sendbuf, channel))
        {
            //fprintf(stderr, "Couldn't send packet at iteration %d", i);

            return -8;
        } 
    }

    // ...and a last one containing the last data IF NEEDED
    if (remain > 0)
    {
        set_pkt_header(sendbuf, PUT, remain, filename, &file_size);
        if(!read(fd, sendbuf+HEADER_SIZE, remain))
        {
            //perror("Couldn't read file...");

            return -8;
        }
        if(!send_pkt(sendbuf, channel))
        {
            //fprintf(stderr, "Couldn't send last packet...");

            return -8;
        }
    }
    
    // receive the answer of the server

    char recebuf[MAX_PACKET_SIZE];
    int is_received = recv_pkt(recebuf, channel);
    if (!is_received) return -8;

    // Error handling
    //error_hand(recebuf);

    /*if (recebuf[2] == 0)
        printf("Your file was put succesfully !");
    else
    {
        printf("Error ! Your file wasn't put.");
        return -10;
    }*/
    int err = 0;

    err = error_hand(recebuf);
    
    if (err < 0)
        return err;




    close(fd);
    return err;
}

int client_rm(char *sendbuf, usercommand *cmd, int channel)
{
    // Getting a file descriptor
    char *filename;
    filename = cmd->param1;
    set_pkt_header(sendbuf, 2, 0, filename, NULL);
    int err = 0;

    // try to send the packet
    int res = send_pkt(sendbuf, channel);
    if (!res) return -8;

    // receive the answer of the server

    char recebuf[MAX_PACKET_SIZE];
    int is_received = recv_pkt(recebuf, channel);
    if (!is_received) return -8;

    // Error handling
    err = error_hand(recebuf);
    if (err < 0)
        return err;
    
    return err;
}

int client_get(char* sendbuf, usercommand* cmd,int channel)
{   
    int err = 0;
    char localfilename[32];

    memcpy(localfilename, cmd->param2, 32);
    char filename[32]; //name of the file to get
    memcpy(filename, cmd->param1, 32);


    //creating the packet
    set_pkt_header(sendbuf, GET, 0, filename, NULL);


    if (!send_pkt(sendbuf, channel)) {//sending the packet
        fprintf(stderr, "Failed to send packet!\n");//handling error: packet not send
        return -10;  
    }


    char recebuf[MAX_PACKET_SIZE]; //receiving the packet
    int is_received = recv_pkt(recebuf, channel);
    if (!is_received) return -8;

    err = error_hand(recebuf);
    if (err < 0)
        return err;


    uint32_t file_size;//size of the file 
    memcpy(&file_size, recebuf + 37, sizeof(uint32_t));//



    int needed_pkts = (file_size / MAX_DATA_SIZE); // Amount of FULL packets needed
    int remain = file_size % MAX_DATA_SIZE; // Remaining data


    if (access(localfilename, F_OK) == 0) {
        return -3;
    }
    // Open the file for writing
    int fd = open(localfilename, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);

    //receive and store data until the whole file is received
    for(int i = 0; i < needed_pkts; i++)
    {
        ssize_t bytes_written = write(fd,recebuf+69 , MAX_DATA_SIZE);
        int is_received = recv_pkt(recebuf, channel);
        if (!is_received) return -8;
    }

    // ...and a last one containing the last data IF NEEDED
    if (remain > 0)
    {   
        ssize_t bytes_written = write(fd,recebuf+69 , remain);
    }
    close (fd);

    return err;
}

// This function should permit to read the data and print it

void read_write(char *buf, int comma, int size)
{
    for (int j = 0 ; j < size ; j++  )
        { 
            while (buf[j] != ',' && j < size )
            {
                printf("%c", buf[j]);
                j++;
            }
            if (buf[j]== ',')           // in order to got to the newline for new files and tab twice when it comes to sizes of the files 
            {
                comma++;
                if ((comma%2))
                    printf("\t\t");
                else
                    printf("\n");
            }
        }
    printf("\n");
}

int client_ls(char *sendbuf, int channel)
{
    set_pkt_header(sendbuf, 4, 0, NULL, NULL);
    int err = 0;
    int res = send_pkt(sendbuf, channel);               
    if (!res) return -8;
    
    // receive the packets sent by the server
    char recebuf[MAX_PACKET_SIZE];
    char recebuf2[MAX_DATA_SIZE];
    
    int is_received = recv_pkt(recebuf, channel);
    if (!is_received) return -8;
    
    // Error handling
    err = error_hand(recebuf);
    if (err < 0)
        return err;

    unsigned int nb_packets;                        // 2^32 is already a huge number
    memcpy(&nb_packets, recebuf+5, 4);

    uint16_t size = getDataSize(recebuf); 
    memcpy(recebuf2, &recebuf[69], size);
    
    int comma = 0;
    
    read_write(recebuf2, comma, size);

    // if there are many packets

    if (nb_packets > 1 )
    {
        for (int k = 1; k < nb_packets; k++)
        {
            int is_received = recv_pkt(recebuf, channel);
            if (!is_received) return -8;
            
            // Error handling
            err = error_hand(recebuf);
            if (err < 0)
                return err;

            size = getDataSize(recebuf);
            memcpy(recebuf2, &recebuf[69], size);
            
            read_write(recebuf2, comma, size);
            
        }
    }
return err;
}


// This function should permit to read the data and print it

void read_write2(char *recebuf2, int nb_lines, int *rlines, int size)
{   
    for (int i = 0 ; i < size ; i++  )
    {
        while (recebuf2[i] != '\n'&& (*rlines) < nb_lines && i < size )
        {
            printf("%c", recebuf2[i]);
            i++;
        }
        if (recebuf2[i]== '\n')           // in order to got to the newline for a new line
        {
            (*rlines)++;
            printf("\n");
        }
    }
}

int client_cat(char* sendbuf, usercommand* cmd, int channel)
{   
    
    unsigned int nb_lines; //size of the file 
    nb_lines = atoi(cmd->param2);
    set_pkt_header(sendbuf, 5, 0, cmd->param1, &nb_lines);

    int res = send_pkt(sendbuf, channel);               
    if (!res) return -8;

    // receive the packets sent by the server
    char recebuf[MAX_PACKET_SIZE];
    char recebuf2[MAX_DATA_SIZE];
    
    int is_received = recv_pkt(recebuf, channel);
    if (!is_received) return -8;

    // Error handling
    int err = error_hand(recebuf);
    if (err < 0)
        return err;

    unsigned int nb_packets;                        // 2^32 is already a huge number
    memcpy(&nb_packets, recebuf+5, 4); 
    
    
    uint16_t size = getDataSize(recebuf);
    
    memcpy(recebuf2, &recebuf[69], size);
    
    int lines = 0;
    
    read_write2(recebuf2, nb_lines, &lines, size);
    
    // if there are many packets

    if (nb_packets > 1 )
    {
        for (int k = 1; k < nb_packets; k++)
        {
            int is_received = recv_pkt(recebuf, channel);
            if (!is_received) return -8;
            
            // Error handling
            err = error_hand(recebuf);
            if (err < 0)
                return err;
            
            size = getDataSize(recebuf);
            memcpy(recebuf2, &recebuf[69], size);
            
            read_write2(recebuf2, nb_lines, &lines, size);
        }
    }
if (nb_lines > lines)
    printf(" @ warning: response contains less than %d complete lines\n", nb_lines);
return err;


}


int client_cp(char* sendbuf, usercommand* cmd, int channel)
{   int err = 0;
    char filename[32];
    char newfilename[32];

    memcpy(filename, cmd->param1, 32);
    memcpy(newfilename, cmd->param2, 32);

    set_pkt_header(sendbuf, 6, 0, filename, newfilename);

    // try to send the packet
    int res = send_pkt(sendbuf, channel);
    if (!res)
        return err;

    // receive the answer of the server

    char recebuf[MAX_PACKET_SIZE];
    int is_received = recv_pkt(recebuf, channel);
    if (!is_received)
        return -8;

    // Error handling
    //error_hand(recebuf);

    err = error_hand(recebuf);
    if (err < 0)
        return err;

    /*if (recebuf[2] == 0)
        printf("Your file was copied succesfully !");
    else
    {
        printf("Error ! Your file wasn't copied.");
        return 1;
    }*/

    return err;
}

// print the command options and command constraints

int client_help()
{
    printf("\033[1mCOMMANDS ARE :\033[0m");

    printf("\n\033[4mput\033[0m  :  \033[1mput filename\033[0m   :  put permits to add the referenced local file to the remote drive\n\n");

    printf("\033[4mrm\033[0m  :  \033[1mrm filename\033[0m  :  rm permits to remove the referenced file from the remote drive\n\n");

    printf("\033[4mget\033[0m  :  \033[1mget filename localfilename\033[0m  :  get permits to locally store a file available remotely\n\n");

    printf("\033[4mls\033[0m  :  \033[1mls\033[0m  :  ls permits to list remote files\n\n");

    printf("\033[4mcat\033[0m  :  \033[1mcat filename n\033[0m  :  cat permits to print the first n lines of a remote file\n\n");

    printf("\033[4mcp\033[0m  :  \033[1mcp originfilename destinationfilename\033[0m  :  cp permits to duplicate a remote file\n\n");

    printf("\033[4mquit\033[0m  or \033[4mexit\033[0m  :  \033[1mquit\033[0m or \033[1mexit\033[0m   :  quit or exit permits the client to exit\n\n");

    printf("\033[4mrestart\033[0m  :  \033[1mrestart\033[0m   :  restart permits the client to reinitialize or reset the connection with the server\n\n");

    printf("\033[4mhelp\033[0m  :  \033[1mhelp\033[0m   :  help describes the available commands\n\n");

    printf("\033[4manalyze\033[0m      :  set printing message mode to analyze\n\n\
\033[4minteractive\033[0m  :  set printing message mode to interactive\n\n\
\033[4mpkt\033[0m          :  toggles on/off the printing of packets)\n\n");

    printf("\033[1mCOMMAND CONSTRAINTS :\033[0m\n\n");

    printf("    - A file name must not be longer than 31 characters. It\n\
    must start with a character between 'a' and 'z' or\n\
    'A' and 'Z'. Then, it can contain only alphanumerical\n\
    characters, and '_' and '.'\n\
    - file size must not be greater than 4294967295\n\
    - cat does not accept more than 1000 lines\n\
    - overwriting file is forbidden and causes an error\n");

    return 0;
    
}

