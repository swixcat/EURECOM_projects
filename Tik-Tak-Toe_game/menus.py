import pygame
from game import *


# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 1440,810
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("X&O's: Tik-Tak-Toe Revamped")
gameIcon = pygame.image.load('themes/logo.png')
pygame.display.set_icon(gameIcon)

# variables to determine which menu is currently displayed
running = True
main = True
theme = False
token = False
play = False
ready = False
game = False
tuto = 0
over = -2

parameters = [running, main, theme, token, play, ready, game, tuto, over]


#variables for launching the game (default setting : classic, player mode)
game_background = "themes/background/classic-back.png"
game_mode = "local"
player1_token = "themes/tokens/classic1.png"
player2_token = "themes/tokens/classic2.png"
current_player = 1
player1_mode = "mouse"
player2_mode = "mouse"
online_mode = None
IPv4 = 0
port = 0
settings = [game_background, game_mode, player1_token, player2_token, current_player, player1_mode, player2_mode,online_mode,IPv4,port]
    
    
# Set up colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
TRANSPARENT = (0, 0, 0, 0)  # Transparent color with alpha channel 0
TEAL = (9, 227, 232, 192)  # Semi-transparent teal color 
PINK = (255, 7, 255, 192)  # Semi-transparent pink color

# grid color and higlight color for each theme
theme_color ={"classic":[WHITE, TEAL],"bnw":[WHITE, GREY],"pixel":[WHITE, (255,0,0)],"autumn":[BLACK,(231, 102, 15)],"winter":[BLACK, (136, 201, 249)],
              "spring":[BLACK,(250, 181, 192)],"summer":[BLACK,(255, 197, 51)],"christmas":[BLACK, (255,0,0)],"chinese":[WHITE,(212, 6, 1)],"valentines":[BLACK,(248, 82, 69)],
              "st-patrick":[BLACK,(22, 155, 98)],"easter":[BLACK,(181, 170, 229)],"national":[WHITE,(42, 185, 228)],"halloween":[WHITE,(251, 133, 0)],"thanksgiving":[BLACK,(239, 156, 56)],
              "skull":[WHITE,(249, 173, 11)],"cat":[BLACK, (246, 140, 146)],"dog":[BLACK, (99, 154, 154)],"dino":[BLACK,(190, 235, 159)],"fruits":[BLACK, (255, 189, 185)]} 

# Create a surface for the transparent layer
transparent_layer = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
transparent_layer.fill(TRANSPARENT)

# Create a surface for the transparent layer for player 1
transparent_layer1 = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
transparent_layer1.fill(TRANSPARENT)

# Create a surface for the transparent layer for player 2
transparent_layer2 = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
transparent_layer2.fill(TRANSPARENT)

# Create input boxe for IP and port : 
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, 1, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = BLACK if self.active else WHITE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, 1,WHITE)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

IP_input_box = InputBox(940, 425,212,56,text = 'IP')
port_input_box = InputBox(940, 510,212,56,text = 'Port')
input_boxes = [IP_input_box,port_input_box]

#######        MAIN MENU            ########   
def main_menu(parameters, settings):
    background_image = pygame.image.load("themes/background/menu-back.png")
    
    # add a buttons
    play_hitbox = pygame.Rect(490,350,434,66) 
    pygame.draw.rect(screen, BLACK, play_hitbox)  
    
    online_hitbox = pygame.Rect(490,450,434,66) 
    pygame.draw.rect(screen, BLACK, online_hitbox)  
    
    quit_hitbox = pygame.Rect(490,550,434,66) 
    pygame.draw.rect(screen, BLACK, quit_hitbox) 
    
    theme_hitbox = pygame.Rect(490,650,434,66) 
    pygame.draw.rect(screen, BLACK, theme_hitbox)  
    
    
    pos = pygame.mouse.get_pos() #position de la souris

    if play_hitbox.collidepoint(pos):
        play_img = pygame.image.load('themes/buttons/play_button2.png')
    else : 
        play_img = pygame.image.load('themes/buttons/play_button1.png') 
        
    if theme_hitbox.collidepoint(pos):
        theme_img = pygame.image.load('themes/buttons/theme_button2.png')
    else : 
        theme_img = pygame.image.load('themes/buttons/theme_button1.png') 
    
    if quit_hitbox.collidepoint(pos):
        quit_img = pygame.image.load('themes/buttons/quit1_button2.png')
    else : 
        quit_img = pygame.image.load('themes/buttons/quit1_button1.png')
        
    if online_hitbox.collidepoint(pos):
        online_img = pygame.image.load('themes/buttons/online_button1.png')
    else : 
        online_img = pygame.image.load('themes/buttons/online_button2.png')  
  
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(play_img, (490,350))
    screen.blit(online_img, (490,450))
    screen.blit(quit_img, (490,550))
    screen.blit(theme_img, (490,650))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if play_hitbox.collidepoint(mouse_x, mouse_y):
                #add choice in settings
                settings[1] = "local"
                parameters[4] = "local"
                parameters[1] = False
            
            if online_hitbox.collidepoint(mouse_x, mouse_y):
                #add choice in settings
                settings[1] = "online"
                parameters[4] = "online"
                parameters[1] = False
                
            if theme_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[2] = True
                parameters[1] = False
                
            if quit_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[0] = False
                
            #if tuto_hitbox.collidepoint(mouse_x, mouse_y):
               # parameters[6] = 1
                #parameters[1] = False
        
    return parameters, settings

