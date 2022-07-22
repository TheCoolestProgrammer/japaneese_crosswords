import pygame

process_running = True

pygame.init()
clock = pygame.time.Clock()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()
font = pygame.font.SysFont("Times New Roman", 19)
# font = pygame.font.SysFont("comicsansms", 40)
fps = 60
opened_windows = []


def is_touched(x, y, width, height):
    pos = pygame.mouse.get_pos()
    if x < pos[0] < x + width and y < pos[1] < y + height:
        return True
    else:
        return False


class Button:
    def __init__(self, x=200, y=200, width=20, height=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (100, 100, 100)
        self.type = type

    @staticmethod
    def create_slider_button(x, y, width, height, type="less"):
        button = Slider_button(x, y, width, height, type)
        return button

    @staticmethod
    def create_exit_button(x, y, width=20, height=20):
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
        super(Ok_button, self).__init__(x, y, width, height)
        self.color = (0, 200, 0)

    def confirm(self, item):
        del (opened_windows[opened_windows.index(item)])

    def touch_button(self, pos):
        return super(Ok_button, self).is_button_touched()


class Exit_button(Button):
    def __init__(self, x, y, width, height):
        super(Exit_button, self).__init__(x, y, width, height)
        self.color = (200, 0, 0)

    def exit(self, item):
        del (opened_windows[opened_windows.index(item)])

    def touch_button(self, pos):
        return super(Exit_button, self).is_button_touched()


class Slider_button(Button):
    def __init__(self, x, y, width, height, type):
        super(Slider_button, self).__init__(x, y, width, height)
        self.type = type

    def is_button_touched(self):
        return super(Slider_button, self).is_button_touched()

    def touch_button(self, value):
        if self.is_button_touched():
            if self.type == "less":
                value -= 1
                if value > 0:
                    return value
                else:
                    return 1
            else:
                value += 1
                return value
        else:
            return None


class Window:
    def __init__(self, text="window", width=300, height=200, x=200, y=200):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.color = (128, 128, 128)
        self.isactive = False

    def is_window_touched(self, pos):
        return is_touched(self.x, self.y, self.width, self.height)

    @staticmethod
    def create_window_slider(text="window", width=300, height=200, x=200, y=200):
        window = Window_slider(text, width, height, x, y)
        return window

    @staticmethod
    def create_window_ok(text="window", width=300, height=200, x=200, y=200):
        window = Window_ok(text, width, height, x, y)
        return window


class Window_ok(Window):
    def __init__(self, text, width, height, x, y):
        super(Window_ok, self).__init__(text, width, height, x, y)
        self.ok_button = Button()
        self.ok_button = self.ok_button.create_ok_button((x + width) // 3 * 2 - 50, (y + height) // 5 * 4, 100, 20)
        self.exit = Button()
        self.exit = self.exit.create_exit_button(x + width - 20, y, 20, 20)
        self.buttons = [self.ok_button, self.exit]

    def is_window_touched(self, pos):
        return super(Window_ok, self).is_window_touched(pos)


class Window_slider(Window):
    def __init__(self, text, width, height, x, y):
        super(Window_slider, self).__init__(text, width, height, x, y)
        self.less_buton = Button()
        self.less_buton = self.less_buton.create_slider_button(x + 20, y + 20, width // 8, height // 3, "less")
        self.more_buton = Button()
        self.more_buton = self.less_buton.create_slider_button(x + width - 20 - (width // 8), y + 20, width // 8,
                                                               height // 3, "more")
        exit_button = Button()
        self.exit_button = exit_button.create_exit_button(x + width - 20, y, 20, 20)
        self.buttons = [self.less_buton, self.more_buton, self.exit_button]

    def is_window_touched(self, pos):
        return super(Window_slider, self).is_window_touched(pos)


class Menu:
    def __init__(self, width, height, x, y, text=""):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = (128, 128, 128)
        self.submenu = []
        self.link = []
        self.isactive = False
        self.text = text

    def is_mouse_touched(self, pos):
        return is_touched(self.x, self.y, self.width, self.height)


def close_menu_items(item):
    for i in item.submenu:
        i.isactive = False
        close_menu_items(i)


def is_menu_touched(item, pos):
    # for i in menu_list:
    if item.isactive and type(item) == Menu and item.is_mouse_touched(pos):
        return True
    return False


def is_window_touched(item, pos):
    # for i in menu_list:
    if issubclass(type(item), Window) and type(item) != Window:
        res = item.is_window_touched(pos)
        if res:
            return True
    return False


def events_check(menu, menu_list):
    global process_running
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for item in menu_list:
                    if item.isactive and len(item.link) != 0:
                        if item.is_mouse_touched(pos):
                            item.link[0].isactive = True
                            opened_windows.append(item.link[0])
                            close_menu_items(menu)
                    elif item.isactive:
                        for j in item.submenu:
                            if j.is_mouse_touched(pos):
                                if j.isactive:
                                    close_menu_items(item)
                                else:
                                    j.isactive = True


def drawing(menu, menu_list):
    screen.fill((255, 255, 255))
    # draw menu
    for item in menu_list:
        if item.isactive:
            pygame.draw.rect(screen, item.color, (item.x, item.y, item.width, item.height))
            surface = font.render(item.text, False, (255, 255, 255))
            screen.blit(surface, (item.x, item.y))
            for j in item.submenu:
                pygame.draw.rect(screen, j.color, (j.x, j.y, j.width, j.height))
                surface = font.render(j.text, False, (255, 255, 255))
                screen.blit(surface, (j.x, j.y))
    for i in opened_windows:
        pygame.draw.rect(screen, (i.color), (i.x, i.y, i.width, i.height))
        for x in range(len(i.buttons)):
            button = i.buttons[x]
            pygame.draw.rect(screen, (button.color), (button.x, button.y, button.width, button.height))
    pygame.display.update()


def mainloop():
    global process_running
    menu = Menu(screen_width, 20, 0, 0)
    menu_list = []
    while process_running:
        events_check(menu, menu_list)
        drawing(menu, menu_list)

        pygame.time.delay(fps)


if __name__ == '__main__':
    mainloop()
