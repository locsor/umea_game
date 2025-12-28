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
	show_email = False
	restart_timer = 3
	ct = 0
	news_offset = 0
	event_sys = Events()

	model = train_model()

	pygame.time.set_timer(pygame.USEREVENT, 1000)

	slider = Slider(canvas, 0.34375*ui.width, 0.75*ui.height, 0.3125*ui.width, 0.042*ui.height,
					min=0, max=10, step=0.01, curved=True, initial=50)
	slider.hide()

	case = None

	background_start = pygame.image.load("./assets/background5.png").convert_alpha()
	background_start = pygame.transform.scale(background_start, (ui.width, ui.height))

	background_alt = pygame.image.load("./assets/background4.png").convert_alpha()
	background_alt = pygame.transform.scale(background_alt, (ui.width, ui.height))

	background = background_start

	while True:
		mouse = pygame.mouse.get_pos()
		events = pygame.event.get()

		canvas.blit(background, (0, 0))

		for event in events:
			if event.type == QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				email_coll = mouse[0] > 0.7757936508*ui.width and mouse[0] < 0.94*ui.width and mouse[1] > 0.38*ui.height and mouse[1] < 0.9*ui.height
				
				if settings.new_game == True:
					settings = Game()
					settings.new_day_fill(wage, jobs, model)

				if settings.new_day == True and not ui.buttons.right2_button.collidepoint((mouse[0], mouse[1])) and not ui.buttons.left2_button.collidepoint((mouse[0], mouse[1])) and not email_coll and not show_email:
					background = background_alt
					
					settings.day += 1
					settings.new_day_fill(wage, jobs, model)

					settings.new_day = False
					settings.case_show = True
					settings.new_game = False
					settings.show_new_day = False
					# settings.fail = False
					settings.out = 0
					event_flag = True

					settings.counter = settings.time_total
					case = settings.cases_preview[0]
					ratio = 10*(case.welfare_suggested/1000)
					slider = Slider(canvas, int(0.42*ui.width), int(0.8*ui.height),
									int(0.2*ui.width), int(0.025*ui.height),
									min=0, max=10, step=0.01, curved=True, initial=ratio)

					text_fund = ui.prep_text(str(settings.funding), font_alt_big, (0,0,0))
					ui.canvas.blit(text_fund, (0.5*ui.width, 0.8*ui.height))

				if len(settings.emails_show) > 0:
					if email_coll:
						mouse_y = mouse[1]
						email_i_ = int(((mouse_y/ui.height) - 0.4)*10)
						# email_i_ = -1 * email_i - 1
						if email_i_ < len(settings.emails_show):
							show_email = True
							settings.emails[len(settings.emails) - email_i_ - settings.email_lead - 1][5] = True

					
				#Start Automation
				if ui.buttons.auto_button.collidepoint((mouse[0], mouse[1])):
					automation = not automation
				
				#Select Case
				if ui.buttons.case_button.collidepoint((mouse[0], mouse[1])) and type(settings.out) == int and automation == False:
					# if settings.case_show: #if the case view is already opened
					if len(settings.cases_preview) > 0:
						case = settings.cases_preview[settings.preview_case]
						ratio = 10*(case.welfare_suggested/1000)
						slider = Slider(canvas, int(0.42*ui.width), int(0.8*ui.height),
										int(0.2*ui.width), int(0.025*ui.height),
										min=0, max=10, step=0.01, curved=True, initial=ratio)

						text_fund = ui.prep_text(str(settings.funding), font_alt_big, (0,0,0))
						ui.canvas.blit(text_fund, (0.5*ui.width, 0.8*ui.height))


				if ui.buttons.approve_button.collidepoint((mouse[0], mouse[1])) and case != None:
					settings = complete_case(case, settings, False)
					settings.case_show = True
					if len(settings.cases_preview) == 0:
						case = None
						settings.new_day = True
						settings.show_new_day = True
					else:
						case = settings.cases_preview[0]
						settings.preview_case = 0

						ratio = 10*(case.welfare_suggested/1000)
						slider = Slider(canvas, int(0.42*ui.width), int(0.8*ui.height),
										int(0.2*ui.width), int(0.025*ui.height),
										min=0, max=10, step=0.01, curved=True, initial=ratio)

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

				if ui.arrow_down.collidepoint((mouse[0], mouse[1])) and len(settings.emails_show) > 2:
					settings.email_lead += 1
				if ui.arrow_up.collidepoint((mouse[0], mouse[1])) and settings.email_lead > 0:
					settings.email_lead -= 1

				if ui.buttons.profile_button.collidepoint((mouse[0], mouse[1])):
					show_profile = not show_profile

				if ui.email_cross.collidepoint((mouse[0], mouse[1])):
					show_email = False
				if len(settings.emails_show) > 0:
					if ui.email_ammend.collidepoint((mouse[0], mouse[1])) and not settings.emails_show[email_i_][3]:
						# settings.happiness += 10
						settings.change_happiness(10)
						settings.emails_show[email_i_][3] = True
						settings.cases_completed[settings.emails_show[email_i_][4]].status = "Given: " + str(settings.cases_completed[settings.emails_show[email_i_][4]].welfare_request)
					
					
			if event.type == pygame.USEREVENT:
				if not settings.out_of_time and type(settings.out) == int and not settings.new_game and not settings.show_new_day:
					settings.counter -= 1
					
				if settings.counter <= 0:
					settings.out_of_time = True

				if type(settings.out) != int:
					restart_timer -=1
					if restart_timer <= 0:
						restart_timer = 3
						automation = False
						# settings.new_game = True
						settings = Game()

		automation, settings, case, ct = auto(automation, settings, case, ct) #Automation logic

		if settings.show_new_day:
			automation = False
			if settings.day == 2 and event_flag:
				event_flag = False
				event_text = event_sys.event1(settings)
			elif settings.day !=2 and event_flag:
				event_flag = False
				event_text = event_sys.event0(settings)
			ui.new_day(event_text)
			slider.hide()

		settings.out = gameover(settings.budget, settings.happiness, settings.case_num, 
						    settings.out_of_time, settings.day, settings.out) #Gameover logic
		# if type(settings.out) != int:
			# settings.fail = True

		# news = ui.update_other(news_offset)
		# w_news = news.get_size()[0]
		# news_offset += int(0.003125*ui.width)
		# if news_offset > ui.width:
		# 	news_offset = -w_news

		if type(settings.out) != int or settings.new_game:
			settings.new_game = True
			automation = False
			if type(settings.out) == int:
				ui.render_game_over('Press Anywhere to Start...')
				background = background_start
			if type(settings.out) != int:
				# out_mem = settings.out
				ui.render_game_over(settings.out)
				slider.hide()
				# settings = Game()
				# settings.out = out_mem
				# settings.fail = True
				background = background_start
		else:
			ui.update_stats(settings)
			ui.render_buttons(settings, automation)
			ui.update_text(automation)
			ui.update_boxes()
			ui.render_icons()
			ui.update_email(settings, settings.email_lead)
			if settings.case_show:
				ui.update_case_box_accepted(settings)
				if case != None:
					case.viz_case()
					slider.show()
					# slider.hide()

					ratio = 10*(case.welfare_suggested/1000)
					settings.funding = int(slider.getValue()*(case.welfare_suggested/ratio))
					
					text_fund = ui.prep_text(str(settings.funding), font_alt, (0,0,0))
					ui.canvas.blit(text_fund, (0.5*ui.width, 0.75*ui.height))

					# slider = Slider(canvas, int(0.42*ui.width), int(0.8*ui.height),
					# 					int(0.2*ui.width), int(0.025*ui.height),
					# 					min=0, max=100, step=1, curved=True, initial=int(ratio))
			else:
				slider.hide()
			if show_email:
				ui.render_email(settings.emails_show[email_i_][0], settings.emails_show[email_i_][3])

		if show_profile:
			ui.render_profile()
		pygame_widgets.update(events)
		pygame.display.update()
		fps.tick(240)
		# print(fps.get_fps())

if __name__ == '__main__':
     main()