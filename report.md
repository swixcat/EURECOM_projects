# Introduction
The group project involves collaborative efforts on both the server and client sides to develop a comprehensive File Management System. The key functionalities include adding, removing, and duplicating remote files, retrieving files, listing available files, and printing specific lines from a file. The primary focus is on ensuring secure and efficient communication between the server and clients while meeting the specific requirements of each function.

## ------- Important remark -------
As our client was blocked on the four (and more) tests (of $ make test) involving -quotasize (problem lies in client_put), we removed the content of those tests for you to witness the rest of the tests (server side). Otherwise, you would'nt be able to see all the "our_server-teacher_client" [OK, OK] results. However, as we removed those tests, they do not mark [OK, OK] for the server anymore, even though they WERE working before.

## Group Members' Contributions

### SARR Serigne Khadim (server) - Project manager

#### General work

**General structure**

- Adapted core communication functions `recv_pkt()` and `send_pkt()`
- Set the overall project structure with appropriate header files and source files and modified the Makefile accordingly
- Created functions to facilitate packet handling (`setDataSize()`, `getDataSize()`, `set_pkt_header()`)

**Working on project specification**
- Worked on cat, get, cp (my role) and helped for ls (error fixing), all my functions are handmade (ChatGPT's not involved)
- Implemented options -directory, -quotasize, -quotanumber, and function `get_dir_stats()` for the options to work properly
- Run and debuged all server side commands with provided tests (\[0K,0K] perfect score on server side) !

### Server Functions Report

## 1. server_cat()

**Purpose:**
The server_cat function is responsible for handling the client's request to print the first n lines of a file. It receives a packet containing the filename and the number of lines to print. The server validates the filename, checks for file existence, opens the file, computes the required amount of bytes, and sends the file's content to the client in multiple packets.

**How it Works:**
- Packet Processing:
Extracts the filename and number of lines from the received packet.
- Filename Validation:
Calls `isValidFileName()` to check the validity of the filename.
- File Existence Check:
Calls `checkFile()` to verify if the file exists.
- Bytes Calculation:
Uses `bytes_for_n_lines()` (an auxiliary function I made) to compute the needed amount of bytes for the specified number of lines.
- Packet Sending Loop:
Sends full packets (4096 bytes) to the client until the entire content is sent.
- Last Packet Handling:
Sends a last packet if there is remaining data.
- Error Handling:
Handles errors during the process and sends appropriate response packets.

## 2. server_get()

**Purpose:**
The `server_get()` function manages the client's request to download a file from the server. It handles filename validation, checks for file existence, opens the file, computes the number of full packets needed, and sends the file's content to the client in multiple packets.

**How it works**
- Packet Processing:
Extracts the filename from the received packet.
- Filename Validation:
Calls `isValidFileName()` to check the validity of the filename.
- File Existence Check:
Calls `checkFile()` to verify if the file exists.
- File Opening:
Attempts to open the file for reading and tests for errors
- Computing Packets:
Calculates the number of full packets needed and remaining data size. I use modulo (%) appropriately for handling last packet.
- Packet Sending Loop:
Sends full packets to the client until the entire content is sent.
- Last Packet Handling:
Sends the last packet if there is remaining data.
- Error Handling:
Handles errors during the process and sends appropriate response packets.

## 3. server_cp()

**Purpose**
The server_cp function is designed to handle the client's request to copy a file. It checks the validity of filenames, verifies file existence, opens both the source and destination files, reads content from the source file, and writes it to the destination file. Quota handling is also implemented to ensure that the operation does not exceed a specified quota size.

**How it Works:**
- Filenames Extraction:
Extracts the source and destination filenames from the received packet.
- File Existence Check:
Checks if the source file exists and if the destination file does not exist to prevent overwriting.
- Filename Validation:
Validates the source and destination filenames using `isValidFileName()`.
- File Opening:
Attempts to open both the source and destination files.
- Quota Handling:
Checks if the operation exceeds the specified quota size.
- File Copy Loop:
Reads content from the source file (using a fixed size buffer) and writes it to the destination file until the entire file is copied.
- Error Handling:
Handles errors during the process and sends appropriate response packets.

...and all my commits tell what I've done so far more precisely.

## 4. server_list() and more

For ls, I chose to use the `lstat()` syscall to gather files' names and types, because the attribute `d_type` from the dirent structure was not part of the POSIX norm, thus to avoid undefined behaviors I decided to stick with lstat. It allowed me to coonsider only the regular files, and that method inspired me for the function `get_dir_stats()`, which gets the number of regular files of a directory along with the amount of bytes that they take.

### FATICH Ayman (server)

#### 1. server_remove Function
**Why:**
- Validation Checks: The function starts by validating the filename to prevent potential errors or security vulnerabilities caused by malformed filenames.
- File Existence Check: It checks whether the file exists before attempting to remove it to avoid errors or removing non-existent files.
- File Removal Attempt: The function attempts to remove the file using the `remove` function and prepares the appropriate response packet based on the success or failure of the removal.

**How it Works:**
- Packet Processing: Extracts the filename from the received packet using `memcpy`.
- Filename Validation: Calls the `isValidFileName` function to check if the filename adheres to the expected format.
- File Existence Check: Calls `checkFile` function to verify if the file exists.
- File Removal Attempt: Uses the `remove` function to attempt file removal.

#### 2. server_list Function
**Why:**
- Directory Listing: Lists files in the current directory, essential for providing information about available files to the client.
- Dynamic Memory Allocation: Dynamically allocates memory for the directory listing string, ensuring flexibility.
- Response Packet Handling: Sends the directory information in packets to the client, considering the maximum data size.

**How it Works:**
- Directory Listing: Iterates through directory entries, retrieves file names and sizes, and appends information to `lsstring`.
- Dynamic Memory Allocation: Dynamically allocates memory for `lsstring` to accommodate variable-sized directory listings.
- Packet Sending Loop: Sends packets with directory information to the client.

#### 3. server_put Function
**Why:**
- Packet Handling: Responsible for receiving and storing a file sent by the client, involving handling packets of data received.
- Validation Checks: Checks the validity of the filename and ensures the file doesn't already exist.

**How it Works:**
- Packet Processing: Extracts filename and file size from the received packet.
- Filename Validation: Calls `isValidFileName` to check the validity of the filename.
- File Existence Check: Calls `checkFile` to check if the file already exists.
- File Opening: Attempts to open the file for writing.
- Data Reception and Writing Loop: Iteratively receives and writes data packets to the file.
- Error Handling During Write: Handles errors during the writing process.
- File Closure and Success Response: Closes the file after successful reception and writing, sends a success response packet to the client.


### Chauvier Tom (client side)

#### 1. `client_put` Function
**Purpose:**
The `client_put` function is designed to send a file to the server in multiple packets. It calculates the number of packets needed to send the entire file, constructs each packet, and sends them to the server. After sending all the packets, it receives a response from the server, indicating the success or failure of the operation.

**Parameters:**
- `char* sendbuf`: Buffer to hold the data to be sent.
- `usercommand* cmd`: A structure containing user commands, specifically the filename in this case.
- `int channel`: An identifier for the communication channel with the server.

**Steps:**
- File Handling: Extract the filename from the user command and attempt to open the file.
- File Size Calculation: Use `lseek` to determine the size of the file.
- Packet Preparation and Transmission: Calculate the number of full packets and send them to the server.
- Receive Server Response: Receive a response packet from the server.
- Result Handling: Print success or error messages based on the server response.
- File Closure: Close the file descriptor.

**Test:**
- Example test for `put` with parameter `testput.txt` containing 5 kbytes.

#### 2. `client_get` Function
**Purpose:**
The purpose of this function is to download a file from the server and save it locally. The function initiates the process by sending a request to the server and then receiving the file data in multiple packets. The received data is written to a local file until the entire file is retrieved.

**Parameters:**
- `char* sendbuf`: Buffer to hold the data to be sent.
- `usercommand* cmd`: A structure containing user commands, specifically the source filename on the server (cmd->param1) and the local filename (cmd->param2).
- `int channel`: An identifier for the communication channel with the server.

**Steps:**
- File Name Handling: Extract the source filename and local filename from the user command.
- Packet Preparation and Transmission: Create a packet header, send the packet to the server.
- Receive Initial Server Response: Receive a response packet from the server, including the file size information.
- File Size Calculation: Calculate the number of full packets needed based on the file size.
- File Opening: Open the local file for writing.
- Receive and Store Data: Use a loop to receive and write full packets of data to the local file.
- Last Packet Handling: If there is remaining data, receive and write the last packet.
- File Closure: Close the local file.

**Test:**
- Example test for `get` with parameter `testget.txt` containing 5 kbytes.

#### 3. `client_cp` Function
**Purpose:**
This function requests the server to copy a file to a new file and receives the server's response to determine the success or failure of the operation.

**Parameters:**
- `char* sendbuf`: Buffer to hold the data to be sent.
- `usercommand* cmd`: A structure containing user commands, specifically the source filename (cmd->param1) and the destination filename (cmd->param2).
- `int channel`: An identifier for the communication channel with the server.

**Steps:**
- Filename Handling: Extract the source filename and the destination filename from the user command.
- Packet Preparation and Transmission: Create a packet header, send the packet to the server.
- Receive Server Response: Receive a response packet from the server.
- Result Handling: Print success or error messages based on the server response.

**Test:**
- Example test for `cp` with parameters `cptest1.txt` and `cptest2.txt`.

#### 4. `student_client` Function
**Options and Flags:**
- The function defines flags (analyze_flag, interactive_flag, directory_flag) to keep track of the presence of specific options in the command-line arguments.
- A buffer (directory) is used to store the directory path if specified.

**Command-Line Argument Parsing:**
- The function iterates through the command-line arguments and handles options such as -analyze, -interactive, and -directory.
- The -analyze option is used to read commands from a file specified by the subsequent argument.

**File Analysis:**
- If the -analyze flag is set, the function opens the specified file and reads commands from it line by line.
- Each command is parsed using `parse_commandline`.
- Based on the parsed command, the corresponding client function (e.g., `client_put`, `client_rm`) is invoked.

**Interactive Mode:**
- If the -interactive flag is set, the function enters an interactive mode where it prompts the user for commands.
- User input is read using `fgets` and processed similarly to the file analysis section.

**Client Function Invocation:**
- Depending on the parsed command, the corresponding client function is called (e.g., `client_put`, `client_rm`).

**Command Handling:**
- The function handles various commands such as help, restart, quit, or exit with specific actions.

### Efaz AHAMAN ULLAH (client side)

In this project, I worked on the client side, implementing the functions: `rm`, `ls`, `cat`, and `help`. In the `communication.c` file, I implemented a function named `error_hand` to handle errors, and in the `student_client` file, I coded some lines to manage error codes, potentially leading to "KO x" messages.

#### client_rm Function

**Purpose:**
This function facilitates communication between the client and the server to remove a remote file. To achieve this, the client sends a packet to the server with the command code and filename. Subsequently, it receives a packet from the server. The function checks the error code and returns the "err_code," initially set to zero.

**How it Works:**
- Packet Processing: Extracts the filename from the user command using `memcpy`.
- Filename Validation: Calls the `isValidFileName` function to check if the filename adheres to the expected format.
- File Existence Check: Calls `checkFile` function to verify if the file exists.
- File Removal Attempt: Uses the `remove` function to attempt file removal.

#### client_ls Function

**Purpose:**
This function enables communication between the client and the server to list the elements of the server's directory. I opted to create another function called `read_write` to enhance code conciseness and readability. The function sends a packet to the server with the command code, receives the server’s answer, checks the error code and datasize, and utilizes the `read_write` function to print the information. The for loop handles subsequent packets, and an integer variable named "comma" helps format the output. The function returns the error code, set to zero by default.

**How it Works:**
- Directory Listing: Iterates through directory entries, retrieves file names and sizes, and appends information to `lsstring`.
- Dynamic Memory Allocation: Dynamically allocates memory for `lsstring` to accommodate variable-sized directory listings.
- Packet Sending Loop: Sends packets with directory information to the client.

#### client_cat Function:

**Purpose:**
This function facilitates communication between the client and the server to return the first n lines (specified by the user). Similar to `ls`, I created the `read_write2` function for code conciseness and readability. The function sends a packet to the server with the filename, the number of lines to be printed, and the command code. It receives and prints the data from the first packet, uses a for loop for subsequent packets, and returns the error code, initially set to zero.

**How it Works:**
- Packet Processing: Extracts filename and the number of lines from the received packet.
- File Existence Check: Calls `checkFile` function to check if the file exists.
- Data Reception and Printing Loop: Receives and prints data from the first packet, uses a loop for subsequent packets.
- Error Handling: Handles errors during the process and returns the appropriate error code.

#### client_help Function

**Purpose:**
This function was implemented to assist users in distinguishing which commands to use in the command line. It uses the `printf` function to display help messages, utilizing bold letters and underlining certain terms for improved readability.

**error_hand Function**
The `error_hand` function, located in `communication.c`, was created to handle error codes in the program, providing appropriate responses. The use of a switch-case statement makes the code easy to read and debug.