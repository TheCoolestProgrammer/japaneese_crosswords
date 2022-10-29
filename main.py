class App:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((1280, 720))
        self.events=[]
        self.process_running=True
        self.font = pygame.font.SysFont("Times New Roman", 19)
        self.menu_list = create_menu(self.screen_width)
        self.opened_windows = []
        self.field = Field(20)
        self.menu_is_touched = False
    def events_check(self):
        pos = pygame.mouse.get_pos()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.process_running=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in self.menu_list:
                        self.opened_windows = i.touch_menu(pos,self.menu_list[0],self.opened_windows)
                    for opened_window in self.opened_windows:
                        if is_window_touched(opened_window, pos):
                            # windows switching
                            res = self.opened_windows.index(opened_window)
                            self.opened_windows.insert(len(self.opened_windows), opened_window)
                            del (self.opened_windows[res])
                            # windows actions
                            for x in range(len(opened_window.buttons)):
                                button = opened_window.buttons[x]
                                if button.is_button_touched():
                                    if opened_window.text == "rows":
                                        self.rows_window_action(opened_window,button)

                                    elif opened_window.text == "columns":
                                        self.columns_window_action(opened_window,button)
                                    elif opened_window.text == "save":
                                        self.save_window_action(opened_window,button)
                                    elif opened_window.text == "clear":
                                        self.clear_window_action(opened_window,button)
                            self.menu_is_touched = True

                    if not self.menu_is_touched:
                        self.field.field = self.field.field_value_changer(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for j in self.opened_windows:
                        j.mouse_pos = None

        keys = pygame.mouse.get_pressed()
        # for opened_window in self.opened_windows:
        if len(self.opened_windows)!=0:
            opened_window = self.opened_windows[-1]
            button_is_touched = False

            for j in opened_window.buttons:
                if j.touch_button():
                    button_is_touched = True
                    break
            if not button_is_touched:
                if opened_window.is_window_touched(pos):
                    if not opened_window.mouse_pos:
                        opened_window.mouse_pos = pos
                    if pos != opened_window.mouse_pos:
                        x = opened_window.x - (opened_window.mouse_pos[0] - pos[0])
                        y = opened_window.y - (opened_window.mouse_pos[1] - pos[1])
                        opened_window.__init__(opened_window.text,
                                               opened_window.width,
                                               opened_window.height, x, y, pos)
                    self.menu_is_touched = True
        if not self.menu_is_touched:
            for i in self.menu_list:
                if is_menu_touched(i, pos):
                    self.menu_is_touched = True
                    break

        if not self.menu_is_touched:
            if keys[0]:
                self.field.field_value_changer(1)
            elif keys[2]:
                self.field.field_value_changer(0)
        self.menu_is_touched=False
            # elif event.type == pygame.KEYDOWN:
    def clear_window_action(self,opened_window,button):
        if type(button) == Ok_button:
            self.opened_windows = button.confirm(self.opened_windows, opened_window)
            self.field.field = [[0] * len(self.field.field[0]) for i in range(len(self.field.field))]
        elif type(button) == Exit_button:
            self.exit_from_window(opened_window, button)
    def save_window_action(self,opened_window,button):
        if type(button) == Ok_button:
            self.opened_windows = button.confirm(self.opened_windows,opened_window)
            saving(self.field)
        elif type(button) == Exit_button:
            self.exit_from_window(opened_window, button)
    def columns_window_action(self,opened_window, button):

        if type(button) == Slider_button:
            res = button.touch_button(len(self.field.field))
            self.field.field = self.field.change_field(len(self.field.field[0]), res)
            self.field.cell_size_y = self.screen_height // len(self.field.field)
        elif type(button) == Exit_button:
            self.exit_from_window(opened_window, button)
    def rows_window_action(self,opened_window,button):

        if type(button) == Slider_button:
            res = button.touch_button(len(self.field.field[0]))
            self.field.field = self.field.change_field(res, len(self.field.field))
            self.field.cell_size_x = self.screen_width // len(self.field.field[0])
        elif type(button) == Exit_button:
            self.exit_from_window(opened_window,button)
    def exit_from_window(self,opened_window,button):
        self.opened_windows = button.exit(opened_window, self.opened_windows)
        self.menu_list[0].close_menu_items(self.menu_list[0].submenu)
    def drawing(self):
        self.screen.fill((255,255,255))
        self.field.drawing(self.screen, self.screen_width, self.screen_height)
        self.submenu_draw()
        self.windows_draw()
        pygame.display.update()
    def submenu_draw(self):
        for submenu in self.menu_list:
            submenu.drawing(self.screen,self.font)
    def windows_draw(self):
        for window in self.opened_windows:
            window.drawing(self.screen,self.font)
            for x in range(len(window.buttons)):
                window.buttons[x].drawing(self.screen,self.font)
            for x in range(len(window.widgets)):
                value = 0
                if window.text == "rows":
                    value = len(self.field.field[0])
                elif window.text == "columns":
                    value = len(self.field.field)
                elif window.text=="clear" or window.text == "save":
                    value="sure?"
                window.widgets[x].drawing(value,self.screen)

    def mainloop(self):
        while self.process_running:
            self.events = pygame.event.get()
            self.events_check()
            self.drawing()
if __name__ == '__main__':
    from menu_settings import create_menu
    from windows_system import *
    from field import Field
    app = App()

    app.mainloop()