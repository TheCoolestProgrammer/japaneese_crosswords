import pygame

process_running=True

pygame.init()
clock = pygame.time.Clock()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()
font = pygame.font.SysFont("Times New Roman",19)
# font = pygame.font.SysFont("comicsansms", 40)
fps = 60
class Field:
    def __init__(self,menu_height,rows=10,columns=10):
        self.cell_size_x = screen_width//rows
        self.cell_size_y = (screen_height-menu_height)//columns
        self.field = [[0]*rows for y in range(columns)]

class Button:
    def __init__(self,x=200,y=200,width=20,height=20):
        self.x = x
        self.y= y
        self.width = width
        self.height = height
        self.color = (100,100,100)
        self.type = type
    @staticmethod
    def create_slider_button(x,y,width,height,type="less"):
        button = Slider_button(x,y,width,height,type)
        return button
class Slider_button(Button):
    def __init__(self,x,y,width,height,type):
        super(Slider_button, self).__init__(x,y,width,height)
        self.type = type
    def is_button_touched(self,pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False
    def touch_button(self,value):
        pos = pygame.mouse.get_pos()
        if self.is_button_touched(pos):
            if self.type == "less":
                value -=1
                if value >0:
                    return value
                else:
                    return 1
            else:
                value += 1
                return value

class Window:
    def __init__(self,text="window",width=300,height=200,x=200,y=200):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.color = (128,128,128)
        self.isactive = False
    @staticmethod
    def create_window_slider(value,text="window",width=300,height=200,x=200,y=200):
        window = Window_slider(value,text,width,height,x,y)
        return window

class Window_slider(Window):
    def __init__(self,value,text,width,height,x,y):
        super(Window_slider, self).__init__(text,width,height,x,y)
        self.less_buton = Button()
        self.less_buton = self.less_buton.create_slider_button(x+20,y+20,width//8,height//3,"less")
        self.more_buton = Button()
        self.more_buton = self.less_buton.create_slider_button(x+width-20-(width//8),y+20,width//8,height//3,"more")
        self.buttons = [self.less_buton,self.more_buton]
        self.value = value
class Menu:
    def __init__(self,width,height,x,y,text=""):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = (128,128,128)
        self.submenu = []
        self.link=[]
        self.isactive = False
        self.text = text
    def is_mouse_touched(self,pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False
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
def events_check(field,menu,menu_list):
    global process_running
    menu_is_touched = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for item in menu_list:
                    if len(item.submenu) == 0 and len(item.link)!=0:
                        if item.is_mouse_touched(pos):
                            item.link[0].isactive = True
                            item.isactive = True
                            menu_is_touched=True
                            break
                    elif item.isactive:
                        for j in item.submenu:
                            if j.is_mouse_touched(pos):
                                j.isactive = True
                                menu_is_touched=True
                                break
                if not menu_is_touched:

                    field_value_changer(1,field,menu)
            if event.button == 3 and not menu_is_touched:
                field_value_changer(0, field, menu)
    pos = pygame.mouse.get_pos()
    for item in menu_list:
        if len(item.submenu) == 0 and len(item.link) != 0:
            if item.is_mouse_touched(pos):
                menu_is_touched = True
                break
    if not menu_is_touched:
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            field_value_changer(1, field, menu)
        elif keys[2]:
            field_value_changer(0, field, menu)
def drawing(field,menu,menu_list):
    screen.fill((255, 255, 255))
    #draw field
    for y in range(menu.height,screen_height,field.cell_size_y):
        pygame.draw.line(screen,(0,0,0),(0,y),(screen_width,y),3)
    for x in range(0,screen_width,field.cell_size_x):
        pygame.draw.line(screen,(0,0,0),(x,0),(x,screen_height),3)

    for y in range(len(field.field)):
        for x in range(len(field.field[y])):
            if field.field[y][x] == 1:
                pos = coordinates_changer_from_field((x,y),field,menu)
                pygame.draw.rect(screen,(0,0,0),(pos[0],pos[1],field.cell_size_x,field.cell_size_y))
    #draw menu
    for item in menu_list:
        if item.isactive:
            pygame.draw.rect(screen,item.color,(item.x,item.y,item.width,item.height))
            surface = font.render(item.text, False, (255, 255, 255))
            screen.blit(surface, (item.x, item.y))
            for j in item.submenu:
                pygame.draw.rect(screen, j.color, (j.x, j.y, j.width, j.height))
                surface = font.render(j.text,False,(255,255,255))
                screen.blit(surface,(j.x,j.y))
    #draw windows
    for i in menu_list:
        if i.isactive and len(i.link)>0 and i.link[0].isactive:
            pygame.draw.rect(screen,(i.link[0].color),(i.link[0].x,i.link[0].y,i.link[0].width,i.link[0].height))
            for x in range(len(i.link[0].buttons)):
                button = i.link[0].buttons[x]
                pygame.draw.rect(screen,(button.color),(button.x,button.y,button.width,button.height))
    pygame.display.update()

def mainloop():
    global process_running
    # describe menu
    menu_width = 100
    menu_height = 20
    menu = Menu(screen_width,20,0,0)
    #block 0
    file_menu= Menu(menu_width,menu_height,0,0,"file")
    field_menu= Menu(menu_width,menu_height,menu_width,0,"field")
    menu.submenu.append(file_menu)
    menu.submenu.append(field_menu)
    menu.isactive = True
    #block1
    save_menu = Menu(menu_width,menu_height,0,menu_height,"save")
    load_menu = Menu(menu_width,menu_height,0,menu_height*2,"load")
    file_menu.submenu.append(save_menu)
    file_menu.submenu.append(load_menu)

    save_window = Window("save as")
    load_window = Window("what kind load?")

    save_menu.link.append(save_window)
    load_menu.link.append(load_window)
    #block2
    rows_menu = Menu(menu_width, menu_height, menu_width, menu_height, "rows")
    columns_menu = Menu(menu_width, menu_height, menu_width, menu_height * 2, "columns")
    clear_menu = Menu(menu_width, menu_height, menu_width, menu_height * 3, "clear")
    field_menu.submenu.append(rows_menu)
    field_menu.submenu.append(columns_menu)
    field_menu.submenu.append(clear_menu)

    field = Field(menu.height)

    rows_window = Window()
    rows_window = rows_window.create_window_slider(len(field.field[0]),"rows")
    columns_window = Window()
    columns_window = columns_window.create_window_slider(len(field.field),"columns")
    clear_window = Window()
    clear_window = clear_window.create_window_slider("really clear?")

    rows_menu.link.append(rows_window)
    columns_menu.link.append(columns_window)
    clear_menu.link.append(clear_window)

    menu_list = [menu,file_menu,save_menu,load_menu,field_menu, rows_menu,columns_menu,clear_menu]

    while process_running:
        events_check(field,menu,menu_list)
        drawing(field,menu,menu_list)
        print(rows_window.buttons)
        pygame.time.delay(fps)
if __name__ == '__main__':
    mainloop()