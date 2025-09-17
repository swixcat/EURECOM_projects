#include "../uinclude/server_functions.h"
#include "../uinclude/communication.h"
#include "../include/utilities.h"
#include <sys/types.h>
#include <sys/stat.h> // for lstat
#include <unistd.h>

//#define _DEFAULT_SOURCE // In order to use the DT_* constants
#include <dirent.h>

#define MAX_FILE_COUNT 10

/* Server functions implementation */

int get_dir_stats(char* dirname, size_t* amount_bytes, int* nb_files)
{
    int fd; // To handle files of a directory
    char* filename; // To store filenames
    size_t total_size = 0;

    int nb_reg_files = 0; // To count the number of regular files
    struct stat file_stat; // To store stats about a file (especially its type)
    struct dirent *entry; // To handle a directory entry

    DIR *dir = opendir(dirname);

    if (dir == NULL)
    {
        fprintf(stderr, "error oppening the directory");
        return -1;
    }

    // Getting through all directory entries
    while ((entry = readdir(dir)) != NULL)
    {
        // Openning the file with filename and checking for success
        filename = entry->d_name;
        fd = open(filename, O_RDONLY | O_SYNC);
        if(fd < 0)
        {
            perror("error oppening the file in directory");
            return -1;
        }

        // Getting stats about the file (especially its type)
        fstat(fd, &file_stat);

        // We use the POSIX macro S_ISREG to test wether the current file is regular or not
        // We also check the validity of the filename
        if (S_ISREG(file_stat.st_mode) && isValidFileName(filename))
        {
            nb_reg_files++;
            total_size += file_stat.st_size;
        }
        close(fd);
    }

    *amount_bytes = total_size;
    *nb_files = nb_reg_files;
    return 1;
}

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

int checkFile(const char* filename) {
    if (access(filename, F_OK) != -1) {
        // File exists
        return 0;
    } else {
        // File does not exist
        return -1;
    }
}

size_t bytes_for_n_lines(int fd, int nb)
{
    int amount; // Amount of bytes read by a call to read()
    int i = 0; // Lines read
    char c = 0; // To check actual char
    size_t bytes = 0; // Total amount of bytes read

    while (i < nb)
    {
        amount = read(fd, &c, 1);
        if(amount == -1)
            return -1;
        else if(amount == 0)
            break;
        else
        {
            bytes++;
            if(c == '\n')
                i++;
        }
    }

    return bytes;
}

