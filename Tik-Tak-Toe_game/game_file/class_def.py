import pygame
import random
line_thickness = 2
class grid() :
    def __init__(self,depth,top_corner,width,height,original = False) :
        if original :
            self._matrice =  [['.' for i in range(9)] for j in range(9)]
        x,y = top_corner
        #The surface rect is used for graphic and clics detection
        self._rect = pygame.Rect(x,y,width,height)
        #Last move is used to enforce part of the rule, registering where was the last move
        self._last_move = -1
        #self._color = "black"
        self._color = "white"
        if depth == 0  :
            self._content = "white"
        else : 
            #Here we describe each of the 9 rect in the grid
            new_x,new_y = x+line_thickness,y+line_thickness
            self._content = []
            count = 0
            new_width = (width-2*line_thickness) // 3
            new_height = (height-2*line_thickness) // 3
            for i in range(9) :
                self._content.append(grid(depth-1,(new_x,new_y),new_width,new_height))
                if count == 2 : #If we described 3 rect, then we lower the next 3
                    new_x = x+line_thickness
                    new_y += new_height
                    count = 0
                else :
                    new_x += new_width
                    count += 1
    def last_move(self) :
        return(self._last_move)
    def set_last_move(self,value) :
        self._last_move = value
    def content(self) :
        return(self._content)
    def set_content(self,value) :
        if value == 1 : self._content = "green" 
        else : self._content = "red"
    def rectangle(self) :
        return(self._rect)
    def color(self) :
        return(self._color)
    def set_color(self,value) :
        self._color = value
    def matrice(self) :
        return self._matrice
    
    def is_case(self) :
        return isinstance(self.content(),str)
    def is_last_move_respect(self,coordinates,depth) :
        if self.last_move() != -1 :
            if coordinates[depth-1] != self.last_move() : #if the move is not respecting the last move
                return 1
        return 0
    
    def is_case_taken(self,coordinates,depth) :
        if self.is_case() and depth != 0 :
            return 2
        if depth == 0 and not self.is_case() :
            return 3
        if depth == 0 and self.content() != "white" :
            return 2
        return 0
    
    def take(self,coordinates,depth,player,original = False,test = False) : 
        if coordinates == [] :
            return 4
        if self.is_last_move_respect(coordinates,depth) != 0 :
            return 1
        case_taken = self.is_case_taken(coordinates,depth)
        if case_taken != 0 :
            return case_taken
        if depth == 0 :
            if not test : 
                self.set_content(player)
            return 0
        else :
            # We take the next sub grid
            subgrid = self.content()[coordinates[depth-1]] 
            nb_error = subgrid.take(coordinates,depth-1,player,test = test)
            if nb_error != 0 :
                return nb_error
            if original and not test :
                self.matrice()[coordinates[1]][coordinates[0]] = player
            self.check(player)
            if not(self.is_case()) and not test:
                #If there was no error, we remove the previous last move
                if self.last_move() != -1 :
                    self.content()[self.last_move()].set_color("black")
                    self.set_last_move(-1)
                #If needed we add the new last move
                if depth > 1 :
                    next_case = self.content()[coordinates[depth-2]]
                    if not(isinstance(next_case.content(),str)):
                        self.set_last_move(coordinates[depth-2])
                        next_case.set_color("red")
            return 0


    
    #Here we check if a player as won a grid
    def check(self,player) :
        if player == 1 : 
            color = "green"
        else :
            color = "red"
        if self.is_case() :
            if self.content() == color : 
                return True
            else : 
                return False
        result = [True if case.content() == color else False for case in self.content()]
        for i in range(3) :
            #Check line
            if result[i*3] and result[i*3+1] and result[i*3+2] :
                self.set_content(player)
                return True
            #Check colon
            if result[i] and result[i+3] and result[i+6] :
                self.set_content(player)
                return True
        #Check both diagonals
        if result[0] and result[4] and result[8] :
            self.set_content(player)
            return True
        if result[2] and result[4] and result[6] :
            self.set_content(player)
            return True
        return False
    #Here we translate a tuple into the a list of the grid clicked (from smaller to bigger)
    def translate_coordinate(self,position) :
        if not self.is_case() :
            for i in range(9) :
                if self.content()[i].rectangle().collidepoint(position) :
                    yield from self.content()[i].translate_coordinate(position)
                    yield i
    def victory(self) :
        if self.is_case() :
            if self.content() == "white" :
                return False
            else :
                return True
        else : 
            for case in self.content() :
                if case.is_case() and case.content() == "white" :
                    return False
                elif not case.victory() :
                    return False
            return True
    def random_move(self):
        if self.is_case() : 
            return False
        if self.last_move() != -1 :
            subgrid = self.content()[self.last_move()]
            yield from subgrid.random_move()
            yield self.last_move()
        else :
            done = False
            while not done :
                random_pos = random.randrange(9)
                subgrid = self.content()[random_pos]
                if subgrid.is_case() and subgrid.content() == "white":
                    yield random_pos
                    done = True
                elif not subgrid.is_case() :
                    yield from subgrid.random_move()
                    yield random_pos 
                    done = True
        

#Here we use game state as a list to store all possible parameters of a game.
class game_state() :
    def __init__(self,src,token1,token2,background):
        self.src = src
        self.token1 = token1
        self.token2 = token2
        self.background = background
        self.player0_cam = False
        self.player1_cam = False
        self.AI_activated_player_0 = False
        self.AI_activated_player_1 = False
        self.random_move_player_0 = False
        self.random_move_player_1 = False
        self.client = False
        self.server = False
        self.IP = None
        self.port = None
        