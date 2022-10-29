import pygame
import xlwt
from pathlib import Path

def is_touched(x,y,width,height):
    pos = pygame.mouse.get_pos()
    if x < pos[0] < x + width and y < pos[1] < y + height:
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            return True
        return False
    else:
        return False
def is_menu_touched(item,pos):
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

    def touch_menu(self,pos,main_menu,opened_windows):
        if self.isactive:
            if len(self.link)!=0:
                if self.is_mouse_touched(pos):
                    if self.link[0] not in opened_windows:
                        self.link[0].isactive = True
                        opened_windows.append(self.link[0])
                        self.close_menu_items(main_menu.submenu)
                        self.menu_is_touched = False

            else:
                for j in self.submenu:
                    if j.is_mouse_touched(pos):
                        if j.isactive:
                            self.close_menu_items(self.submenu)
                        else:
                            j.isactive = True
                        self.menu_is_touched = True
                        break
        return opened_windows
    def close_menu_items(self,item):
        for i in item:
            i.isactive = False
            # if type(i) == list():
            self.close_menu_items(i.submenu)
    def drawing(self,screen,font):
        if self.isactive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            surface = font.render(self.text, False, (255, 255, 255))
            screen.blit(surface, (self.x, self.y))
            for j in self.submenu:
                pygame.draw.rect(screen, j.color, (j.x, j.y, j.width, j.height))
                surface = font.render(j.text, False, (255, 255, 255))
                screen.blit(surface, (j.x, j.y))
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
        self.buttons=[]

    def is_window_touched(self,pos):
        return is_touched(self.x, self.y, self.width, self.height)

    def drawing(self,screen,font):
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
class Button:
    def __init__(self,x=200,y=200,width=20,height=20,text=""):
        self.text = text
        self.x = x
        self.y= y
        self.width = width
        self.height = height
        self.color = (100,100,100)
        # self.type = type
    def drawing(self,screen,font):
        pygame.draw.rect(screen, (self.color), (self.x, self.y, self.width, self.height))
        surface = font.render(self.text, False, (255, 255, 255))
        screen.blit(surface, (self.x, self.y))

    @staticmethod
    def create_slider_button(x,y,width,height,type="less",text="<"):
        button = Slider_button(x,y,width,height,type,text)
        return button
    @staticmethod
    def create_exit_button(x,y,width=20,height=20,text="X"):
        button = Exit_button(x, y, width, height,text)
        return button
    @staticmethod
    def create_ok_button(x, y, width=100, height=20,text="OK"):
        button = Ok_button(x, y, width, height,text)
        return button
    def is_button_touched(self):
        return is_touched(self.x, self.y, self.width, self.height)
class Ok_button(Button):
    def __init__(self,x, y, width, height, text):
        super(Ok_button, self).__init__(x,y,width,height,text)
        self.color = (0,200, 0)
    def confirm(self,opened_windows,item):
        del (opened_windows[opened_windows.index(item)])
        return opened_windows
    def touch_button(self,value=0):
        return super(Ok_button, self).is_button_touched()
class Exit_button(Button):
    def __init__(self, x, y, width, height,text):
        super(Exit_button, self).__init__(x,y,width,height,text)
        self.color = (200,0,0)
    def exit(self,item,opened_windows):
        del(opened_windows[opened_windows.index(item)])
        return opened_windows
    def touch_button(self,value=0):
        return super(Exit_button, self).is_button_touched()
class Slider_button(Button):
    def __init__(self,x,y,width,height,type,text):
        super(Slider_button, self).__init__(x,y,width,height,text)
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

class Label():
    def __init__(self, x=280, y=250, width=100, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.type = type
        self.font = pygame.font.SysFont("Times New Roman", 30)
    def drawing(self,value,screen):
        pygame.draw.rect(screen, (self.color), (self.x, self.y, self.width, self.height))
        surface = self.font.render(str(value), False, (100, 100, 100))
        screen.blit(surface, (self.x+50, self.y))
class Window_ok(Window):
    def __init__(self,text,width,height,x,y,mouse_pos):
        super(Window_ok, self).__init__(text,width,height,x,y,mouse_pos)
        self.ok_button = Button()
        self.ok_button =self.ok_button.create_ok_button((x+width)//3*2-50,(y+height)//5*4,100,20)
        self.exit = Button()
        self.exit = self.exit.create_exit_button(x+width-20,y,20,20)
        self.buttons = [self.ok_button,self.exit]
        self.label = Label(x + 20 + width // 8 + 10, y + 20, 150, height // 3)
        self.widgets = [self.label]
    def is_window_touched(self,pos):
        return super(Window_ok,self).is_window_touched(pos)
class Window_slider(Window):
    def __init__(self,text,width,height,x,y,mouse_pos):
        super(Window_slider, self).__init__(text,width,height,x,y,mouse_pos)
        self.less_buton = Button()
        self.less_buton = self.less_buton.create_slider_button(x+20,y+20,width//8,height//3,"less","<")
        self.more_buton = Button()
        self.more_buton = self.less_buton.create_slider_button(x+width-20-(width//8),y+20,width//8,height//3,"more",">")
        exit_button = Button()
        self.exit_button = exit_button.create_exit_button(x+width-20,y,20,20)
        self.label = Label(x+20+width//8+10, y+20,150,height//3)
        self.widgets=[self.label]
        self.buttons = [self.less_buton,self.more_buton,self.exit_button]
    def is_window_touched(self,pos):
        return super(Window_slider,self).is_window_touched(pos)