void server_cat(char* pkt, int channel)
{
    char res_pkt[HEADER_SIZE]; // Response packet (for errors and stuff)
    unsigned int nb_of_lines; // -> from packet
    char filename[32]; // -> from packet

    int fd; // File descriptor

    size_t bytes_needed;
    uint16_t remain; // Size of data in the last packet
    unsigned int needed_pkts; // Amount of FULL packets needed
    unsigned int total; // Total amount of packets needed

    memcpy(filename, pkt+5, 32);
    memcpy(&nb_of_lines, pkt+37, 32); // copying the number of lines

    printf("Filename : %s\n", filename);
    for(int i = 0; i<32; i++)
    {
        printf("%d ~ ", filename[i]);
    }
    printf("\n");

    // Checking the filename
    if(!isValidFileName(filename))
    {

        fprintf(stderr, "Incorrect filename format !\n");
        set_pkt_header(res_pkt, FORMAT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        return;
    }

    // Checks for existence (file)
    if(checkFile(filename) == -1)
    {
        set_pkt_header(res_pkt, MISS, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "File doesn't exist");
        return;
    }

    // Trying to open the file
    fd = open(filename, O_RDONLY | O_SYNC);
    if(fd == -1)
    {
        perror("Cannot open file");
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        return;
    }

    // Computing the needed amount of bytes for nb_of_lines lines
    bytes_needed = bytes_for_n_lines(fd, nb_of_lines);
    if (bytes_needed < 0)
    {
        fprintf(stderr, "Incorrect number of bytes !\n");
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        close(fd);
        return;
    }
    else
    {   // We replace the file cursor at the beginning (because it has been modified by bytes_for_n_lines)
        lseek(fd, 0, SEEK_SET);
        printf("%ld needed bytes for %d lines\n", bytes_needed, nb_of_lines);
    }

    // Computing packets informations (about their number)
    needed_pkts = bytes_needed / MAX_DATA_SIZE;
    remain = bytes_needed % MAX_DATA_SIZE;
    total = needed_pkts + (remain == 0 ? 0 : 1);

    // Sending full packets...
    set_pkt_header(pkt, PRINT, MAX_DATA_SIZE, &total, NULL); // No need to fill in the packet's header at each iteration
    for(int i = 0; i < needed_pkts; i++)
    {
        printf("Ahhh... Entered loop\n");
        if(!read(fd, pkt+HEADER_SIZE, MAX_DATA_SIZE))
        {
            perror("Couldn't read file...");
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            send_pkt(res_pkt, channel);
            close(fd);
            return;
        }
        send_pkt(pkt, channel);
    }

    // ...and what remains if necessary
    if(remain > 0)
    {
        printf("Last packet. Remaining bytes : %d\n", remain);
        set_pkt_header(pkt, PRINT, remain, &total, NULL);
        if(!read(fd, pkt+HEADER_SIZE, remain))
        {
            perror("Couldn't read file for last packet...");
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            send_pkt(res_pkt, channel);
            close(fd);
            return;
        }
        printf("--> Huh, packet : %s\n", pkt+HEADER_SIZE);
        send_pkt(pkt, channel);
    }

    close(fd);
}

void server_get(char *pkt, int channel)
{ 
    char res_pkt[HEADER_SIZE]; // Response packet (for errors and stuff)
    char filename[32]; // Name of the file to get
    off_t file_size; // Size of the file to get
    int fd; // File descriptor

    unsigned int remain; // Size of data in the last packet
    unsigned int needed_pkts; // Amount of FULL packets needed to send a complete file

    // I assume that option1 is well filled in (with '\0' at the end). That's a job for client team !
    memcpy(filename, pkt+5, 32); // To get the file's name from the packet

    /* From now on, we don't need the packet's data anymore, so we'll use it to write
    * and send future packets. Doing so, we won't have to allocate more memory as
    * we already have a pointer. Nice !
    */

    // Checks if filename is valid
    if(!isValidFileName(filename))
    {
        fprintf(stderr, "Wrong filename format !");
        set_pkt_header(res_pkt, FORMAT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        return;
    }

    // Checks for existence (file)
    if(checkFile(filename) == -1)
    {
        set_pkt_header(res_pkt, MISS, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "File doesn't exist");
        return;
    }

    fd = open(filename, O_RDONLY | O_SYNC); // Trying to open the file
    if(fd == -1)
    {
        perror("Cannot open file.");
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        return;
    }

    file_size = lseek(fd, 0, SEEK_END); // We compute the file's size
    if(file_size == -1)
    {
        perror("lseek() problem, thus cannot get file size.");
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        return;
    }
    else // If file_size is correct, we move the file cursor to the beginning agian
        lseek(fd, 0, SEEK_SET);

    needed_pkts = (file_size / MAX_DATA_SIZE); // Amount of FULL packets needed
    remain = file_size % MAX_DATA_SIZE; // Remaining data

    // We send needed_pkts amount of full packets...
    // (Won't start the loop if needed_pkts == 0)
    for(int i = 0; i < needed_pkts; i++)
    {
        // Filling in a full packet
        set_pkt_header(pkt, GET, MAX_DATA_SIZE, filename, &file_size);
        if(!read(fd, pkt+HEADER_SIZE, MAX_DATA_SIZE))
        {
            perror("Couldn't read file...");
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            send_pkt(res_pkt, channel);
            return;
        }

        if(!send_pkt(pkt, channel))
        {
            fprintf(stderr, "Couldn't send packet at iteration %d", i);
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            send_pkt(res_pkt, channel);
            return;
        } 
    }

    // ...and a last one containing the last data IF NEEDED (if remain equals 0, needed_pkts is a multiple of 4027)
    if (remain > 0)
    {
        set_pkt_header(pkt, GET, remain, filename, &file_size);
        // Reads file for the last packet and handle errors
        if(!read(fd, pkt+HEADER_SIZE, remain))
        {
            perror("Couldn't read file...");
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            send_pkt(res_pkt, channel);
            return;
        }
        // Sends last packet and handles errors
        if(!send_pkt(pkt, channel))
        {
            fprintf(stderr, "Couldn't send last packet...");
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            send_pkt(res_pkt, channel);
            return;
        } 
    }
}

void server_put(char *pkt, int channel) {
    char filename[32];
    char response_pkt[HEADER_SIZE];
    uint32_t file_size;
    
    // Extract information from the received packet
    memcpy(filename, pkt + 5, 32);
    memcpy(&file_size, pkt + 37, sizeof(uint32_t));

    // Check if the filename is valid
    if (!isValidFileName(filename)) {
        fprintf(stderr, "Invalid filename format!\n");
        set_pkt_header(response_pkt, FORMAT, 0, NULL, NULL);

        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
        }
            return;
        }

    // Check if the file already exists
    if (checkFile(filename) == 0) {
        fprintf(stderr, "File already exists!\n");
        set_pkt_header(response_pkt, EXISTS, 0, NULL, NULL);

        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
        }
        return;
    }

    // Open the file for writing
    int fd = open(filename, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
    if (fd == -1) {
        perror("Cannot open file");
        set_pkt_header(response_pkt, ABORT, 0, NULL, NULL);

        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
        }
        return;
    }

    int needed_pkts = (file_size / MAX_DATA_SIZE); // Amount of FULL packets needed
    int remain = file_size % MAX_DATA_SIZE; // Remaining data

    set_pkt_header(response_pkt, 0, 0, NULL, NULL);
    if (!send_pkt(response_pkt, channel)) {
        fprintf(stderr, "Failed to send response packet!\n");
        return;
    }


    for(int i = 0; i < needed_pkts; i++)
    {
        write(fd,pkt+69 , MAX_DATA_SIZE);
        int is_received = recv_pkt(pkt, channel);
        if (!is_received) return;
    }

    // and a last one containing the last data IF NEEDED
    if (remain > 0)
    {   
        write(fd,pkt+69 , remain);
    }
    close (fd);
    if(needed_pkts>1){
        // Send a response packet indicating success (code 0)
        set_pkt_header(response_pkt, 0, 0, NULL, NULL);
        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
            return;
    }
    }
    return;
}

