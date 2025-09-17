
import pygame
import pygame.locals
from Obj_detect.Object_Detection_Module import *
from game_file.class_def import *
from game_file.graphic import *
from game_file.minmax import *
from communication.com import *
def message_handling(code,main_grid,player,grid_pos,sock):
    if code == 1 or code == 2 :
        if grid_pos == [] :
            return 6
        else :  
            error_code = main_grid.take(grid_pos,len(grid_pos),player,original=True)
            if code == 2 :
                vict = main_grid.victory()
                if vict :
                    matrice=main_grid.matrice()
                    position = str(grid_pos[1])+str(grid_pos[0])
                    message=construire_message(matrice,position,"WIN")
                    sock.sendall(message.encode())
            return error_code,0 
    if code == 3 :
        pygame.quit()
        return -1

def error_handling(nb_error,g_s) :
    if nb_error == 1 :
        text_showing("Unvalid move : last move not respected",g_s.src,g_s.background)
    if nb_error == 2 :
        text_showing("Unvalid move : case already taken",g_s.src,g_s.background)
    if nb_error == 3 :
        text_showing("Move not recognized : error of the code",g_s.src,g_s.background)
    if nb_error == 4 :
        text_showing("Unvalid move : no grid selectionned",g_s.src,g_s.background)
    if nb_error == 5 :
        text_showing("You can't click when using the camera",g_s.src,g_s.background)

def switch_player(player) :
    if player == 1 : return 0
    else : return 1

def tour(grid_pos,main_grid,player,online,g_s,sock=None) :
    if grid_pos == None or grid_pos == "QUIT" :
        return player
    else :
        if online :
            boucle = True
            while boucle :
                code,grid_pos =  reception_msg(sock,main_grid,grid_pos,player)
                error_code = message_handling(code,main_grid,player,grid_pos,sock)
                error_handling(error_code,g_s)
                if code != 0 : #Les 2 cas ou un "tour es fini" : soit quand on a recu un ack ou un new state
                    boucle = False
                if code == 3 : #cas ou on a recu un "end"
                    return -1
            return switch_player(player)
        else :
            error_code = main_grid.take(grid_pos,len(grid_pos),player,original=True)
            error_handling(error_code,g_s)
            if error_code == 0 : 
                return switch_player(player)
            else : 
                return player

def position(main_grid,player,last_click,online,g_s,mon_tour=None,sock=None) :
    if not mon_tour and online :
        return "PASS"
    if player == 0 : 
        ai_activated = g_s.AI_activated_player_0
        random_move = g_s.random_move_player_0
        player_cam = g_s.player0_cam
    else : 
        ai_activated = g_s.AI_activated_player_1
        random_move = g_s.random_move_player_1
        player_cam = g_s.player1_cam
    if random_move :
        grid_pos = main_grid.random_move()
        grid_pos = [i for i in grid_pos]
        print(grid_pos)
    elif ai_activated :
        a = startai(main_grid.matrice(),main_grid.last_move(),player)
        print(a)
        grid_pos = [a[1],a[0]]
    elif player_cam :
        grid_pos = coordinates()
        text = "is your play : " + str(grid_pos)
        text_showing(text,g_s.src,g_s.background)
        verif = position_verifyer()
        if not verif :
            return None
        grid_pos = grid_pos[::-1]
    else : 
        grid_pos = last_click
    if online and mon_tour and grid_pos != None :
        #On teste si le move indiqué est valide
        error_code = main_grid.take(grid_pos,len(grid_pos),player,original=True,test = True)
        error_handling(error_code,g_s)
        if error_code != 0 :
            return None
        send_message(grid_pos,main_grid,sock)
    return grid_pos
                

def event_treatment(main_grid,button_hitbox) :
    pos = []
    events = pygame.event.get()
    for event in events :
        if event.type == pygame.QUIT: 
            return "QUIT"  
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button_hitbox.collidepoint(pos):
                return "QUIT"
            else :
                pos = pygame.mouse.get_pos()
                pos = [i for i in main_grid.translate_coordinate(pos)]
                return pos

def mon_tour(player,orig_player):
    if player == orig_player :
        return True
    else :
        return False

def tic_tac_toe(g_s):
    size_square,top_corner_x,top_corner_y = postion_main_grid(g_s.src)
    main_grid = grid(2,(top_corner_x,top_corner_y),size_square,size_square,original=True)  
    done = False
    online = False
    sock = None
    player = 1
    winning_player = -2
    if g_s.client :
        if g_s.IP == None or g_s.port == None :
            text_showing("No port or IP were provided",g_s.src,g_s.background)
            done = True
        server_host=g_s.IP
        server_port=g_s.port
        con = (server_host,server_port)
        matrice= main_grid.matrice()
        pseudo = "TEAM9B"
        sock,pseudo_adversary=client_init(matrice,con,"TEAM9B")
        print(pseudo_adversary)
        online = True
        orig_player = 1
    if g_s.server :
        if g_s.IP == None or g_s.port == None :
            text_showing("No port or IP were provided",g_s.src,g_s.background)
            done = True
        server_host=g_s.IP
        server_port=g_s.port
        con = (server_host,server_port)
        matrice= main_grid.matrice()
        pseudo = "TEAM9B"
        sock,pseudo_adversary=server_init(matrice,con,"TEAM9B")
        print(pseudo_adversary)
        online = True
        orig_player = 0
    draw(main_grid,g_s.src,g_s.token1,g_s.token2,g_s.background)
    while not done: 
        # Add buttons
        back_hitbox = pygame.Rect(1150,58,187,46) 
        pygame.draw.rect(g_s.src, [0,0,0], back_hitbox)
        pos = pygame.mouse.get_pos() # Mouse position
        if back_hitbox.collidepoint(pos):
            back_img = pygame.image.load('themes/buttons/back_button2.png')
        else : 
            back_img = pygame.image.load('themes/buttons/back_button1.png')   
        draw(main_grid,g_s.src,g_s.token1,g_s.token2,g_s.background)
        #Blit the button onto the screen
        g_s.src.blit(back_img, (1150,58)) 
        pygame.display.flip()
        action = event_treatment(main_grid,back_hitbox)
        if action == "QUIT" :
            done = True
        if online :
            tour_joueur = mon_tour(player,orig_player)
            grid_pos = position(main_grid,player,action,online,g_s,mon_tour = tour_joueur,sock = sock)
        else :
            grid_pos = position(main_grid,player,action,online,g_s,)
            print(grid_pos)
        player = tour(grid_pos,main_grid,player,online,g_s,sock=sock)
        if player == -1 :
            done = True
            online = False
        vict = main_grid.victory()
        if vict : 
            if not online : 
                done = True
            if main_grid.is_case() :
                #we automatically switch player after a move, so we switch it again to obtain the true winner
                winning_player = switch_player(player)
                if online :
                    if orig_player == player :
                        message = "UTTT/1.0 WIN "+ pseudo+'\n'
                    else : 
                        message = "UTTT/1.0 WIN "+ pseudo_adversary+'\n'
                    sock.sendall(message.encode())
            else :
                if online :
                    message = "UTTT/1.0 WIN\n"
                    sock.sendall(message.encode())
                winning_player = -1
    if winning_player == -2 and online :
        message = "UTTT/1.0 406 FATAL_ERROR\n"
        sock.sendall(message.encode())
    return winning_player