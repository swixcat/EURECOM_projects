#ifndef SERVER_FUNCTIONS
#define SERVER_FUNCTIONS

#include <stdint.h>
#include <stdio.h>

/*Server functions prototypes and structs*/

// Test weather a file's name is correct of not.
// Returns 1 if correct, 0 if not.
int isValidFileName(const char *filename);

// Checks wether a file exists or not
int checkFile(const char* filename);

// Get the amount of bytes of a directpry and the number of regular files in it
int get_dir_stats(char* dirname, size_t* amount_bytes, int* nb_files);

// Returns the number of bytes needed to store nb lines in fd
size_t bytes_for_n_lines(int fd, int nb);

// Get function
void server_get(char* pkt, int channel);

// Cat funtion
void server_cat(char* pkt, int channel);

// Put function
void server_put(char *pkt, int channel);

// List function
void server_list(char *pkt, int channel);

// remove function
void server_remove(char *pkt, int channel);

// copy function
void server_cp(char* pkt, int channel, size_t quotasize, size_t total_bytes);

#endif