void server_list(char *pkt, int channel)
{
    char rpkt[HEADER_SIZE]; // Error response packet
    int fd; // To handle files of a directory
    char* filename; // To store filenames
    size_t file_size;
    int nb_reg_files = 0; // To count the number of regular files
    struct stat file_stat; // To store stats about a file (especially its type)
    struct dirent *entry; // To handle a directory entry

    int totalPackets; // Total amount of packets to send
    char entry_str[512]; // To store the "filename,size" string of the actual entry

    size_t buffer_size = 512; // Size of lsstring, used for reallocation if needed
    char *lsstring = (char *)malloc(buffer_size); // The string on which we call sort_dir()
    lsstring[0] = '\0'; // For strcat() to work properly as it erase the null terminator

    // Oppening diectory and cheking for success
    DIR *dir = opendir(".");
    if (dir == NULL)
    {
        set_pkt_header(rpkt, ABORT, 0, NULL, NULL);
        if (!send_pkt(rpkt, channel))
        {
            fprintf(stderr,"error sending the error packet");
        }
        fprintf(stderr, "error oppening the directory");
        return;
    }

    // Getting through all directory entries
    while ((entry = readdir(dir)) != NULL)
    {
        // Openning the file with filename and checking for success
        filename = entry->d_name;
        fd = open(filename, O_RDONLY | O_SYNC);
        if(fd < 0)
        {
            set_pkt_header(rpkt, ABORT, 0, NULL, NULL);
            if (!send_pkt(rpkt, channel))
            {
                fprintf(stderr,"error sending the error packet");
            }
            perror("error oppening the file in directory");
            return;
        }

        // Getting stats about the file (especially its type)
        fstat(fd, &file_stat);

        // We use the POSIX macro S_ISREG to test wether the current file is regular or not
        // We also check the validity of the filename
        if (S_ISREG(file_stat.st_mode) && isValidFileName(filename))
        {
            file_size = lseek(fd, 0, SEEK_END); // We don't check for errors as we will witness them later
            if(nb_reg_files == 0)
                snprintf(entry_str, 512, "%s,%ld", filename, file_size);
            else
                snprintf(entry_str, 512, ",%s,%ld", filename, file_size);

            // Check if there is enough space in lsstring, if not, reallocate
            if (strlen(lsstring) + strlen(entry_str) + 1 > buffer_size)
            {
                printf("> Reallocation needed for buffer...\n");
                buffer_size *= 2;
                lsstring = (char *)realloc(lsstring, buffer_size);
                printf("> Done\n");
            }

            // Concatenate the entry to lsstring
            strcat(lsstring, entry_str);
            //printf("lsstring : %s", lsstring);
            nb_reg_files++;
        }
        close(fd);
    }

    closedir(dir);

    // If there is no packets
    if(nb_reg_files == 0)
    {
        totalPackets = 1;
        set_pkt_header(rpkt, LIST, 0, &totalPackets, NULL);
        send_pkt(rpkt, channel);
        free(lsstring);
        return;
    }

    // Sorting by alphanumerical order
    printf("ls string : %s\n", lsstring);
    if(nb_reg_files > 1)
    {
        sort_dir(lsstring);
        printf("Sorted ls string : %s\n", lsstring);
    }
    
    // Sending all packets
    totalPackets = (strlen(lsstring) / MAX_DATA_SIZE) + (strlen(lsstring) % MAX_DATA_SIZE != 0);
    printf("Total packets to send : %d\n", totalPackets);
    
    for (int i = 0; i < totalPackets; i++) {
        // Calculate the number of characters to include in this packet
        int charsInThisPacket = (i == totalPackets - 1) ? strlen(lsstring) % MAX_DATA_SIZE : MAX_DATA_SIZE;

        // Allocate space for the response packet
        char response_pkt[MAX_PACKET_SIZE];

        // Set the packet header appropriately
        set_pkt_header(response_pkt, LIST, charsInThisPacket, &totalPackets, NULL);

        // Copy the directory string to the response packet
        memcpy(response_pkt + HEADER_SIZE, lsstring + i * MAX_DATA_SIZE, charsInThisPacket);
        // Send the response packet
        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
        }
    }

    free(lsstring);
    return;
}