#######        TUTO MENU - PAGE 1            ########   
def tuto_menu1(parameters, settings):
    background_image = pygame.image.load("themes/background/tuto1-back.png")
    
    # add buttons
    con_hitbox = pygame.Rect(513,130,187,46) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  
    
    back_hitbox = pygame.Rect(740,130,187,46) 
    pygame.draw.rect(screen, BLACK, back_hitbox)  
    
           
    #Make buttons appear
    pos = pygame.mouse.get_pos() # Mouse position

    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/con_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/con_button1.png') 
        
    if back_hitbox.collidepoint(pos):
        back_img = pygame.image.load('themes/buttons/back_button2.png')
    else : 
        back_img = pygame.image.load('themes/buttons/back_button1.png') 
     
    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))
    
    # Blit the transparent layer onto the screen
    screen.blit(transparent_layer, (0, 0))    
    
    # Blit the buttons onto the screen
    screen.blit(con_img, (513, 130))
    screen.blit(back_img, (740, 130))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if con_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 2
                parameters[1] = False
                
            if back_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 0
                parameters[1] = True
                
    return parameters, settings

#######        TUTO MENU - PAGE 2            ########   
def tuto_menu2(parameters, settings):
    background_image = pygame.image.load("themes/background/tuto2-back.png")
    
    # add buttons
    con_hitbox = pygame.Rect(513,130,187,46) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  
    
    back_hitbox = pygame.Rect(740,130,187,46) 
    pygame.draw.rect(screen, BLACK, back_hitbox)  
    
           
    #Make buttons appear
    pos = pygame.mouse.get_pos() # Mouse position

    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/con_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/con_button1.png') 
        
    if back_hitbox.collidepoint(pos):
        back_img = pygame.image.load('themes/buttons/back_button2.png')
    else : 
        back_img = pygame.image.load('themes/buttons/back_button1.png') 
     
    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))
    
    # Blit the transparent layer onto the screen
    screen.blit(transparent_layer, (0, 0))    
    
    # Blit the buttons onto the screen
    screen.blit(con_img, (513, 130))
    screen.blit(back_img, (740, 130))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if con_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 3
                parameters[1] = False
                
            if back_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 1
                parameters[1] = False
        
    return parameters, settings          

#######        TUTO MENU - PAGE 3            ########   
def tuto_menu3(parameters, settings):
    background_image = pygame.image.load("themes/background/tuto3-back.png")
    
    # add buttons
    con_hitbox = pygame.Rect(513,130,187,46) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  
    
    back_hitbox = pygame.Rect(740,130,187,46) 
    pygame.draw.rect(screen, BLACK, back_hitbox)  
    
           
    #Make buttons appear
    pos = pygame.mouse.get_pos() # Mouse position

    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/con_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/con_button1.png') 
        
    if back_hitbox.collidepoint(pos):
        back_img = pygame.image.load('themes/buttons/back_button2.png')
    else : 
        back_img = pygame.image.load('themes/buttons/back_button1.png') 
     
    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))
    
    # Blit the transparent layer onto the screen
    screen.blit(transparent_layer, (0, 0))    
    
    # Blit the buttons onto the screen
    screen.blit(con_img, (513, 130))
    screen.blit(back_img, (740, 130))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if con_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 0
                parameters[1] = True
                
            if back_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 2
                parameters[1] = False
        
    return parameters, settings

#######        PLAY ONLINE MENU            ########   

