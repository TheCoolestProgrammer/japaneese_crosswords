import pygame

process_running=True

pygame.init()
clock = pygame.time.Clock()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

fps = 60

def events_check():
    global  process_running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False

def drawing():
    screen.fill((0, 0, 0))
    pygame.display.update()

def mainloop():
    global process_running
    while process_running:
        events_check()
        drawing()
        pygame.time.delay(fps)
if __name__ == '__main__':
    mainloop()