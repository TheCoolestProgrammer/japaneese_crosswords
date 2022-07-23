import pygame
import xlrd,xlwt
from pathlib import Path

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
opened_windows=[]
def is_touched(x,y,width,height):
    pos = pygame.mouse.get_pos()
    if x < pos[0] < x + width and y < pos[1] < y + height:
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            return True
        return False
    else:
        return False

class Field:
    def __init__(self,menu_height,rows=10,columns=10):
        self.cell_size_x = screen_width//rows
        self.cell_size_y = (screen_height-menu_height)//columns
        self.field = [[0]*rows for y in range(columns)]
        self.menu_height = menu_height
    def drawing(self):
        for y in range(self.menu_height, screen_height, self.cell_size_y):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (screen_width, y), 3)
        for x in range(0, screen_width, self.cell_size_x):
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, screen_height), 3)

        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x] == 1:
                    pos = self.coordinates_changer_from_field((x, y))
                    pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], self.cell_size_x, self.cell_size_y))

    def coordinates_changer_in_field(self,pos):
        if pos[1] < self.menu_height or pos[0] < 0 or pos[0] >= self.cell_size_x * len(self.field[0]) or pos[1] >= self.cell_size_y * len(self.field):
            return None
        new_y = (pos[1] - self.menu_height) // self.cell_size_y
        new_x = pos[0] // self.cell_size_x
        return (new_x, new_y)

    def coordinates_changer_from_field(self,pos):
        if pos[0] >= len(self.field[0]) or pos[1] >= len(self.field) or pos[0] < 0 or pos[1] < 0:
            return None
        new_x = self.cell_size_x * pos[0]
        new_y =self.menu_height + self.cell_size_y * pos[1]
        return (new_x, new_y)

    def field_value_changer(self,value):
        pos = pygame.mouse.get_pos()
        pos = self.coordinates_changer_in_field(pos)
        if pos:
            self.field[pos[1]][pos[0]] = value

    def change_field(self, x, y):
        new_field = [[0] * x for i in range(y)]
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if y < len(new_field) and x < len(self.field[0]) - 1:
                    new_field[y][x] = self.field[y][x]
        self.field = new_field
class Button:
    def __init__(self,x=200,y=200,width=20,height=20):
        self.x = x
        self.y= y
        self.width = width
        self.height = height
        self.color = (100,100,100)
        self.type = type
    def drawing(self):
        pygame.draw.rect(screen, (self.color), (self.x, self.y, self.width, self.height))

    @staticmethod
    def create_slider_button(x,y,width,height,type="less"):
        button = Slider_button(x,y,width,height,type)
        return button
    @staticmethod
    def create_exit_button(x,y,width=20,height=20):
        button = Exit_button(x, y, width, height)
        return button
    @staticmethod
    def create_ok_button(x, y, width=100, height=20):
        button = Ok_button(x, y, width, height)
        return button
    def is_button_touched(self):
        return is_touched(self.x, self.y, self.width, self.height)
class Ok_button(Button):
    def __init__(self, x, y, width, height):
        super(Ok_button, self).__init__(x,y,width,height)
        self.color = (0,200, 0)
    def confirm(self,item):
        del (opened_windows[opened_windows.index(item)])
    def touch_button(self,value=0):
        return super(Ok_button, self).is_button_touched()
class Exit_button(Button):
    def __init__(self, x, y, width, height):
        super(Exit_button, self).__init__(x,y,width,height)
        self.color = (200,0,0)
    def exit(self,item):
        del(opened_windows[opened_windows.index(item)])
    def touch_button(self,value=0):
        return super(Exit_button, self).is_button_touched()
class Slider_button(Button):
    def __init__(self,x,y,width,height,type):
        super(Slider_button, self).__init__(x,y,width,height)
        self.type = type
    def is_button_touched(self):
        return super(Slider_button, self).is_button_touched()
    def touch_button(self,value=0):
        if self.is_button_touched():
            if self.type == "less":
                value -=1
                if value >0:
                    return value
                else:
                    return 1
            else:
                value += 1
                return value
        else:
            return None


class Window:
    def __init__(self,text="window",width=300,height=200,x=200,y=200,mouse_pos=None):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.color = (128,128,128)
        self.isactive = False
        self.mouse_pos=mouse_pos
    def is_window_touched(self,pos):
        return is_touched(self.x, self.y, self.width, self.height)
    def drawing(self):
        pygame.draw.rect(screen, (self.color), (self.x, self.y, self.width, self.height))
        surface = font.render(self.text, False, (255, 255, 255))
        screen.blit(surface, (self.x, self.y))

    @staticmethod
    def create_window_slider(text="window",width=300,height=200,x=200,y=200,mouse_pos=None):
        window = Window_slider(text,width,height,x,y,mouse_pos)
        return window
    @staticmethod
    def create_window_ok(text="window",width=300,height=200,x=200,y=200,mouse_pos=None):
        window = Window_ok(text,width,height,x,y,mouse_pos)
        return window