def play_menu_online(parameters, settings,input_boxes):
    background_image = pygame.image.load("themes/background/play-menu-back.png")
    
    # add a buttons
    camera_hitbox = pygame.Rect(274,336,212,56) 
    pygame.draw.rect(screen, BLACK, camera_hitbox)  
    
    mouse_hitbox = pygame.Rect(274, 425,212,56) 
    pygame.draw.rect(screen, BLACK, mouse_hitbox)  
    
    ai_hitbox = pygame.Rect(274,510,212,56) 
    pygame.draw.rect(screen, BLACK, ai_hitbox)  
    
    client_hitbox = pygame.Rect(940,247,212,56) 
    pygame.draw.rect(screen, BLACK, client_hitbox)
    
    server_hitbox = pygame.Rect(940, 336,212,56) 
    pygame.draw.rect(screen, BLACK, server_hitbox)  
    
    return_hitbox = pygame.Rect(744, 616, 212,56) 
    pygame.draw.rect(screen, BLACK, return_hitbox)  
   
    con_hitbox = pygame.Rect(484, 616, 212, 56) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  

    pos = pygame.mouse.get_pos() #position de la souris
    if camera_hitbox.collidepoint(pos):
        camera_img = pygame.image.load('themes/buttons/camera_button2.png')
    else : 
        camera_img = pygame.image.load('themes/buttons/camera_button1.png') 
        
    if mouse_hitbox.collidepoint(pos):
        mouse_img = pygame.image.load('themes/buttons/mouse_button2.png')
    else : 
        mouse_img = pygame.image.load('themes/buttons/mouse_button1.png') 
        
    if ai_hitbox.collidepoint(pos):
        ai_img = pygame.image.load('themes/buttons/aiplay_button2.png')
    else : 
        ai_img = pygame.image.load('themes/buttons/aiplay_button1.png') 
    
    if client_hitbox.collidepoint(pos):
        client_img = pygame.image.load('themes/buttons/client_button2.png')
    else : 
        client_img = pygame.image.load('themes/buttons/client_button1.png') 

    if server_hitbox.collidepoint(pos):
        server_img = pygame.image.load('themes/buttons/server_button2.png')
    else : 
        server_img = pygame.image.load('themes/buttons/server_button1.png')
    
    if return_hitbox.collidepoint(pos):
        return_img = pygame.image.load('themes/buttons/backplay_button2.png')
    else : 
        return_img = pygame.image.load('themes/buttons/backplay_button1.png') 
        
    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/continue_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/continue_button1.png') 
    
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(camera_img, (274,336))
    screen.blit(mouse_img, (274,425))
    screen.blit(ai_img, (274,510))
    screen.blit(client_img, (940,250))
    screen.blit(server_img, (940,336))
    screen.blit(con_img, (484,616))
    screen.blit(return_img, (744,616))
    [input_box.draw(screen) for input_box in input_boxes]
    for event in pygame.event.get():
        for box in input_boxes:
            box.handle_event(event)
            box.update()
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if camera_hitbox.collidepoint(mouse_x, mouse_y):
                settings[5]="camera"
                settings[6]="camera"
                
            if mouse_hitbox.collidepoint(mouse_x, mouse_y):
                settings[5]="mouse"
                settings[6]="mouse"
                
            if ai_hitbox.collidepoint(mouse_x, mouse_y):
                settings[5]="ai"
                settings[6]="ai"
                
            if client_hitbox.collidepoint(mouse_x, mouse_y):
                settings[7]="client"
                print(settings[7])

            if server_hitbox.collidepoint(mouse_x, mouse_y):
                settings[7]="server"
                print(settings[7])

            if con_hitbox.collidepoint(mouse_x, mouse_y):
                settings[8] = input_boxes[0].text
                settings[9] = input_boxes[1].text
                IP_input_box = InputBox(940, 425,212,56,text = 'IP')
                port_input_box = InputBox(940, 510,212,56,text = 'Port')
                input_boxes = [IP_input_box,port_input_box]
                parameters[5] = True
                parameters[4] = False
                
            if return_hitbox.collidepoint(mouse_x, mouse_y):
                IP_input_box = InputBox(940, 425,212,56,text = 'IP')
                port_input_box = InputBox(940, 510,212,56,text = 'Port')
                input_boxes = [IP_input_box,port_input_box]
                parameters[1] = True
                parameters[4] = False
        
    return parameters, settings       

