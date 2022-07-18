import pygame

process_running=True

pygame.init()
clock = pygame.time.Clock()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

fps = 60
class Field:
    def __init__(self,menu_height,rows=10,columns=10):
        self.cell_size_x = screen_width//rows
        self.cell_size_y = (screen_height-menu_height)//columns
        self.field = [[0]*rows for y in range(columns)]
class Menu:
    def __init__(self):
        self.height = 20
        self.width = screen_width
def coordinates_changer_in_field(pos,field,menu):
    if pos[1]<menu.height or pos[0]<0:
        return None
    new_y = (pos[1]-menu.height)//field.cell_size_y
    new_x = pos[0]//field.cell_size_x
    return (new_x,new_y)
def coordinates_changer_from_field(pos,field,menu):
    new_x = field.cell_size_x*pos[0]
    new_y = menu.height+field.cell_size_y*pos[1]
    return (new_x,new_y)
def field_value_changer(value,field,menu):
    pos = pygame.mouse.get_pos()
    pos = coordinates_changer_in_field(pos, field, menu)
    if pos:
        field.field[pos[1]][pos[0]] = value
def events_check(field,menu):
    global process_running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                field_value_changer(1,field,menu)
            if event.button == 3:
                field_value_changer(0, field, menu)
    keys = pygame.mouse.get_pressed()
    if keys[0]:
        field_value_changer(1, field, menu)
    elif keys[2]:
        field_value_changer(0, field, menu)

def drawing(field,menu):
    screen.fill((255, 255, 255))
    for y in range(menu.height,screen_height,field.cell_size_y):
        pygame.draw.line(screen,(0,0,0),(0,y),(screen_width,y),3)
    for x in range(0,screen_width,field.cell_size_x):
        pygame.draw.line(screen,(0,0,0),(x,0),(x,screen_height),3)

    for y in range(len(field.field)):
        for x in range(len(field.field[y])):
            if field.field[y][x] == 1:
                pos = coordinates_changer_from_field((x,y),field,menu)
                pygame.draw.rect(screen,(0,0,0),(pos[0],pos[1],field.cell_size_x,field.cell_size_y))
    pygame.display.update()

def mainloop():
    global process_running
    menu = Menu()
    field = Field(menu.height)

    while process_running:
        events_check(field,menu)
        drawing(field,menu)
        pygame.time.delay(fps)
if __name__ == '__main__':
    mainloop()