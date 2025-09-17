import socket
import hashlib
hash = hashlib.sha3_224()





def server_init(matrice,con,pseudo):
    sock_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock_server.bind(con)
    sock_server.listen(1)
    conn, addr = sock_server.accept()
         # premier message 
    data = conn.recv(2048).decode()
    if not data:
        data = conn.recv(2048).decode()
    print(data)
    if data :
        message=construire_message(matrice,pseudo, statut ="CONNECTION") # pseudoname 
        conn.sendall(message.encode())
        pseudo =verifyer_msg(data)[2]  # autre pseudo
    return conn,pseudo


def client_init(matrice,con ,pseudo):
    socket_client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    message=construire_message(matrice,pseudo, statut ="CONNECTION") # pseudoname 
    socket_client.connect(con)
    socket_client.sendall(message.encode())
    # 2 part 
    data=socket_client.recv(2048).decode()
    while data is None:
        data=socket_client.recv(2048).decode()
    if  data:
        print(data)
        pseudo =verifyer_msg(data)[2]
    return socket_client,pseudo
        

def construire_message(matrice,position, statut="PLAY",error = -1):
    L=make_hash(matrice)
    if error !=-1 :
        message = f"UTTT/1.0 {error} {statut} {position} {L}\n"
    else :    
        message = f"UTTT/1.0 {statut} {position} {L}\n"
    return message


def verifyer_msg(message): # return list of all components 
    if message.startswith("UTTT/1.0"):
        L=message.split(" ")
        return L
    else:
        return False 

def make_hash(matrice):
    m=hashlib.sha3_224()
    L=["/","-","-"]
    chaine=""
    for i in range(len(matrice)) :
        chaine=chaine+L[i%3]
        for j in range(len(matrice)):
            chaine = chaine + str(matrice[i][j])
    chaine = chaine[1::]
    print(chaine)
    m.update(chaine.encode('utf-8'))
    return m.hexdigest()

def reception_msg(sock,main_grid,grid_pos,player):
    message=sock.recv(2048).decode()
    print('recu ',message)
    L=verifyer_msg(message)
    if L == "error_syntax":
        message=construire_message(matrice,405,"BAD_REQUEST")
        sock.sendall(message.encode())
        sock.close()
        return 0,grid_pos
    if L[1]=="PLAY":
        hash_produced = make_hash(main_grid.matrice())
        hash_produced_2 = make_hash(main_grid.matrice())+'\n'
        if L[3] == hash_produced or L[3] == hash_produced_2 : 
            print('We received PLAY')
            grid_pos = [int(L[2][0]),int(L[2][1])]
            print('grid position recu : ', grid_pos)
            matrice_copy = main_grid.matrice()
            matrice_copy[grid_pos[0]][grid_pos[1]] = player
            message=construire_message(matrice_copy,"" ,"NEW_STATE")
            print('message envoye:')
            print(message)
            sock.sendall(message.encode())   # premiere fois new state
            grid_pos = grid_pos[::-1]
            return 0,grid_pos       
        else :
            print('hash differs for play, supposedly impossible')
            message = construire_message(matrice,'',"STATE_PLAY")
            return 0,grid_pos
    if L[1]=="ACK\n":      # recevoir acknowledge
        return 2,grid_pos
    if L[1]=="NEW_STATE" :
        matrice_copy = main_grid.matrice()
        matrice_copy[grid_pos[1]][grid_pos[0]] = player
        hash_produced = make_hash(main_grid.matrice())
        hash_produced_2 = make_hash(main_grid.matrice())+'\n'
        print(L[2])
        print(hash_produced_2)
        if L[2] == hash_produced or L[2] == hash_produced_2 or L[3] == hash_produced or L[3] == hash_produced_2 : 
            message="UTTT/1.0 ACK\n"
            print("sent ack")
            sock.sendall(message.encode())
            print("Grid coordinates: ", grid_pos[::-1])
            return 1,grid_pos
        else :
            print("hash differs")
            matrice = main_grid.matrice()
            position = str(grid_pos[1])+str(grid_pos[0])
            message = construire_message(matrice,position,statut = "STATE_PLAY",error =404) 
            return 0,grid_pos
    if L[1]=="STATE_PLAY" : 
        matrice = main_grid.matrice()
        message=construire_message(matrice,"","NEW_STATE")
        sock.sendall(message.encode()) 
        return 0,grid_pos
    if L[1]=="406" :
        print("state play est envoye 3 fois ") 
        sock.close()
        return 3,[]
        

    if L[1]=="WIN":
        message="UTTT/1.0 END\n"
        sock.sendall(message.encode())   
        sock.close()
        return 3,[]

    if L[1]=="END\n":
        print('end')   
        sock.close()
        return 3,[]

def send_message(grid_pos,main_grid,sock) :
    matrice = main_grid.matrice()
    position = str(grid_pos[1])+str(grid_pos[0])
    message = construire_message(matrice,position, statut="PLAY")
    sock.sendall(message.encode())
    print('sent ',message)