#######        PLAY LOCAL MENU            ########   
def play_menu_local(parameters, settings):
    background_image = pygame.image.load("themes/background/play-menu-back.png")
    
    # add a buttons
    camera_hitbox1 = pygame.Rect(274,336,212,56) 
    pygame.draw.rect(screen, BLACK, camera_hitbox1)  
    
    mouse_hitbox1 = pygame.Rect(274, 425,212,56) 
    pygame.draw.rect(screen, BLACK, mouse_hitbox1)  
    
    ai_hitbox1 = pygame.Rect(274,510,212,56) 
    pygame.draw.rect(screen, BLACK, ai_hitbox1)  
    
    camera_hitbox2 = pygame.Rect(940,336,212,56) 
    pygame.draw.rect(screen, BLACK, camera_hitbox2)  
    
    mouse_hitbox2 = pygame.Rect(940, 425,212,56) 
    pygame.draw.rect(screen, BLACK, mouse_hitbox2)  
    
    ai_hitbox2 = pygame.Rect(940,510,212,56) 
    pygame.draw.rect(screen, BLACK, ai_hitbox2)  
    
    return_hitbox = pygame.Rect(744, 616, 212,56) 
    pygame.draw.rect(screen, BLACK, return_hitbox)  
   
    con_hitbox = pygame.Rect(484, 616, 212, 56) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  

    pos = pygame.mouse.get_pos() #position de la souris
    if camera_hitbox1.collidepoint(pos):
        camera_img1 = pygame.image.load('themes/buttons/camera_button2.png')
    else : 
        camera_img1 = pygame.image.load('themes/buttons/camera_button1.png') 
        
    if mouse_hitbox1.collidepoint(pos):
        mouse_img1 = pygame.image.load('themes/buttons/mouse_button2.png')
    else : 
        mouse_img1 = pygame.image.load('themes/buttons/mouse_button1.png') 
        
    if ai_hitbox1.collidepoint(pos):
        ai_img1 = pygame.image.load('themes/buttons/aiplay_button2.png')
    else : 
        ai_img1 = pygame.image.load('themes/buttons/aiplay_button1.png') 
    
    if camera_hitbox2.collidepoint(pos):
        camera_img2 = pygame.image.load('themes/buttons/camera_button2.png')
    else : 
        camera_img2 = pygame.image.load('themes/buttons/camera_button1.png') 
        
    if mouse_hitbox2.collidepoint(pos):
        mouse_img2 = pygame.image.load('themes/buttons/mouse_button2.png')
    else : 
        mouse_img2 = pygame.image.load('themes/buttons/mouse_button1.png') 
        
    if ai_hitbox2.collidepoint(pos):
        ai_img2 = pygame.image.load('themes/buttons/aiplay_button2.png')
    else : 
        ai_img2 = pygame.image.load('themes/buttons/aiplay_button1.png') 
    
    if return_hitbox.collidepoint(pos):
        return_img = pygame.image.load('themes/buttons/backplay_button2.png')
    else : 
        return_img = pygame.image.load('themes/buttons/backplay_button1.png') 
        
    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/continue_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/continue_button1.png') 
    
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(camera_img1, (274,336))
    screen.blit(mouse_img1, (274,425))
    screen.blit(ai_img1, (274,510))
    screen.blit(camera_img2, (940,336))
    screen.blit(mouse_img2, (940,425))
    screen.blit(ai_img2, (940,510))
    screen.blit(con_img, (484,616))
    screen.blit(return_img, (744,616))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if camera_hitbox1.collidepoint(mouse_x, mouse_y):
                settings[5]="camera"
                
            if mouse_hitbox1.collidepoint(mouse_x, mouse_y):
                settings[5]="mouse"
                
            if ai_hitbox1.collidepoint(mouse_x, mouse_y):
                settings[5]="ai"
                
            if camera_hitbox2.collidepoint(mouse_x, mouse_y):
                settings[6]="camera"
                
            if mouse_hitbox2.collidepoint(mouse_x, mouse_y):
                settings[6]="mouse"
                
            if ai_hitbox2.collidepoint(mouse_x, mouse_y):
                settings[6]="ai"
                
            if con_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[5] = True
                parameters[4] = False
                
            if return_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[1] = True
                parameters[4] = False
        
    return parameters, settings       


