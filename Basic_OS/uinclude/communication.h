/* to awoid including this header twice */
#ifndef COMMUNICATION_H
#define COMMUNICATION_H

/* to print messages associated to detected errors */
#include <errno.h>
/* for fprintf, stderr,...*/
#include <stdio.h>
/* for read/write,...*/
#include <unistd.h>
/* for memcpy,...*/
#include <string.h>

/* for atoi,...*/
#include <stdlib.h>
/* for uint16, ...*/
#include <stdint.h>
/* for size_t type and others I/O tools*/
#include <stdio.h> 
/* for open, ...*/
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define HEADER_SIZE 69 // Size of the header (always sent)
#define MAX_PACKET_SIZE 4096 // Maximum size of a packet
#define MAX_DATA_SIZE 4027

// Enumeration of commands (in order to write them instead of numbers)
enum commands {PUT = 1, REMOVE, GET, LIST, PRINT, COPY};

enum errors
{
    FORMAT = -1,
    MISS = -2,
    EXISTS = -3,
    ABORT = -4,
    QUOTA = -5,
    SYNTAX = -6,
    RESP = -7,
    CLOSED = -8
};

/* a function to send a packet pkt on a socket channel 
 * the parameter packet must respect the format.
 * Returns 1 for success and 0 for failure
 */
int send_pkt(char *pkt, int channel);

/* a function to receive a packet (in pkt) on a socket channel 
 * it supposes that the received packet respects the format.
 * Returns 1 for success and 0 for failure
 */
int recv_pkt(char *pkt, int channel);

// Returns the number formed by the "data size" field of a given packet
uint16_t getDataSize (const char* pkt);

// Stores data_size in the data size field of a given packet (2 bytes)
void setDataSize(char *pkt, uint16_t data_size);

// Fills the pkt with given parameters.
// This function assumes ("précondition") that the packet is well allocated !
// Parameters option1 and option2 are void* because sometimes one can be an int or something else than a string.
// Moreover, memcpy() doesn't care about the type of its arguments, it modifies their BYTES, so void* is perfect here !
void set_pkt_header(char* pkt, char cmd_nb, uint16_t data_size, void* option1, void* option2);

// Handles error
int error_hand(char *recebuf);

#endif