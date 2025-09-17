#ifndef CLIENT_FUNCTIONS
#define CLIENT_FUNCTIONS

#include <stdio.h>
#include <stdlib.h>

// Libraries to use open(), read().. and other file IO syscalls (plus some defined constants)
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

// For the usercommand struct definition
#include "../include/utilities.h"

int isValidFileName(const char *filename);

// "put" function prototype for client side
int client_put(char* sendbuf, usercommand* cmd,int channel);

// "get" function prototype for client side
int client_get(char* sendbuf, usercommand* cmd,int channel);

// "rm" function prototype for client side
int client_rm(char *sendbuf, usercommand *cmd, int channel);

// "ls" function prototype for client side
int client_ls(char *sendbuf, int channel);

// "rm" function prototype for client side
int client_cat(char *sendbuf, usercommand *cmd, int channel);

// "cp" function prototype for client side
int client_cp(char *sendbuf, usercommand *cmd, int channel);

// "help" function prototype for client side
int client_help();
#endif