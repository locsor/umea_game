from faker import Faker
from datetime import date
import random, datetime
import pandas as pd

from sklearn.linear_model import LinearRegression

import pygame, pygame_widgets
from pygame.locals import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from utils.core import *
from utils.fonts import *
from utils.common import *

fake = Faker('en_GB')

normalization_vals = []

wage_url = resource_path('data/wage.csv')
wage = pd.read_csv(wage_url)
jobs_url = resource_path('data/jobs_new.csv')
jobs = pd.read_csv(jobs_url)

def train_model():
	global normalization_vals

	df_url = resource_path('data/data.csv')
	df_data = pd.read_csv(df_url)

	for column in df_data.columns:
		normalization_vals += [df_data[column].abs().max()]
		df_data[column] = df_data[column] / df_data[column].abs().max()

	features = ['age', 'code', 'wage']
	X = df_data[features]
	y = df_data['benifit']

	model = LinearRegression()
	model.fit(X, y)

	return model

def main():
	global settings, canvas, fps

	start_auto = False
	automation = False
	event_flag = True
	show_profile = False
	ct = 0
	news_offset = 0
	event_sys = Events()

	model = train_model()

	pygame.time.set_timer(pygame.USEREVENT, 1000)

	slider = Slider(canvas, 0.34375*ui.width, 0.75*ui.height, 0.3125*ui.width, 0.042*ui.height,
					min=0, max=100, step=1, curved=True, initial=50)
	slider.hide()

	settings.new_day_fill(wage, jobs, model)

	case = settings.cases[settings.current_case]

	# section_main = pygame.Surface((1100, 630))
	# section_main.fill((250, 213, 230))
	# section_main_rect = section_main.get_rect(center=(0.4296875*ui.width, 0.5625*ui.height))

	while True:
		canvas.fill(canvas_color)
		mouse = pygame.mouse.get_pos()
		events = pygame.event.get()

		# canvas.blit(section_main, section_main_rect)

		for event in events:
			if event.type == QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				
				#Start Automation
				if ui.buttons.auto_button.collidepoint((mouse[0], mouse[1])):
					automation = not automation
				
				#Next Case
				if ui.buttons.case_button.collidepoint((mouse[0], mouse[1])) and type(settings.out) == int and automation == False:
					if not settings.case_show: #If the case is not open
						if settings.new_game:
							settings.new_game = False
						if settings.show_new_day:
							settings.show_new_day = False

						settings.new_day_fill(wage, jobs, model)
						case = settings.cases[settings.current_case]
						settings.new_day = False
						settings.case_show = True
						ratio = 100*(case.welfare_suggested/10000)
						slider = Slider(canvas, int(0.34375*ui.width), int(0.75*ui.height),
										int(0.3125*ui.width), int(0.042*ui.height),
										min=0, max=100, step=1, curved=True, initial=int(ratio))
							
					elif settings.case_show: #if the case view is already opened
						ratio = 100*(case.welfare_suggested/10000)
						slider = Slider(canvas, int(0.34375*ui.width), int(0.75*ui.height),
										int(0.3125*ui.width), int(0.042*ui.height),
										min=0, max=100, step=1, curved=True, initial=int(ratio))

						settings = complete_case(case, settings, True)

						if not settings.new_day:
							if settings.current_case < settings.case_num[settings.day-1]-1:
								settings.current_case += 1
							else:
								settings.new_day = True
								settings.show_new_day = True
							case = settings.cases[settings.current_case]
							ratio = 100*(case.welfare_suggested/10000)
							
				if ui.buttons.restart_button.collidepoint((mouse[0], mouse[1])): #Restart Logic
					automation = False
					settings.new_game = True
					settings = Game()
					# settings.new_day_fill(wage, jobs, model)

				if ui.buttons.right1_button.collidepoint((mouse[0], mouse[1])):
					if settings.preview_case < len(settings.cases_preview)-1:
						settings.preview_case += 1
				if ui.buttons.left1_button.collidepoint((mouse[0], mouse[1])):
					if settings.preview_case > 0:
						settings.preview_case -= 1

				if ui.buttons.right2_button.collidepoint((mouse[0], mouse[1])):
					if settings.comp_case < len(settings.cases_completed)-1:
						settings.comp_case += 1
				if ui.buttons.left2_button.collidepoint((mouse[0], mouse[1])):
					if settings.comp_case > 0:
						settings.comp_case -= 1

				if ui.buttons.profile_button.collidepoint((mouse[0], mouse[1])):
					show_profile = not show_profile
					
					
			if event.type == pygame.USEREVENT:
				if not settings.out_of_time and type(settings.out) == int and not settings.new_game:
					settings.counter -= 1
					
				if settings.counter <= 0:
					settings.out_of_time = True

				if type(settings.out) != int and not settings.new_game:
					settings.restart_timer -=1
					if settings.restart_timer <= 0:
						settings.restart_timer = 30
						automation = False
						settings.new_game = True
						settings = Game()


		automation, settings, case, ct = auto(automation, settings, case, ct) #Automation logic

		if settings.new_day == True:
			settings.day += 1
			settings.new_day = False
			settings.case_show = False
			event_flag = True
			settings.counter = settings.time_total

		if settings.show_new_day:
			automation = False
			if settings.day == 2 and event_flag:
				event_flag = False
				event_text = event_sys.event1(settings)
			elif settings.day !=2 and event_flag:
				event_flag = False
				event_text = event_sys.event0(settings)
			ui.new_day(event_text)

		settings.out = gameover(settings.budget, settings.happiness, settings.case_num, 
									 settings.out_of_time, settings.day, settings.out) #Gameover logic
		ui.update_stats(settings)

		news = ui.update_other(news_offset)
		w_news = news.get_size()[0]
		news_offset += int(0.003125*ui.width)
		if news_offset > ui.width:
			news_offset = -w_news
		
		ui.render_buttons()

		if type(settings.out) != int or settings.new_game:
			automation = False
			if settings.new_game:
				ui.game_over('New Game')
			else:
				ui.game_over(settings.out)
				canvas.blit(ui.images.restart_image, ui.buttons.restart_button)
		else:
			if settings.case_show:
				ui.update_case_box_accepted(settings)
				case.viz_case()
				slider.show()

				settings.funding = slider.getValue()*(case.welfare_suggested/ratio)

				text5 = ui.font.render(str(int(settings.funding)), False, (0, 0, 0))
				canvas.blit(text5, (0.7*ui.width,0.75*ui.height))
			else:
				slider.hide()

		if show_profile:
			ui.render_profile()
		pygame_widgets.update(events)
		pygame.display.update()
		fps.tick(60)
		# print(fps.get_fps())

if __name__ == '__main__':
     main()