class Window_ok(Window):
    def __init__(self,text,width,height,x,y,mouse_pos):
        super(Window_ok, self).__init__(text,width,height,x,y,mouse_pos)
        self.ok_button = Button()
        self.ok_button =self.ok_button.create_ok_button((x+width)//3*2-50,(y+height)//5*4,100,20)
        self.exit = Button()
        self.exit = self.exit.create_exit_button(x+width-20,y,20,20)
        self.buttons = [self.ok_button,self.exit]
    def is_window_touched(self,pos):
        return super(Window_ok,self).is_window_touched(pos)
class Window_slider(Window):
    def __init__(self,text,width,height,x,y,mouse_pos):
        super(Window_slider, self).__init__(text,width,height,x,y,mouse_pos)
        self.less_buton = Button()
        self.less_buton = self.less_buton.create_slider_button(x+20,y+20,width//8,height//3,"less")
        self.more_buton = Button()
        self.more_buton = self.less_buton.create_slider_button(x+width-20-(width//8),y+20,width//8,height//3,"more")
        exit_button = Button()
        self.exit_button = exit_button.create_exit_button(x+width-20,y,20,20)
        self.buttons = [self.less_buton,self.more_buton,self.exit_button]
    def is_window_touched(self,pos):
        return super(Window_slider,self).is_window_touched(pos)
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
        return is_touched(self.x,self.y,self.width,self.height)
    def drawing(self):
        if self.isactive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            surface = font.render(self.text, False, (255, 255, 255))
            screen.blit(surface, (self.x, self.y))
            for j in self.submenu:
                pygame.draw.rect(screen, j.color, (j.x, j.y, j.width, j.height))
                surface = font.render(j.text, False, (255, 255, 255))
                screen.blit(surface, (j.x, j.y))

def close_menu_items(item):
    for i in item.submenu:
        i.isactive=False
        close_menu_items(i)
def is_menu_touched(item,pos):
    # for i in menu_list:
    if item.isactive and type(item)==Menu and item.is_mouse_touched(pos):
        return True
    return False
def is_window_touched(item,pos):
    # for i in menu_list:
    if issubclass(type(item),Window) and type(item) != Window:
        res = item.is_window_touched(pos)
        if res:
            return True
    return False
def saving(field):
    print("_++++++++++++++++_")
    horisontal_lines=[]
    for i in field.field:
        line = []
        counter=0
        for j in i:
            if j == 0:
                if counter !=0:
                    line.append(counter)
                counter=0
            else:
                counter+=1
        if i[-1]==1:
            line.append(counter)
        horisontal_lines.append(line)
    vertical_lines=[]
    for i in range(len(field.field[0])):
        line = []
        counter=0
        for j in range(len(field.field)):
            if field.field[j][i] == 0:
                if counter != 0:
                    line.append(counter)
                counter = 0
            else:
                counter += 1
        if field.field[-1][i]==1:
            line.append(counter)
        vertical_lines.append(line)
    maximal_vertical_length=0
    maximal_horisontal_length=0
    for i in vertical_lines:
        if len(i)>maximal_vertical_length:
            maximal_vertical_length=len(i)
    for i in horisontal_lines:
        if len(i) > maximal_horisontal_length:
            maximal_horisontal_length = len(i)
    wb = xlwt.Workbook()
    ws = wb.add_sheet("crossword")
    for y in range(len(horisontal_lines)):
        for x in range(len(horisontal_lines[y])):
            ws.write(y+maximal_vertical_length, x+ maximal_horisontal_length - len(horisontal_lines[y]),horisontal_lines[y][x])
    for x in range(len(vertical_lines)):
        for y in range(len(vertical_lines[x])):
            ws.write(y + maximal_vertical_length - len(vertical_lines[x]),x + maximal_horisontal_length,vertical_lines[x][y])
    folder = Path("projects/")
    counter=0
    for i in folder.iterdir():
        if "crossword" in str(i) and ".xls" in str(i):
            counter+=1
    wb.save(f"projects/crossword{counter}.xls")

def events_check(field,menu,menu_list):
    global process_running
    menu_is_touched = False
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in opened_windows:
                    if is_window_touched(i,pos):
                        for x in range(len(i.buttons)):
                            button = i.buttons[x]
                            if i.text == "rows":
                                res = button.touch_button(len(field.field[0]))
                                if res:
                                    if type(button) == Slider_button:
                                        field.change_field(res,len(field.field))
                                        field.cell_size_x = screen_height//len(field.field[0])
                                    elif type(button) == Exit_button:
                                        button.exit(i)
                                        close_menu_items(menu)
                                        menu.isactive = True
                            elif i.text == "columns":
                                res = button.touch_button(len(field.field))
                                if res:
                                    if type(button) == Slider_button:
                                        field.change_field(len(field.field[0]), res)
                                        field.cell_size_y = (screen_height - menu.height) // len(field.field)
                                    elif type(button) == Exit_button:
                                        button.exit(i)
                                        close_menu_items(menu)
                                        menu.isactive = True
                            elif i.text == "save":
                                res = button.touch_button()
                                if res:
                                    if type(button) == Ok_button:
                                        button.confirm(i)
                                        saving(field)
                                    elif type(button) == Exit_button:
                                        button.exit(i)
                                        close_menu_items(menu)
                                        menu.isactive = True
                            elif i.text == "clear":
                                res = button.touch_button()
                                if res:
                                    if type(button) == Ok_button:
                                        button.confirm(i)
                                        field.field = [[0]*len(field.field[0]) for i in range(len(field.field))]
                                    elif type(button) == Exit_button:
                                        button.exit(i)
                                        close_menu_items(menu)
                                        menu.isactive = True

                        menu_is_touched = True
                for item in menu_list:
                    if item.isactive and len(item.link)!=0:
                        if item.is_mouse_touched(pos):
                            item.link[0].isactive = True
                            opened_windows.append(item.link[0])
                            close_menu_items(menu)
                            # menu.isactive=True
                            # item.isactive = True
                            menu_is_touched=True
                            break
                    elif item.isactive:
                        for j in item.submenu:
                            if j.is_mouse_touched(pos):
                                if j.isactive:
                                    close_menu_items(item)
                                else:
                                    j.isactive = True
                                menu_is_touched=True
                                break
                if not menu_is_touched:
                    field.field_value_changer(1)
            if event.button == 3:
                for i in opened_windows:
                    if is_window_touched(i,pos):
                        menu_is_touched = True
                        break
                if not menu_is_touched:
                    for item in menu_list:
                        if len(item.link)!=0:
                            if item.is_mouse_touched(pos):
                                menu_is_touched=True
                                break
                        elif item.isactive:
                            if item.is_mouse_touched(pos):
                                menu_is_touched = True
                                break
                if not menu_is_touched:
                    field.field_value_changer(0)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for j in opened_windows:
                    j.touch_button=None
    # проверка на зажатие
    keys = pygame.mouse.get_pressed()
    for i in opened_windows:
        if is_window_touched(i, pos) and (keys[0] or keys[2]):
            button_is_touched = False
            for j in i.buttons:
                if j.touch_button():
                    button_is_touched = True
                    break
            if not button_is_touched:
                if not i.mouse_pos:
                    i.mouse_pos= pos
                if pos !=i.mouse_pos:
                    x = i.x - (i.mouse_pos[0] -pos[0])
                    y = i.y - (i.mouse_pos[1] -pos[1])
                    i.__init__(i.text,i.width,i.height,x,y,pos)
            menu_is_touched = True
            break
    if not menu_is_touched:
        for i in menu_list:
            if is_menu_touched(i,pos):
                menu_is_touched = True
                break

    if not menu_is_touched:
        if keys[0]:
            field.field_value_changer(1)
        elif keys[2]:
            field.field_value_changer(0)
    if menu_is_touched:
        print("____________________________")
def drawing(field,menu_list):
    screen.fill((255, 255, 255))
    #draw field
    field.drawing()
    #draw windows
    for i in opened_windows:
        i.drawing()
        for x in range(len(i.buttons)):
            i.buttons[x].drawing()
    # draw menu
    for item in menu_list:
        item.drawing()
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
    # load_menu = Menu(menu_width,menu_height,0,menu_height*2,"load")
    file_menu.submenu.append(save_menu)
    # file_menu.submenu.append(load_menu)

    save_window = Window("save as")
    save_window = save_window.create_window_ok("save")

    save_menu.link.append(save_window)
    #block2
    rows_menu = Menu(menu_width, menu_height, menu_width, menu_height, "rows")
    columns_menu = Menu(menu_width, menu_height, menu_width, menu_height * 2, "columns")
    clear_menu = Menu(menu_width, menu_height, menu_width, menu_height * 3, "clear")
    field_menu.submenu.append(rows_menu)
    field_menu.submenu.append(columns_menu)
    field_menu.submenu.append(clear_menu)

    field = Field(menu.height)

    rows_window = Window()
    rows_window = rows_window.create_window_slider("rows")
    columns_window = Window()
    columns_window = columns_window.create_window_slider("columns")
    clear_window = Window()
    clear_window = clear_window.create_window_ok("clear")

    rows_menu.link.append(rows_window)
    columns_menu.link.append(columns_window)
    clear_menu.link.append(clear_window)

    menu_list = [menu,file_menu,save_menu,field_menu, rows_menu,columns_menu,clear_menu]

    while process_running:
        events_check(field,menu,menu_list)
        drawing(field,menu_list)
        pygame.time.delay(fps)
if __name__ == '__main__':
    mainloop()