#######        READY MENU            ########   
def ready_menu(parameters, settings):
    background_image = pygame.image.load("themes/background/ready-menu-back.png")
    
    # add a buttons
    go_hitbox = pygame.Rect(490,372,434,66) 
    pygame.draw.rect(screen, BLACK, go_hitbox)  
    
    tuto_hitbox = pygame.Rect(490,481,434,66) 
    pygame.draw.rect(screen, BLACK, tuto_hitbox)  
    
    return_hitbox = pygame.Rect(490,590,434,66) 
    pygame.draw.rect(screen, BLACK, return_hitbox) 
    
    
    pos = pygame.mouse.get_pos() #position de la souris

    if go_hitbox.collidepoint(pos):
        go_img = pygame.image.load('themes/buttons/go_button2.png')
    else : 
        go_img = pygame.image.load('themes/buttons/go_button1.png') 
        
    if tuto_hitbox.collidepoint(pos):
        tuto_img = pygame.image.load('themes/buttons/tuto_button2.png')
    else : 
        tuto_img = pygame.image.load('themes/buttons/tuto_button1.png') 
    
    if return_hitbox.collidepoint(pos):
        return_img = pygame.image.load('themes/buttons/return_button2.png')
    else : 
        return_img = pygame.image.load('themes/buttons/return_button1.png')
        
  
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(go_img, (490,372))
    screen.blit(return_img, (490,590))
    screen.blit(tuto_img, (490,481))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if go_hitbox.collidepoint(mouse_x, mouse_y):
                #add choice in settings
                parameters[6] = True
                parameters[5] = False
            
            if tuto_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[7] = 1
                parameters[5] = False
                
            if return_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[4] = True
                parameters[5] = False
                
            #if tuto_hitbox.collidepoint(mouse_x, mouse_y):
               # parameters[6] = 1
                #parameters[1] = False
        
    return parameters, settings

#######        THEME MENU            ########    
def theme_menu(parameters, settings):
    background_image = pygame.image.load("themes/background/theme-menu-back.png")
    
    # Create surfaces for hitboxes with per-pixel alpha
    hitbox_surfaces = []
    hitbox_positions= [(90+(160+20)*i, 226 + (160+18)*j)  for j in range(3) for i in range(7)]
    hitbox_positions2 = [(58, 233),(253, 233),(447, 233),(642,233),(836, 233),(1030, 233),(1225,233), 
                        (58,417),(253, 417),(447, 417),(642,417),(836, 417),(1030, 417),(1224,417),
                        (58, 601),(253, 601),(447, 601),(642,601),(836, 601),(1030, 601),(1224,601)]
    selected_hitbox = None

    theme_dict ={1:"classic",2:"bnw",3:"pixel",4:"autumn",5:"winter",6:"spring",7:"summer",8:"christmas",9:"chinese",
                 10:"valentines",11:"st-patrick",12:"easter",13:"national",14:"halloween",15:"thanksgiving",16:"skull",
                 17:"cat",18:"dog",19:"dino",20:"fruits",21:"plus"}

    for pos in hitbox_positions:
        hitbox_surface = pygame.Surface((160, 160), pygame.SRCALPHA)
        pygame.draw.rect(hitbox_surface, TRANSPARENT, (0, 0, 160, 160))  # Draw hitbox rectangles
        hitbox_surfaces.append((hitbox_surface, pos))
        
    # add buttons
    con_hitbox = pygame.Rect(513,165,187,46) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  
    
    back_hitbox = pygame.Rect(740,165,187,46) 
    pygame.draw.rect(screen, BLACK, back_hitbox)  
    
           
    #Make buttons appear
    pos = pygame.mouse.get_pos() # Mouse position

    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/con_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/con_button1.png') 
        
    if back_hitbox.collidepoint(pos):
        back_img = pygame.image.load('themes/buttons/back_button2.png')
    else : 
        back_img = pygame.image.load('themes/buttons/back_button1.png') 
     
    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))
    
    # Blit the transparent layer onto the screen
    screen.blit(transparent_layer, (0, 0))    
    
    # Blit the buttons onto the screen
    screen.blit(con_img, (513, 165))
    screen.blit(back_img, (740, 165))
    
    # Blit the hitboxes onto the screen
    for hitbox_surface, hitbox_pos in hitbox_surfaces:
        screen.blit(hitbox_surface, hitbox_pos)
    
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            #Selection of an hitbox
            for hitbox_surface, hitbox_pos in hitbox_surfaces:
                hitbox_rect = pygame.Rect(hitbox_pos[0], hitbox_pos[1], 160, 160)
                if hitbox_rect.collidepoint(mouse_x, mouse_y):
                    selected_hitbox = hitbox_pos
                    transparent_layer.fill(TRANSPARENT)  # Deselect all hitboxes first
                    pygame.draw.rect(transparent_layer, TEAL, hitbox_rect, 3)  # Draw a frame around the selected hitbox
                    
                    #find the selected theme's name
                    index = hitbox_positions.index(selected_hitbox) + 1 
                    game_background = "themes/background/" +  theme_dict[index] + "-back.png"
                    settings[0] = game_background
                         
            if con_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[3] = True
                parameters[2] = False
                
            if back_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[1] = True
                parameters[2] = False
    return parameters, settings

