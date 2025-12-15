import pygame, pygame_widgets
from pygame.locals import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from faker import Faker
import random, datetime
from datetime import date

import numpy as np
import pandas as pd

import sys
import os
import csv
import collections

from .common import *
from .fonts import *

fake = Faker('en_GB')

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def render_note(text, pos, w, h):
    words = [word.split(' ') for word in text.splitlines()]
    space = ui.font.size(' ')[0]
    x, y = pos
    rects = []
    row_rects = []
    for line in words:
        for word in line:
            word_surface = ui.font.render(word, 0, (0, 0, 0))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= w:
                x = pos[0]
                rects.append(row_rects)
                row_rects = []
            row_rects.append(word)
            x += word_width + space
        x = pos[0]
        rects.append(row_rects)
        row_rects = []

    for line in rects:
        for word in line:
            word_surface = ui.font.render(word, 0, (0, 0, 0))
            word_width, word_height = word_surface.get_size()
            ui.canvas.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

class Events:
    def __init__(self):
        self.a = 0

    def event0(self, settings):
        return None

    def event1(self, settings):
        settings.counter = settings.counter//2
        return "Shorter Time"

class UI:
    def __init__(self, canvas):
        self.font = pygame.font.SysFont('Grand9K Pixel',25)
        self.font_small = pygame.font.SysFont('Grand9K Pixel',21)
        self.texts = {}
        self.texts_render = {}
        self.canvas = canvas
        self.width = self.canvas.get_width()
        self.height = self.canvas.get_height()

        self.Buttons = collections.namedtuple('Buttons', 'case_button restart_button auto_button right1_button left1_button right2_button left2_button profile_button')
        self.Images = collections.namedtuple('Images', 'case_button_image restart_image auto_image right1_image left1_image right2_image left2_image profile_image')
        self.buttons()


        self.profile = pygame.Surface((250, 300))
        self.profile.fill((250, 213, 230))
        self.profile_rect = self.profile.get_rect(center=(0.15*self.width, 0.25*self.height))

    def load_image(self, path, w, h):
        path = resource_path(path)
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (w, h))
        return image

    def buttons(self):
        button_color = (243,206,161)
        button_w = 0.15625*self.width
        button_h = 0.1*self.height
        button_x = 0.5*self.width
        button_y = 0.86*self.height

        case_button_image = self.load_image("./assets/button2.png", button_w, button_h)
        case_button = case_button_image.get_rect()
        case_button.center = (button_x,button_y)

        restart_image = self.load_image("./assets/restart2.png", self.width//12.8, self.width//12.8)
        restart_button = restart_image.get_rect()
        restart_button.center = (0.75*self.width, button_y)

        auto_image = self.load_image("./assets/button2.png", button_w, button_h)
        auto_button = auto_image.get_rect()
        auto_button.center = (0.25*self.width, button_y)

        right1_image = self.load_image("./assets/arrow_right.png", self.width//25, self.height//25)
        right1_button = right1_image.get_rect()
        right1_button.center = (0.22*self.width,0.4*self.height)

        left1_image = self.load_image("./assets/arrow_left.png", self.width//25, self.height//25)
        left1_button = left1_image.get_rect()
        left1_button.center = (0.12*self.width,0.4*self.height)


        right2_image = self.load_image("./assets/arrow_right.png", self.width//25, self.height//25)
        right2_button = right2_image.get_rect()
        right2_button.center = (0.22*self.width,0.7*self.height)

        left2_image = self.load_image("./assets/arrow_left.png", self.width//25, self.height//25)
        left2_button = left2_image.get_rect()
        left2_button.center = (0.12*self.width,0.7*self.height)

        profile_image = self.load_image("./assets/6522516.png", self.width//25, self.height//25)
        profile_button = profile_image.get_rect()
        profile_button.center = (0.15*self.width, 0.025*self.height)

        self.buttons = self.Buttons(case_button, restart_button, auto_button, 
                                    right1_button, left1_button, right2_button, left2_button,
                                    profile_button)
        self.images = self.Images(case_button_image, restart_image, auto_image, 
                                  right1_image, left1_image, right2_image, left2_image,
                                  profile_image)


    def render_buttons(self):
        self.canvas.blit(self.images.case_button_image, self.buttons.case_button)
        if settings.new_day:
            self.canvas.blit(text_newday, (0.5*self.width - text_newday_size[0]//2, 0.92*self.height))
        else:
            self.canvas.blit(text_nextcase, (0.5*self.width - text_nextcase_size[0]//2, 0.92*self.height))
        self.canvas.blit(self.images.auto_image, self.buttons.auto_button)
        self.canvas.blit(text_automation, (0.25*self.width - text_automation_size[0]//2, 0.92*self.height))
        self.canvas.blit(self.images.profile_image, self.buttons.profile_button)

    def render_profile(self):
        self.canvas.blit(self.profile, self.profile_rect)
        # self.canvas.blit(self.update_text("Some Info"), (self.width*0.4,self.height*0.025))
        profile_text = "Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile"
        render_note(profile_text, (0.1*ui.width,0.1*ui.height), 0.25*ui.width, 0.15*ui.height)


    def update_text(self, text):
        return self.font.render(text, False, (0, 0, 0))

    def update_stats(self, settings):
        day = 'Day: ' + str(settings.day)
        workers = 'CWs: ' + str(settings.workers)
        time = 'Time Left: ' + str(settings.counter)
        budget = 'Budget: ' + str(int(settings.budget))
        happiness = 'Happiness: ' + str(settings.happiness)
        cases = 'Cases Left: ' + str(settings.case_num[settings.day-1] - settings.current_case)

        self.canvas.blit(self.update_text(day), (self.width*0.4,self.height*0.025))
        self.canvas.blit(self.update_text(cases), (self.width*0.2,self.height*0.025))
        self.canvas.blit(self.update_text(time), (0.3*self.width,self.height*0.025))
        self.canvas.blit(self.update_text(budget), (0.5*self.width,self.height*0.025))
        # self.canvas.blit(self.update_text(workers), (0.875*self.width,self.height*0.1875))
        self.canvas.blit(self.update_text(happiness), (0.6*self.width,self.height*0.025))

    def update_case_box_accepted(self, settings):

        pygame.draw.rect(self.canvas, (0,0,0), width=1,
                         rect=[0.1*self.width,0.2*self.height,0.15*self.width,0.25*self.height],
                         border_radius=int(0.15*self.width/4))
        pygame.draw.rect(self.canvas, (0,0,0), width=1,
                         rect=[0.1*self.width,0.5*self.height,0.15*self.width,0.25*self.height],
                         border_radius=int(0.15*self.width/4))
        self.canvas.blit(self.images.right1_image, self.buttons.right1_button)
        self.canvas.blit(self.images.left1_image, self.buttons.left1_button)

        self.canvas.blit(self.images.right2_image, self.buttons.right2_button)
        self.canvas.blit(self.images.left2_image, self.buttons.left2_button)

        name = self.font.render(settings.cases_preview[settings.preview_case].name, False, (0, 0, 0))
        self.canvas.blit(name, (0.15*self.width, 0.3*self.height))
        status = self.font.render(settings.cases_preview[settings.preview_case].status, False, (0, 0, 0))
        self.canvas.blit(status, (0.15*self.width, 0.35*self.height))

        if len(settings.cases_completed) > 0:
            print(len(settings.cases_completed), settings.comp_case)
            name_comp = self.font.render(settings.cases_completed[settings.comp_case].name, False, (0, 0, 0))
            self.canvas.blit(name_comp, (0.15*self.width, 0.6*self.height))
            status_comp = self.font.render(settings.cases_completed[settings.comp_case].status, False, (0, 0, 0))
            self.canvas.blit(status_comp, (0.15*self.width, 0.65*self.height))

        counter = self.font.render(str(len(settings.cases_preview)), False, (0, 0, 0))
        self.canvas.blit(counter, (0.125*self.width, 0.225*self.height))

        counter_comp = self.font.render(str(len(settings.cases_completed)), False, (0, 0, 0))
        self.canvas.blit(counter_comp, (0.125*self.width, 0.525*self.height))


    def update_other(self, offset):
        news = self.font.render(news1, False, (0, 0, 0))
        self.canvas.blit(news, (offset, 0.075*self.height))
        
        pygame.draw.line(self.canvas, (0,0,0), (0, 0.0625*self.height), (self.width, 0.0625*self.height), width=1)
        pygame.draw.line(self.canvas, (0,0,0), (0, 0.125*self.height), (self.width, 0.125*self.height), width=1)
        # pygame.draw.line(self.canvas, (0,0,0), (0.859375*self.width, 0.125*self.height), (0.859375*self.width, self.height), width=1)

        return news
        
    def game_over(self, game_over):
        text = self.font.render(str(game_over), False, (0, 0, 0))
        self.canvas.blit(text, (0.5*self.width - self.font.size(str(game_over))[0]//2, 0.4*self.height))
        
    def new_day(self, event_text):
        text = self.font.render('New Day', False, (0, 0, 0))
        self.canvas.blit(text, (0.5*self.width - self.font.size('New Day')[0]//2, 0.4*self.height))

        if event_text != None:
            text = self.font.render(event_text, False, (0, 0, 0))
            self.canvas.blit(text, (0.5*self.width - self.font.size(event_text)[0]//2, 0.5*self.height))

ui = UI(canvas)

class Case:
    def __init__(self, wage, jobs, model, custom_id=None):
        self.norm_vals = [np.int64(99), np.int64(92), np.int64(87774), np.float64(2797.0)]
        self.status = 'Pending'
        if custom_id != None:
            print(custom_cases[custom_id]['name'])
            self.name = custom_cases[custom_id]['name']
            self.address = custom_cases[custom_id]['address']
            self.age = custom_cases[custom_id]['age']
            self.occupation = custom_cases[custom_id]['occupation']
            self.code = custom_cases[custom_id]['code']
            self.wage = custom_cases[custom_id]['wage']
            self.welfare_request = custom_cases[custom_id]['welfare_request']
            df_input = pd.DataFrame({'age':[self.age/self.norm_vals[0]], 
                                     'code': [self.code/self.norm_vals[1]], 
                                     'wage': [self.wage/self.norm_vals[2]]})
            self.welfare_suggested = (model.predict(df_input) * self.norm_vals[3])[0]
        else:
            self.name = fake.name()
            self.address = fake.address().replace('\n', ', ')
            self.birthday = fake.date_of_birth(minimum_age=18, maximum_age=99)
            self.age = self.calculate_age(self.birthday)
            self.occupation = random.choice(jobs['job'].values)
            self.code = random.choice(jobs['code'].values)
            self.wage = self.calc_wage(wage)
            df_input = pd.DataFrame({'age':[self.age/self.norm_vals[0]], 
                                     'code': [self.code/self.norm_vals[1]], 
                                     'wage': [self.wage/self.norm_vals[2]]})
            self.welfare_suggested = (model.predict(df_input) * self.norm_vals[3])[0]
            self.welfare_request = int(self.welfare_suggested * random.uniform(2, 5))

    def calc_wage(self, wage):
        wage_job = wage.loc[wage['Code'] == self.code]
        wage_num_min = int(wage_job['10'].values[0].replace(',', ''))
        wage_num_max = int(wage_job['70'].values[0].replace(',', ''))
        
        wage_num = random.choice(range(wage_num_min, wage_num_max))
        return wage_num
        
    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def render_bio(self, text, w, h):
        text = ui.font_small.render(text, False, (0, 0, 0))
        ui.canvas.blit(text, (w,h))

    def viz_case(self):
        self.render_bio('Name: ' + self.name, 0.3*ui.width,0.2*ui.height)
        self.render_bio('Age: ' + str(self.age), 0.3*ui.width,0.3*ui.height)
        self.render_bio('Wage: ' + str(self.wage), 0.3*ui.width,0.4*ui.height)
        self.render_bio('Address: ' + self.address, 0.3*ui.width,0.25*ui.height)
        self.render_bio('Occupation: ' + self.occupation, 0.3*ui.width,0.35*ui.height)
        self.render_bio('Note:', 0.65*ui.width-ui.font.size('Note:')[0]//2,0.22*ui.height)
        self.render_bio('Request: ' + str(self.welfare_request), 0.3*ui.width,0.45*ui.height)

        pygame.draw.line(ui.canvas, (0,0,0), (0.6*ui.width, 0.2*ui.height), 
                                             (0.9*ui.width, 0.2*ui.height), width=1)
        pygame.draw.line(ui.canvas, (0,0,0), (0.6*ui.width, 0.2*ui.height), 
                                             (0.6*ui.width, 0.6*ui.height), width=1)
        pygame.draw.line(ui.canvas, (0,0,0), (0.9*ui.width, 0.2*ui.height), 
                                             (0.9*ui.width, 0.6*ui.height), width=1)
        pygame.draw.line(ui.canvas, (0,0,0), (0.6*ui.width, 0.6*ui.height), 
                                             (0.9*ui.width, 0.6*ui.height), width=1)

        render_note(note1, (0.62*ui.width,0.25*ui.height), 0.88*ui.width, 0.35*ui.height)

class Game:
    def __init__(self):
        self.budget = int(1e5)
        self.case_num = [3, 5, 7, 9, 11]
        self.cases = []
        self.quota = 1.0
        self.happiness = 100

        self.day = 0
        self.time_total = 120
        self.counter = self.time_total
        self.restart_timer = 30

        self.out_of_time = False
        self.case_show = False
        self.new_day = True
        self.new_game = True
        self.show_new_day = False
        self.out = 0
        
        self.funding = 0
        self.current_case = 0

        self.workers = 12

        self.preview_case = 0
        self.comp_case = 0

    def new_day_fill(self, wage, jobs, model):
        self.current_case = 0
        self.cases = []
        self.cases_preview = []
        self.cases_completed = []
        self.comp_case = 0
        self.preview_case = 0
        for i in range(self.case_num[self.day-1]):
            case = Case(wage, jobs, model)
            self.cases += [case]

        if len(custom_cases_info) > 0:
            if custom_cases_info[0][0] == self.day:
                self.cases[custom_cases_info[0][1]] = Case(wage, jobs, model, 0)
                del custom_cases_info[0]

        self.cases_preview = self.cases.copy()

def gameover(budget, happiness, case_num, out_of_time, day, out):
    if budget <= 0:
        return "You run out of budget"
    if happiness <= 0:
        return ":(("
    if case_num[day-1] > 0 and out_of_time:
        return "Too slow"
    if case_num[day-1] <= 0 and day == len(case_num):
        return "You win!"

    return out

settings = Game()

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)

def complete_case(case, settings, auto=False):
    if not auto:
        settings.budget -= settings.funding
    else:
        settings.budget -= case.welfare_request

    if settings.funding < case.welfare_request:
        settings.happiness -= 10
    elif settings.funding == case.welfare_request:
        settings.happiness -= 0
    else:
        settings.happiness += 10

    append_list_as_row('./data/data.csv', [case.age, case.code, case.wage, int(settings.funding)])
    if len(settings.cases_preview) > 1:
        settings.cases_preview.pop(0)
        print(case.name)
    if settings.preview_case != 0:
        settings.preview_case -= 1

    settings.cases_completed.append(case)
    settings.comp_case = len(settings.cases_completed)-1

    case.status = "Given: " + str(settings.funding)

    return settings

def auto(automation, settings, case, ct):
    if automation and settings.new_day == False:
        if settings.case_show == False:
            settings.current_case += 1
            case = settings.cases[settings.current_case]
            settings.case_show = True
        if ct < 60:
            ct += 1
        else:
            ct = 0
            # settings.budget -= case.welfare_request // 2
            # settings.happiness -= 10
            settings = complete_case(case, settings, True)

            if settings.current_case < settings.case_num[settings.day-1]-1:
                settings.current_case += 1
            else:
                            settings.new_day = True
                            settings.show_new_day = True
            case = settings.cases[settings.current_case]
            
    return automation, settings, case, ct

def restart():
    return Game()