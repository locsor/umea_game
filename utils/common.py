from .core import *

start_auto = False
automation = False
event_flag = True

# canvas_color = (243,223,193)
dark_color = (8, 32, 62)

# canvas = pygame.display.set_mode((1200, 779))
canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
fps = pygame.time.Clock()
pygame.init()
# game_settings = Game()
# ui = UI(canvas)