#######        TOKEN MENU            ########    
def token_menu(parameters, settings):
    transparent_layer.fill(TRANSPARENT)  # Deselect all hitboxes first
    background_image = pygame.image.load("themes/background/token-menu-back.png")
    
    token_positions = [(84 + i * (77+23), 220 + (77+13) * j)   for j in range(6) for i in range(13)]
    token_surfaces = []
    
    token_dict={1:"classic1",2:"classic2", 3:"bnw1", 4:"bnw2", 5:"pixel1", 6:"pixel2", 7:"pixel3", 8:"pixel4", 9:"autumn1",
                 10:"autumn2", 11:"autumn3", 12:"autumn4",13:"winter1",14:"winter2",15:"winter3",16:"winter4", 17:"spring1", 
                 18:"spring2",19:"spring3", 20:"summer1",21:"summer2",22:"summer3",23:"summer4", 24:"christmas1",25:"christmas2",
                 26:"christmas3",27:"chinese1",28:"chinese2",29:"chinese3", 30:"valentines1",31:"valentines2",32:"valentines3",
                 33:"st-patrick1",34:"st-patrick2",35:"st-patrick3",36:"easter1",37:"easter2",38:"easter3",39:"easter4", 40:"national1",
                 41:"national2", 42:"national3", 43:"national4",44:"halloween1",45:"halloween2",46:"halloween3",47:"halloween4",
                 48:"thanksgiving1", 49:"thanksgiving2",50:"thanksgiving3",51:"thanksgiving4",52:"skull1", 53:"skull2", 54:"skull3", 
                 55:"skull4",56:"cat1",57:"cat2",58:"cat3",59:"cat4", 60:"cat5",61:"dog1",62:"dog2",63:"dog3",64:"dog4",65:"dino1",
                 66:"dino2",67:"dino3",68:"dino4",69:"fruits1", 70:"fruits2",71:"fruits3",72:"fruits4",73:"fruits5",74:"fruits6",
                 75:"fruits7",76:"fruits8",77:"fruits9",78:"fruits10"}   
    
    for pos in token_positions:
        token_surface = pygame.Surface((77, 77), pygame.SRCALPHA)
        pygame.draw.rect(token_surface, TRANSPARENT, (0, 0, 77, 77))  # Draw hitbox rectangles
        token_surfaces.append((token_surface, pos)) 
        
        
    # add buttons
    player1_hitbox = pygame.Rect(286,159,187,46) 
    pygame.draw.rect(screen, BLACK, player1_hitbox)  

    player2_hitbox = pygame.Rect(513,159,187,46) 
    pygame.draw.rect(screen, BLACK, player2_hitbox) 
    
    con_hitbox = pygame.Rect(740,159,187,46) 
    pygame.draw.rect(screen, BLACK, con_hitbox)  
    
    back_hitbox = pygame.Rect(967,159,187,46) 
    pygame.draw.rect(screen, BLACK, back_hitbox)
    
     
    #Make buttons appear
    pos = pygame.mouse.get_pos() #position de la souris

    if player1_hitbox.collidepoint(pos):
        player1_img = pygame.image.load('themes/buttons/player1_button2.png')
    else : 
        player1_img = pygame.image.load('themes/buttons/player1_button1.png')  
    
    if player2_hitbox.collidepoint(pos):
        player2_img = pygame.image.load('themes/buttons/player2_button2.png')
    else : 
        player2_img = pygame.image.load('themes/buttons/player2_button1.png') 
    
    if con_hitbox.collidepoint(pos):
        con_img = pygame.image.load('themes/buttons/con_button2.png')
    else : 
        con_img = pygame.image.load('themes/buttons/con_button1.png') 
        
    if back_hitbox.collidepoint(pos):
        back_img = pygame.image.load('themes/buttons/back_button2.png')
    else : 
        back_img = pygame.image.load('themes/buttons/back_button1.png') 
     
    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0)) 
    
    # Blit the transparent layers onto the screen
    screen.blit(transparent_layer1, (0, 0))
    screen.blit(transparent_layer2, (0, 0))
    
    # Blit the buttons onto the screen
    screen.blit(player1_img, (286, 149))
    screen.blit(player2_img, (513, 149))
    screen.blit(con_img, (740, 149))
    screen.blit(back_img, (967, 149))
    
    # Blit the hitboxes onto the screen
    for token_surface, token_pos in token_surfaces:
        screen.blit(token_surface, token_pos)
    
    current_player = settings[4]
    selected_token1 = None
    selected_token2 = None
    
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if player1_hitbox.collidepoint(mouse_x, mouse_y):
                current_player = 1
                settings[4]=current_player
            
            if player2_hitbox.collidepoint(mouse_x, mouse_y):
                current_player = 2
                settings[4]=current_player
                
            if con_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[5] = True
                parameters[3] = False
                
            if back_hitbox.collidepoint(mouse_x,mouse_y):
                parameters[1] = True
                parameters[3] = False   
            
            #Selection of an hitbox
            for token_surface, token_pos in token_surfaces:
                token_rect = pygame.Rect(token_pos[0], token_pos[1], 77, 77)
                if token_rect.collidepoint(mouse_x, mouse_y):
                    if current_player == 1:
                        selected_token1 = token_pos
                        transparent_layer1.fill(TRANSPARENT)  # Deselect all hitboxes first
                        pygame.draw.rect(transparent_layer1, TEAL, token_rect, 3)  # Draw a frame around the selected hitbox
                        
                        #find the selected theme's name
                        index = token_positions.index(selected_token1) + 1 
                        player1_token = "themes/tokens/" +  token_dict[index] + ".png"
                        settings[2] = player1_token
                    else:
                        selected_token2 = token_pos
                        transparent_layer2.fill(TRANSPARENT)  # Deselect all hitboxes first
                        pygame.draw.rect(transparent_layer2, PINK, token_rect, 3)  # Draw a frame around the selected hitbox
                        
                        #find the selected theme's name
                        index = token_positions.index(selected_token2) + 1 
                        player2_token = "themes/tokens/" +  token_dict[index] + ".png"
                        settings[3] = player2_token
        
    return parameters, settings

