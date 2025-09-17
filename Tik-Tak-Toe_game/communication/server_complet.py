import pygame
from Object_Detection_Module import *
from game_file.class_def import *
from game_file.graphic import *
from communication import *
import socket
import hashlib

m=hashlib.sha3_224()
token1 = "themes/tokens/classic1.png"
token2 = "themes/tokens/classic2.png"
game_background = "themes/background/classic-back.png"
timeout_duration = 10

#sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

amtrow =9
amtcol =9




def verifyer_msg(message): # return list of all components 
    if message.startswith("UTTT/1.0"):
        L=message.split(" ")
        return L
    else:
        return "error_syntax"



def error_handling(nb_error,src,game_backgrownd) :
    if nb_error == 1 :
        text_showing("Unvalid move : last move not respected",src,game_backgrownd)
    if nb_error == 2 :
        text_showing("Unvalid move : case already taken",src,game_backgrownd)
    if nb_error == 3 :
        text_showing("Move not recognized : error of the code",src,game_backgrownd)
    if nb_error == 4 :
        text_showing("Unvalid move : no grid selectionned",src,game_backgrownd)

def switch_player(player) :
    if player == 0 : return 1
    else : return 0


if __name__ == '__main__' :
    pygame.init()
    clock = pygame.time.Clock()
    src = pygame.display.set_mode()
    pygame.display.set_caption("Ultimate tic tac toe")
    size_square,top_corner_x,top_corner_y = postion_main_grid(src)
    main_grid = grid(2,(top_corner_x,top_corner_y),size_square,size_square,original=True)   
    done = False
    player = 1
    src.fill(pygame.Color("white"))
    draw(main_grid,src,token1,token2,game_background)
    mon_tour = 0

    matrice= main_grid.matrice()
    conn,pseudo=server(matrice ,"TEAM9B")
    print(pseudo)

    while not done:
        if mon_tour :
            print('le tour de cet ordi')
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print('click enregistre')
                    pos = pygame.mouse.get_pos()
                    grid_pos = [i for i in main_grid.translate_coordinate(pos)]
                    
                    matrice = main_grid.matrice()
                    position = str(grid_pos[1])+str(grid_pos[0]) 
                    message = construire_message(matrice,position, statut="PLAY")
                    conn.sendall(message.encode())
                    print('sent',message)
                    mon_tour = 0
        else :
            #attend recevoir information (Sad)
            print('le tour de sad')
    
            message=conn.recv(2048).decode()
            print('recu ',message)
            L=verifyer_msg(message)
            if L == "error_syntax":
                message=construire_message(matrice,405,"BAD_REQUEST")
                conn.close()
            if L[1]=="PLAY":
                hash_produced = make_hash(main_grid.matrice())+'\n'

                if L[3] == hash_produced : 
                    print('We received PLAY')
                    grid_pos = [int(L[2][0]),int(L[2][1])]
                    print('grid position recu : ', grid_pos)
                    grid_pos = grid_pos[::-1]  
                    error_code = main_grid.take(grid_pos,len(grid_pos),player,original=True)
                    matrice = main_grid.matrice()
                    message=construire_message(matrice,"" ,"NEW_STATE")
                    print('message envoye:')
                    print(message)
                    conn.sendall(message.encode())   # premiere fois new state       
                else :
                    print('hash differs')
            if L[1]=="ACK\n":      # recevoir acknowledge
                victoire = main_grid.is_case()
                if victoire :
                    message=construire_message(matrice,position,"WIN")
                    conn.sendall(message.encode())
                else :
                    player = switch_player(player)
                    mon_tour = 1
            if L[1]=="NEW_STATE" :
                matrice_copy = main_grid.matrice()
                matrice_copy[grid_pos[1]][grid_pos[0]] = player
                hash_produced = make_hash(main_grid.matrice())+'\n'
                if L[3] == hash_produced : 
                    message="UTTT/1.0 ACK\n"
                    conn.sendall(message.encode())
                    print("Grid coordinates: ", grid_pos[::-1])
                    main_grid.take(grid_pos,len(grid_pos),player,original=True)
                    player = switch_player(player)
                else :
                    print(hash_produced)
                    print("hash differs")
                    matrice = main_grid.matrice()
                    message = construire_message(matrice,position,statut = "STATE_PLAY",error =404) 
                    
            if L[1]=="STATE_PLAY" : 
                matrice = main_grid.matrice()
                message=construire_message(matrice,"","NEW_STATE")
                conn.sendall(message.encode()) 
            
            if L[1]=="406" :
                print("state play est envoye 3 fois ") 
                pygame.quit()
                conn.close()

            if L[1]=="WIN":
                text = pseudo + " a gagner avec le move " + L[2]
                text_showing(text,src,game_background)
                print(text)
                message="UTTT/1.0 END\n"
                conn.sendall(message.encode())
                pygame.quit()   
                conn.close()
                break

            if L[1]=="END\n":
                print('end')
                pygame.quit()   
                conn.close()
                break
            


        src.fill(pygame.Color("white"))
        clock.tick(50)
        draw(main_grid,src,token1,token2,game_background)
        pygame.display.flip()
    pygame.quit()