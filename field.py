import pygame
class Field:
    def __init__(self,menu_height,rows=10,columns=10,screen_width=1280,screen_height=720):
        self.cell_size_x = screen_width//rows
        self.cell_size_y = (screen_height-menu_height)//columns
        self.field = [[0]*rows for y in range(columns)]
        self.menu_height = menu_height
    def drawing(self,screen,screen_width, screen_height):
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
        return self.field

    def change_field(self, x, y):
        new_field = [[0] * x for i in range(y)]
        for y in range(len(new_field)):
            for x in range(len(new_field[y])):
                if y < len(self.field) and x < len(self.field[0]):
                    new_field[y][x] = self.field[y][x]
        return new_field