#######        GAME MENU            ########   
def game_menu(parameters, settings):
    # Collect the informations on the settings
    game_background = settings[0]
    game_mode = settings[1]
    print(game_mode)
    player1_token = settings[2]
    player2_token = settings[3]
    g_s = game_state(screen,player1_token,player2_token,game_background)
    player1_mode = settings[5]
    player2_mode = settings[6]
    g_s.random_move_player_0 = False
    g_s.random_move_player_1 = False
    if player1_mode == "camera":
        g_s.player0_cam = True
        g_s.AI_activated_player_0 = False 
    if player2_mode == "camera":
        g_s.player1_cam = True     
        g_s.AI_activated_player_1 = False
   
    if player1_mode == "ai":
       g_s.player0_cam = False
       g_s.AI_activated_player_0 = True

    if player2_mode == "ai":
        g_s.AI_activated_player_1 = True
        g_s.player1_cam = False

    if game_mode == "local":
        parameters[8] = tic_tac_toe(g_s) +1
        # the gameover case is not handled yet, that is when the back button is selected
        if parameters[8] == -1 :
            parameters[1] = True    
        parameters[6] = False
        
    if game_mode == "online":
        if settings[7] == "client" :
            g_s.client = True
            g_s.server = False
        if settings[7] == "server" :
            g_s.client = False
            g_s.server = True
        g_s.IP = str(settings[8])
        g_s.port = int(settings[9])
        parameters[8] = tic_tac_toe(g_s) +1
        # the gameover case is not handled yet, that is when the back button is selected
        if parameters[8] == -1 :
            parameters[1] = True    
        parameters[6] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        
    return parameters, settings

#######        GAME OVER MENU - tie case            ########   
def over_menu0(parameters, settings):
    background_image = pygame.image.load("themes/background/over0-menu-back.png")
    
    # add buttons
    again_hitbox = pygame.Rect(490,452,434,66) 
    pygame.draw.rect(screen, BLACK, again_hitbox)  
    
    quit_hitbox = pygame.Rect(490,562,434,66) 
    pygame.draw.rect(screen, BLACK, quit_hitbox)  

    pos = pygame.mouse.get_pos() 

    if again_hitbox.collidepoint(pos):
        again_img = pygame.image.load('themes/buttons/again1_button2.png')
    else : 
        again_img = pygame.image.load('themes/buttons/again1_button1.png') 
    
    if quit_hitbox.collidepoint(pos):
        quit_img = pygame.image.load('themes/buttons/quit1_button2.png')
    else : 
        quit_img = pygame.image.load('themes/buttons/quit1_button1.png') 
    
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(again_img, (490,452))
    screen.blit(quit_img, (490,562))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if again_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[1] = True
                parameters[8] = -2
                
            if quit_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[0] = False
        
    return parameters, settings    

