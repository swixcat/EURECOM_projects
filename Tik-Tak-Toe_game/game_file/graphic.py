import pygame
line_thickness = 2

def text_creation(text):
    pygame.font.init()
    font = pygame.font.Font(None,36)
    text_font = font.render(text, 1, pygame.Color("white"))
    textpos = text_font.get_rect()
    return (text_font,textpos)

def text_showing(text,src,background):
    text_font,textpos = text_creation(text)
    texpos_center_x,texpos_center_y = src.get_size()
    texpos_center_x,texpos_center_y = texpos_center_x//2,texpos_center_y//2
    textpos.center = (texpos_center_x,texpos_center_y)
    load_background(src,background)
    src.blit(text_font,textpos)
    pygame.display.flip()
    pygame.time.delay(1000)


def draw(grid,src,token1,token2,background) :
    load_background(src,background)
    draw_case(grid,src,token1,token2)

def load_background(src,background):
    background = pygame.image.load(background)
    screen_size = src.get_size()
    background = pygame.transform.scale(background,(screen_size))
    src.blit(background,src.get_rect())

def draw_case(grid,src,token1,token2) :
    if grid.is_case() :
            if grid.content() != "white" :   
                if grid.content() == "red" :
                    case = pygame.image.load(token1)
                if grid.content() == "green" :
                    case = pygame.image.load(token2)
                case_size= grid.rectangle().size
                case = pygame.transform.scale(case,(case_size))
                src.blit(case,grid.rectangle())
    else :
        for sub_grid in grid.content() :
            draw_case(sub_grid,src,token1,token2)
    pygame.draw.rect(src,pygame.Color(grid.color()),grid.rectangle(),line_thickness)

def postion_main_grid(surface):
    width,height = surface.get_size()
    ref_width, ref_height = 1440,810
    ratio_width = width/ref_width
    ratio_height = height/ref_height
    ratio = min(ratio_width,ratio_height)
    size_square = 549*ratio
    top_corner_x = 444*ratio
    top_corner_y = 131*ratio
    return (size_square,top_corner_x,top_corner_y)
