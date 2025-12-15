import pygame, pygame_widgets
from pygame.locals import *
from utils.common import *
from utils.core import *

font = pygame.font.SysFont('Grand9K Pixel',25)
font_small = pygame.font.SysFont('Grand9K Pixel',18)

text_newday = font.render('Next Day', False, (0, 0, 0))
text_newday_size = font.size('Next Day')

text_nextcase = font.render('Next Case', False, (0, 0, 0))
text_nextcase_size = font.size('Next Case')

text_automation = font.render('Automation', False, (0, 0, 0))
text_automation_size = font.size('Automation')

news1 = 'News of the Day: All\'s right with the world!'

note1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

case1 = {'name':'Test',
		 'address': 'Test Street',
		 'age': 100,
		 'occupation':'Test',
		 'code':41,
		 'wage':100000,
		 'welfare_request': 0,
		 'note':'Test case',}

custom_cases = [case1]
custom_cases_info = [[2,2], [3,3]]