#######        GAME OVER MENU - player 1 victory            ########   
def over_menu1(parameters, settings):
    background_image = pygame.image.load("themes/background/over1-menu-back.png")
    
    # add buttons
    again_hitbox = pygame.Rect(490,452,434,66) 
    pygame.draw.rect(screen, BLACK, again_hitbox)  
    
    quit_hitbox = pygame.Rect(490,562,434,66) 
    pygame.draw.rect(screen, BLACK, quit_hitbox)  

    pos = pygame.mouse.get_pos() 

    if again_hitbox.collidepoint(pos):
        again_img = pygame.image.load('themes/buttons/again1_button2.png')
    else : 
        again_img = pygame.image.load('themes/buttons/again1_button1.png') 
    
    if quit_hitbox.collidepoint(pos):
        quit_img = pygame.image.load('themes/buttons/quit1_button2.png')
    else : 
        quit_img = pygame.image.load('themes/buttons/quit1_button1.png') 
    
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(again_img, (490,452))
    screen.blit(quit_img, (490,562))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if again_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[1] = True
                parameters[8] = -2
                
            if quit_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[0] = False
        
    return parameters, settings    

#######        GAME OVER MENU - player 2 victory            ########   
def over_menu2(parameters, settings):
    background_image = pygame.image.load("themes/background/over2-menu-back.png")
    
    # add buttons
    again_hitbox = pygame.Rect(490,452,434,66) 
    pygame.draw.rect(screen, BLACK, again_hitbox)  
    
    quit_hitbox = pygame.Rect(490,562,434,66) 
    pygame.draw.rect(screen, BLACK, quit_hitbox)  

    pos = pygame.mouse.get_pos() 

    if again_hitbox.collidepoint(pos):
        again_img = pygame.image.load('themes/buttons/again2_button2.png')
    else : 
        again_img = pygame.image.load('themes/buttons/again2_button1.png') 
    
    if quit_hitbox.collidepoint(pos):
        quit_img = pygame.image.load('themes/buttons/quit2_button2.png')
    else : 
        quit_img = pygame.image.load('themes/buttons/quit2_button1.png') 
    
    # Blit the background image onto the screen
    screen.blit(background_image, (0,0))
    
    # Blit the buttons onto the screen
    screen.blit(again_img, (490,452))
    screen.blit(quit_img, (490,562))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            parameters[0] = False    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if again_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[1] = True
                parameters[8] = -2
                
            if quit_hitbox.collidepoint(mouse_x, mouse_y):
                parameters[0] = False
        
    return parameters, settings 

    
#Main loop
running = parameters[0]
while running:
    # Clear the screen
    screen.fill((0, 0, 0))
    running, main, theme, token, play, ready, game, tuto, over = parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6], parameters[7], parameters[8]
    
    # Management of the pages 
    if main:
        parameters, settings = main_menu(parameters, settings)
    
    if tuto == 1: 
        parameters, settings = tuto_menu1(parameters, settings)
        
    if tuto == 2: 
       parameters, settings = tuto_menu2(parameters, settings)
        
    if tuto == 3: 
        parameters, settings = tuto_menu3(parameters, settings)
    
    if play == "local":
        parameters, settings = play_menu_local(parameters, settings)
    
    if play == "online":
        parameters, settings = play_menu_online(parameters, settings,input_boxes)

    if ready:
        parameters, settings = ready_menu(parameters, settings)
        
    if theme:
        parameters, settings = theme_menu(parameters, settings)
    
    if token:
        parameters, settings = token_menu(parameters, settings)
        
    if game:
        parameters, settings = game_menu(parameters, settings)
    
    if over == 0:
        parameters, settings = over_menu0(parameters, settings)
    
    if over == 1:
        parameters, settings = over_menu1(parameters, settings)
    
    if over == 2:
        parameters, settings = over_menu2(parameters, settings)

    # Update the display
    pygame.display.flip()




# Quit Pygame
pygame.quit()