void server_cp(char* pkt, int channel, size_t quotasize, size_t total_bytes)
{
    char res_pkt[HEADER_SIZE]; // Response packet (for errors and stuff)
    char filename[32]; // Name of the file to copy
    char copy_name[32]; // Name of the copy
    int fd_file; // File descriptor (file)
    int fd_copy; // File descriptor (copy)
    char buf[4096]; // A buffer to copy content

    off_t amount_to_read; // File size, then decrease
    int amount_read;
    int amount_written;

    // Getting the filenames
    memcpy(filename, pkt+5, 32);
    memcpy(copy_name, pkt+37, 32);

    //printf("1:%s 2:%s\n", filename, copy_name);

    set_pkt_header(res_pkt, 0, 0, NULL, NULL);

    // Checks for existence (file)
    if(checkFile(filename) == -1)
    {
        set_pkt_header(res_pkt, MISS, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "File doesn't exist");
        return;
    }

    // Checks for existence (copy)
    if(checkFile(copy_name) == 0)
    {
        set_pkt_header(res_pkt, EXISTS, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "File exists, overwrite forbidden !");
        return;
    }

    // Checks for filename validity
    if(!isValidFileName(filename) || !isValidFileName(copy_name))
    {
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "Incorrect filename");
        return;
    }

    // Tries to open files
    if((fd_file = open(filename, O_RDONLY | O_SYNC)) < 0)
    {
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "Cannot open file to copy");
        return;
    }

    if((fd_copy = open(copy_name, O_WRONLY | O_CREAT, 00644)) < 0)
    {
        set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "Cannot create copy");
        return;
    }

    amount_to_read = lseek(fd_file, 0, SEEK_END);

    // QUOTA HANDLING BRRR
    if(amount_to_read + total_bytes > quotasize)
    {
        close(fd_copy);
        close(fd_file);
        unlink(copy_name);
        set_pkt_header(res_pkt, QUOTA, 0, NULL, NULL);
        send_pkt(res_pkt, channel);
        fprintf(stderr, "Quota exceeded !");
    }

    lseek(fd_file, 0, SEEK_SET);

    while(amount_to_read > 0)
    {
        amount_read = read(fd_file, buf, 4096);
        if(amount_read == -1)
        {
            perror("cannot copy file");
            set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
            break;
        }
        else
        {
            amount_written = write(fd_copy, buf, amount_read);
            if(amount_written == -1)
            {
                perror("cannot write in copy file");
                set_pkt_header(res_pkt, ABORT, 0, NULL, NULL);
                unlink(copy_name); // We delete the uncomplete created copy
                break;
            }
            amount_to_read -= amount_written;
        }
    }

    // Closing openned files
    close(fd_copy);
    close(fd_file);

    // Sending response packet
    send_pkt(res_pkt, channel);
}

void server_remove(char *pkt, int channel) {
    char remoteFileName[256]; 
    memcpy(remoteFileName, pkt + 5, sizeof(remoteFileName));
    char response_pkt[HEADER_SIZE];

    if(!isValidFileName(remoteFileName))
    {
        fprintf(stderr, "Incorrect filename format !\n");
        set_pkt_header(response_pkt, FORMAT, 0, NULL, NULL);
        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
            return;
        }
        return;
    }
    if (checkFile(remoteFileName) != 0) {
        fprintf(stderr, "File does not exists!\n");
        set_pkt_header(response_pkt, MISS, 0, NULL, NULL);

        if (!send_pkt(response_pkt, channel)) {
            fprintf(stderr, "Failed to send response packet!\n");
            return;
        }
        return;
    }
    
    // Attempt to remove the file
    int removalStatus = remove(remoteFileName);

    // Create the response packet
    if (removalStatus == 0) {
        set_pkt_header(response_pkt, 0, 0, NULL, NULL);
    } else {
        set_pkt_header(response_pkt, ABORT, 0, NULL, NULL);
    }

    // Send the response packet
    if (!send_pkt(response_pkt, channel)) {
        fprintf(stderr, "Failed to send response packet!\n");
    }

    return;
}