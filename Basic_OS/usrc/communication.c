#include "../uinclude/communication.h" 

// Returns the number formed by the "data size" field of a given packet
uint16_t getDataSize(const char* pkt)
{
    uint16_t num;
    memcpy(&num, pkt+3, 2); // Normally, sizeof(uint16_t) is 2
    return num;
}

// This funtion is more human friendly (I don't want you to struggle with your packets xD)
void setDataSize(char *pkt, uint16_t data_size)
{
    memcpy(pkt+3, &data_size, 2);
}

void set_pkt_header(char* pkt, char cmd_nb, uint16_t data_size, void* option1, void* option2)
{
    memset(pkt, 0, HEADER_SIZE); // We clear the pkt header with 0 ('\0' in char)
    pkt[0] = 'E';
    pkt[1] = 'D';
    pkt[2] = cmd_nb;
    setDataSize(pkt, data_size);
    // We copy only 31 bytes for the options as they must end with the string terminator '\0' (0 in decimal).
    // That's why we first set all the pkt header to 0 with memset !
    if (option1 != NULL)
        memcpy(pkt+5, option1, 31);
    if (option2 != NULL)
        memcpy(pkt+37, option2, 31);
}

/* A function to receive a packet (in pkt) on a socket channel 
 * it supposes that the received packet respects the format.
 * Returns 1 for success and 0 for failure
 */
int recv_pkt(char *pkt, int channel)
{
    int amount_to_receive;
    int amount_received;
    char *buf = pkt; // pointer to the place where received 
                     // data will be put, begins at pkt
    
    // First reads the whole header then gets data size if no errors
    amount_received = read(channel, buf, HEADER_SIZE);
    if (amount_received == -1) //error case
    {
        // print error-associated message on stderr cf errno.h
        perror("cannot write"); 
        return 0;
    }
    if (amount_received == 0) // connection closed
    {
        // print relevant error message on stderr
        fprintf(stderr, "connection closed\n"); 
        return 0;
    }
    else
    {
        // At this point, the whole header has been read
        amount_to_receive = getDataSize(pkt);
        buf += HEADER_SIZE; // We add HEADER_SIZE to the adress where buf points to
    }

    while(amount_to_receive > 0)
    {
        amount_received = read(channel, buf, amount_to_receive);
        if (amount_received == -1) { //error case
            // print error-associated message on stderr. cf errno.h
            perror("cannot read"); 
            return 0;
        }
        if (amount_received == 0) { // connection closed
            // print relevant error message on stderr
            fprintf(stderr, "connection closed\n"); 
            return 0;
        }
        else { // amount_received bytes have been read
            // update amount of data to receive
            amount_to_receive -= amount_received;
            // points to relevant data location
            buf += amount_received;
        }
    }
    return 1; // if this line is reached, no error occured.
}

/* a function to send a packet pkt on a socket channel 
 * the parameter packet must respect the format.
 * Returns 1 for success and 0 for failure
 */
int send_pkt(char *pkt, int channel)
{
    int amount_to_send = HEADER_SIZE + getDataSize(pkt);
    int amount_sent;
    char *buf = pkt; // pointer to the data to send, begins at pkt


    // send the packet which may require several writes
    while(amount_to_send > 0)
    {
        amount_sent = write(channel, buf, amount_to_send);
        if (amount_sent == -1)
        {
            // print specific message for closed connection (cf errno.h)
            if(errno == EPIPE)
                fprintf(stderr, "connection closed\n"); 
            else
            // print error-associated message on stderr cf (errno.h)
                perror("cannot write"); 
            return 0;
        }
        if (amount_sent == 0) // checked to avoid infinite loop
        {
            // print relevant error message on stderr
            fprintf(stderr, "Write problem. Infinite loop avoided !\n"); 
            return 0;
        }
        else // amount_sent bytes have been sent
        {
            // update amount of data to send
            amount_to_send -= amount_sent;
            // points to remaining data
            buf += amount_sent;
        }
    }
    return 1; // if this line is reached, no error occured.
}

int error_hand(char *recebuf)  //Handles error codes : can be used both in server and in client side
{
    int err_code;
    err_code = *(recebuf+2);
    switch(err_code)
    {
        case -1 :
            fprintf(stderr, "FORMAT : Bad packet format\n");
            break;
        
        case -2 :
            fprintf(stderr,"MISS : File not found\n");
            break;
        
        case -3 :
            fprintf(stderr,"EXISTS : File already exists\n");
            break;
        
        case -4 : 
            fprintf(stderr,"ABORT : Command fails\n");
            break;
        
        case -5 :
            fprintf(stderr,"QUOTA : Quota exceeded\n");
            break;
        
        case -6 :
            fprintf(stderr,"SYNTAX : Syntax error in command line\n");
            break;

        case -7 :
            fprintf(stderr,"RESP : Bad response from server\n");
            break;
        
        case -8 :
            fprintf(stderr,"CLOSED : Connection closed\n");
            break;

    }
    return err_code;
}