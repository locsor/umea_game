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

        self.Buttons = collections.namedtuple('Buttons', 'approve_button case_button auto_button right1_button left1_button right2_button left2_button profile_button')
        self.Images = collections.namedtuple('Images', 'approve_button_image case_button_image auto_image auto_image_alt right1_image left1_image right2_image left2_image profile_image')
        self.buttons()

        self.profile = pygame.Surface((250, 300))
        self.profile.fill((250, 213, 230))
        self.profile_rect = self.profile.get_rect(center=(0.15*self.width, 0.25*self.height))

        self.icon1 = self.load_image("./assets/icon.png", self.width*0.02133333333, 0.04210526316*self.height)
        self.icon2 = self.load_image("./assets/circle.png", self.width*0.03866666667, 0.059563543*self.height)

        self.email_cross_image = self.load_image("./assets/restart2.png", self.width*0.032, 0.04929396662*self.height)
        self.email_cross = self.email_cross_image.get_rect()
        self.email_cross.center = (0.7*self.width, 0.3*self.height)

        self.email_ammend_image = self.load_image("./assets/ammend2.png", self.width*0.1073333333, 0.059563543*self.height)
        self.email_ammend = self.email_ammend_image.get_rect()
        self.email_ammend.center = (0.35*self.width, 0.7*self.height)

        self.deny_button_image = self.load_image("./assets/deny.png", 0.0753968254*self.width, 0.059563543*self.height)
        self.deny_button = self.deny_button_image.get_rect()
        self.deny_button.center = (0.74*self.width - self.deny_button.width,0.9*self.height)

        self.arrow_down_image = self.load_image("./assets/arrow_down.png", self.width//40, self.height//40)
        self.arrow_down = self.arrow_down_image.get_rect()
        self.arrow_down.center = (0.95*self.width,0.9*self.height)

        self.arrow_up_image = self.load_image("./assets/arrow_up.png", self.width//40, self.height//40)
        self.arrow_up = self.arrow_up_image.get_rect()
        self.arrow_up.center = (0.95*self.width,0.85*self.height)

        self.notif_image = self.load_image("./assets/notif.png", self.width//96, self.width//96)

    def load_image(self, path, w, h):
        path = resource_path(path)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (w, h))
        return image

    def buttons(self):
        button_color = (243,206,161)
        button_w = 0.15625*self.width
        button_h = 0.1*self.height
        button_x = 0.175*self.width
        button_y = 0.4*self.height

        approve_button_image = self.load_image("./assets/approve.png", 0.1073333333*self.width, 0.059563543*self.height)
        approve_button = approve_button_image.get_rect()
        approve_button.center = (0.35*self.width + approve_button.width/2,0.9*self.height)

        # restart_image = self.load_image("./assets/restart2.png", self.width//12.8, self.width//12.8)
        # restart_button = restart_image.get_rect()
        # restart_button.center = (0.75*self.width, 0.86*self.height)

        auto_image = self.load_image("./assets/toggle.png", 0.104*self.width, 0.059563543*self.height)
        auto_image_alt = self.load_image("./assets/toggle2.png", 0.104*self.width, 0.059563543*self.height)
        auto_button = auto_image.get_rect()
        auto_button.center = (0.1633597884*self.width + auto_button.width/2, 0.03054989817*self.height + auto_button.height/2)

        case_button_image = self.load_image("./assets/select.png", 0.08666666667*self.width, 0.059563543*self.height)
        case_button = case_button_image.get_rect()
        case_button.center = (0.145*self.width,0.45*self.height)

        right1_image = self.load_image("./assets/arrow_right.png", self.width//25, self.height//25)
        right1_button = right1_image.get_rect()
        right1_button.center = (0.245*self.width - right1_button.width/2,0.45*self.height)

        left1_image = self.load_image("./assets/arrow_left.png", self.width//25, self.height//25)
        left1_button = left1_image.get_rect()
        left1_button.center = (0.045*self.width + left1_button.width/2,0.45*self.height)

        right2_image = self.load_image("./assets/arrow_right.png", self.width//25, self.height//25)
        right2_button = right2_image.get_rect()
        right2_button.center = (0.245*self.width - right1_button.width/2,0.9*self.height)

        left2_image = self.load_image("./assets/arrow_left.png", self.width//25, self.height//25)
        left2_button = left2_image.get_rect()
        left2_button.center = (0.045*self.width + left1_button.width/2,0.9*self.height)

        profile_image = self.load_image("./assets/profile.png", 0.1353333333*self.width, 0.059563543*self.height)
        profile_button = profile_image.get_rect()
        profile_button.center = (0.087*self.width, 0.061*self.height)

        self.buttons = self.Buttons(approve_button, case_button, auto_button, 
                                    right1_button, left1_button, right2_button, left2_button,
                                    profile_button)
        self.images = self.Images(approve_button_image, case_button_image, auto_image, auto_image_alt, 
                                  right1_image, left1_image, right2_image, left2_image,
                                  profile_image)

    def render_icons(self):
        self.canvas.blit(self.icon2, (0.251984127*self.width-self.icon2.width/2, 0.1304928717*self.height))
        self.canvas.blit(self.icon2, (0.251984127*self.width-self.icon2.width/2, 0.575503055*self.height))
        self.canvas.blit(self.icon1, (0.251984127*self.width-self.icon1.width/2, 0.1384928717*self.height))
        self.canvas.blit(self.icon1, (0.251984127*self.width-self.icon1.width/2, 0.583503055*self.height))

    def render_email(self, content, status):
        pygame.draw.rect(ui.canvas, (255,255,255),
                         rect=[0.25*self.width,0.25*self.height,0.5*self.width,0.5*self.height],
                         border_radius=int(0.005*ui.width))
        pygame.draw.rect(ui.canvas, (0,0,0), width=2,
                         rect=[0.25*self.width,0.25*self.height,0.5*self.width,0.5*self.height],
                         border_radius=int(0.005*ui.width))

        text = self.prep_text(content, font_email, (0,0,0))
        self.canvas.blit(text, (0.27*self.width, 0.27*self.height))

        if not status:
            self.canvas.blit(self.email_ammend_image, self.email_ammend)
        self.canvas.blit(self.email_cross_image, self.email_cross)


    def render_buttons(self, settings, automation):
        if settings.out == 0:
            if settings.new_day == False:
                self.canvas.blit(self.images.case_button_image, self.buttons.case_button)
                self.canvas.blit(self.images.approve_button_image, self.buttons.approve_button)
                self.canvas.blit(self.deny_button_image, self.deny_button)
            # if settings.new_day:
                # self.canvas.blit(text_newday, (0.5*self.width - text_newday_size[0]//2, 0.92*self.height))
            # else:
                # self.canvas.blit(text_nextcase, (0.5*self.width - text_nextcase_size[0]//2, 0.92*self.height))
            if not automation:
                self.canvas.blit(self.images.auto_image, self.buttons.auto_button)
            else:
                self.canvas.blit(self.images.auto_image_alt, self.buttons.auto_button)
            # self.canvas.blit(text_automation, (0.25*self.width - text_automation_size[0]//2, 0.92*self.height))
            if len(settings.emails) > 5:
                self.canvas.blit(self.arrow_down_image, self.arrow_down)
                self.canvas.blit(self.arrow_up_image, self.arrow_up)
        self.canvas.blit(self.images.profile_image, self.buttons.profile_button)

    def render_profile(self):
        self.canvas.blit(self.profile, self.profile_rect)
        # self.canvas.blit(self.prep_text("Some Info"), (self.width*0.4,self.height*0.025))
        profile_text = "Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile Profile"
        render_note(profile_text, (0.1*ui.width,0.1*ui.height), 0.25*ui.width, 0.15*ui.height)

    def update_text(self, automation):
        color = (255, 255, 255)
        text = self.prep_text("CASE INFORMATION", font_alt, color)
        self.canvas.blit(text, (0.52*self.width-text.width/2, 0.46*self.height))

        text = self.prep_text("PILE: INBOX", font_alt, color)
        self.canvas.blit(text, (0.145*self.width-text.width/2, 0.125*self.height))

        text = self.prep_text("PILE: FINISHED", font_alt, color)
        self.canvas.blit(text, (0.145*self.width-text.width/2, 0.58*self.height))

        if not automation:
            text = self.prep_text("AI: Off", font_thin, color)
        else:
            text = self.prep_text("AI: On", font_thin, color)
        self.canvas.blit(text, (0.205*self.width, 0.05*self.height))

        text = self.prep_text("Umeå", font_alt_big, color)
        self.canvas.blit(text, (0.825*self.width + text.width/2, 0.044*self.height))

        text = self.prep_text("EMAIL INBOX", font_alt, color)
        self.canvas.blit(text, (0.74*self.width + text.width/2, 0.36*self.height))

    def update_boxes(self):
        pygame.draw.rect(ui.canvas, (255,255,255),
                         rect=[0.35*ui.width,0.55*ui.height,0.35*ui.width,0.3*ui.height],
                         border_radius=int(0.005*ui.width))

        pygame.draw.rect(ui.canvas, (255,255,255),
                         rect=[0.045*ui.width,0.17*ui.height,0.2*ui.width,0.2*ui.height],
                         border_radius=int(0.005*ui.width))

        pygame.draw.rect(ui.canvas, (255,255,255),
                         rect=[0.045*ui.width,0.62*ui.height,0.2*ui.width,0.2*ui.height],
                         border_radius=int(0.005*ui.width))

    def prep_text(self, text, font, color = (0, 0, 0)):
        return font.render(text, False, color)

    def update_stats(self, settings):
        color = (255, 255, 255)

        day = self.prep_text('Day: ' + str(settings.day), font_thin_small, color)
        workers = 'CWs: ' + str(settings.workers)
        time = str(settings.counter // 60) + ':' + str(settings.counter%60)
        if settings.counter % 60 == 0:
             time += '0'
        elif settings.counter % 60 < 10 and settings.counter != 0:
             time_sec = str(settings.counter % 60)
             time = list(time)
             time[-1] = '0'
             time += [time_sec]
             time = "".join(time)

        budget = self.prep_text('Budget: ' + str(int(settings.budget)), font_thin_small, color)
        happiness = self.prep_text('Happiness: ' + str(settings.happiness), font_thin_small, color)
        # cases = 'Cases Left: ' + str(settings.case_num[settings.day-1] - settings.current_case)

        time = font_timer.render(time, False, (255, 255, 255))

        self.canvas.blit(day, (self.width*0.3664021164, self.height*0.04175152749 - day.height/2))
        self.canvas.blit(happiness, (0.5691137566*self.width, self.height*0.04175152749 - happiness.height/2))
        # self.canvas.blit(self.prep_text(cases, self.font), (self.width*0.2,self.height*0.025))
        self.canvas.blit(time, (0.5*self.width - time.get_size()[0]/2,self.height*0.069 - time.get_size()[1]/2))
        self.canvas.blit(budget, (self.width*0.337, self.height*0.08 + day.height/2))
        # self.canvas.blit(self.update_text(workers), (0.875*self.width,self.height*0.1875))

    def update_case_box_accepted(self, settings):
        self.canvas.blit(self.images.right1_image, self.buttons.right1_button)
        self.canvas.blit(self.images.left1_image, self.buttons.left1_button)

        self.canvas.blit(self.images.right2_image, self.buttons.right2_button)
        self.canvas.blit(self.images.left2_image, self.buttons.left2_button)

        if len(settings.cases_preview) > 0:
            name = self.font.render(settings.cases_preview[settings.preview_case].name, False, (0, 0, 0))
            self.canvas.blit(name, (0.06*self.width, 0.225*self.height))
            status = self.font.render(settings.cases_preview[settings.preview_case].status, False, (0, 0, 0))
            self.canvas.blit(status, (0.06*self.width, 0.25*self.height))

        if len(settings.cases_completed) > 0:
            name_comp = self.font.render(settings.cases_completed[settings.comp_case].name, False, (0, 0, 0))
            self.canvas.blit(name_comp, (0.06*self.width, 0.675*self.height))
            status_comp = self.font.render(settings.cases_completed[settings.comp_case].status, False, (0, 0, 0))
            self.canvas.blit(status_comp, (0.06*self.width, 0.725*self.height))

        counter = self.font.render(str(len(settings.cases_preview)), False, (0, 0, 0))
        self.canvas.blit(counter, (0.251984127*self.width-counter.width/2, 0.1354928717*self.height+counter.height/2))

        counter_comp = self.font.render(str(len(settings.cases_completed)), False, (0, 0, 0))
        self.canvas.blit(counter_comp, (0.251984127*self.width-counter_comp.width/2, 0.580503055*self.height+counter.height/2))

    def update_email(self, settings, start=0):
        color = (255, 255, 255)

        emails = settings.emails[::-1]
        emails = emails[start:]

        settings.emails_show = emails.copy()

        for i, email in enumerate(emails[:5]):
            text = self.prep_text(email[0], font_email, color)
            self.canvas.blit(text, (0.80*self.width, (0.4+0.1*i)*self.height))

            text = self.prep_text(email[1], font_email, color)
            self.canvas.blit(text, (0.7817460317*self.width, (0.43+0.1*i)*self.height))

            text = self.prep_text(email[2], font_email, color)
            self.canvas.blit(text, (0.7817460317*self.width, (0.46+0.1*i)*self.height))

            if not email[5]:
                self.canvas.blit(self.notif_image, (0.785*self.width, (0.397+0.1*i)*self.height))

    def update_other(self, offset):
        news = self.font.render(news1, False, (0, 0, 0))
        self.canvas.blit(news, (offset, 0.075*self.height))
        
        pygame.draw.line(self.canvas, (0,0,0), (0, 0.0625*self.height), (self.width, 0.0625*self.height), width=1)
        pygame.draw.line(self.canvas, (0,0,0), (0, 0.125*self.height), (self.width, 0.125*self.height), width=1)
        # pygame.draw.line(self.canvas, (0,0,0), (0.859375*self.width, 0.125*self.height), (0.859375*self.width, self.height), width=1)

        return news
        
    def render_game_over(self, game_over):
        text = font_alt.render(str(game_over), False, (255, 255, 255))
        self.canvas.blit(text, (0.5*self.width - text.width//2, 0.4*self.height))

        # text = font_alt.render('Press Anywhere to Start Again...', False, (255, 255, 255))
        # self.canvas.blit(text, (0.5*self.width - self.font.size(str(game_over))[0]//2, 0.5*self.height))
        
    def new_day(self, event_text):
        text = font_alt.render('New Day', False, (255, 255, 255))
        self.canvas.blit(text, (0.5*self.width - text.width//2, 0.3*self.height))

        text = font_alt.render('Press Anywhere To Start The Next Day...', False, (255, 255, 255))
        self.canvas.blit(text, (0.5*self.width - text.width//2, 0.35*self.height))

        if event_text != None:
            text = self.font.render(event_text, False, (0, 0, 0))
            self.canvas.blit(text, (0.5*self.width - self.font.size(event_text)[0]//2, 0.5*self.height))

ui = UI(canvas)

class Case:
    def __init__(self, wage, jobs, model, custom_id=None):
        self.norm_vals = [np.int64(99), np.int64(92), np.int64(87774), np.float64(2797.0)]
        self.status = 'Pending'
        if custom_id != None:
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

        if self.welfare_suggested <= 0:
            self.welfare_suggested = 135

        self.email_a = ['Subject_a', "Wawawawa"]
        self.email_b = ['Subject_b', "Bababababa"]

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
        case_line = 0.37 * ui.width
        self.render_bio('Name: ' + self.name, case_line,                    0.6*ui.height)
        # self.render_bio('Note:', 0.65*ui.width-ui.font.size('Note:')[0]//2, 0.62*ui.height)
        self.render_bio('Address: ' + self.address, case_line,              0.64*ui.height)
        self.render_bio('Age: ' + str(self.age), case_line,                 0.66*ui.height)
        self.render_bio('Occupation: ' + self.occupation, case_line,        0.68*ui.height)
        self.render_bio('Wage: ' + str(self.wage), case_line,               0.70*ui.height)
        self.render_bio('Request: ' + str(self.welfare_request), case_line, 0.72*ui.height)

        # pygame.draw.line(ui.canvas, (0,0,0), (0.6*ui.width, 0.2*ui.height), 
        #                                      (0.9*ui.width, 0.2*ui.height), width=1)
        # pygame.draw.line(ui.canvas, (0,0,0), (0.6*ui.width, 0.2*ui.height), 
        #                                      (0.6*ui.width, 0.6*ui.height), width=1)
        # pygame.draw.line(ui.canvas, (0,0,0), (0.9*ui.width, 0.2*ui.height), 
        #                                      (0.9*ui.width, 0.6*ui.height), width=1)
        # pygame.draw.line(ui.canvas, (0,0,0), (0.6*ui.width, 0.6*ui.height), 
        #                                      (0.9*ui.width, 0.6*ui.height), width=1)

        # render_note(note1, (0.62*ui.width,0.25*ui.height), 0.88*ui.width, 0.35*ui.height)

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
        self.restart_timer = 3

        self.out_of_time = False
        self.case_show = False
        self.new_day = True
        self.new_game = True
        self.show_new_day = False
        self.fail = False
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
        self.emails = []
        self.emails_show = []
        self.email_lead = 0
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
    def change_happiness(self, amount):
        if amount > 0 and self.happiness + 10 >= 100:
            self.happiness = 100
        elif amount > 0 and self.happiness + 10 < 100:
            self.happiness += 10
        elif amount < 0 and self.happiness -10 <= 0:
            self.happiness = 0
        elif amount < 0 and self.happiness - 10 > 0:
            self.happiness -= 10

def gameover(budget, happiness, case_num, out_of_time, day, out):
    if budget <= 0:
        return "You run out of budget"
        # return 'Press Anywhere to Start Again...'
    if happiness <= 0:
        return ":(("
        # return 'Press Anywhere to Start Again...'
    if case_num[day-1] > 0 and out_of_time:
        return "Too slow"
        # return 'Press Anywhere to Start Again...'
    if case_num[day-1] <= 0 and day == len(case_num):
        return "You win!"
        # return 'Press Anywhere to Start Again...'

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
        # settings.happiness -= 10
        settings.change_happiness(-10)
        email = [case.name] + case.email_a
    elif settings.funding == case.welfare_request:
        # settings.happiness -= 0
        settings.change_happiness(0)
        email = [case.name] + case.email_b
    else:
        # settings.happiness += 10
        settings.change_happiness(10)
        email = [case.name] + case.email_b

    email += [False]

    append_list_as_row('./data/data.csv', [case.age, case.code, case.wage, int(settings.funding)])
    # if len(settings.cases_preview) > 1:
    settings.cases_preview.remove(case)

    if settings.preview_case != 0:
        settings.preview_case -= 1

    settings.cases_completed.append(case)
    settings.comp_case = len(settings.cases_completed)-1
    email += [settings.comp_case]

    case.status = "Given: " + str(int(settings.funding))

    settings.emails += [email]

    viewed = False
    email += [viewed]

    return settings

def auto(automation, settings, case, ct):
    if automation and settings.new_day == False:
        if case == None:
            case = settings.cases_preview[0]
        # if settings.case_show == False:
            # settings.current_case += 1
            # case = settings.cases[settings.current_case]
        settings.case_show = True
        if ct < 60:
            ct += 1
        else:
            ct = 0
            if len(settings.cases_preview)==0:
                settings.new_day = True
                settings.show_new_day = True
            else:
                print(len(settings.cases_preview), case.name)
                # settings.budget -= case.welfare_request // 2
                # settings.happiness -= 10
                case = settings.cases_preview[0]
                settings = complete_case(case, settings, True)

                # if settings.current_case < settings.case_num[settings.day-1]-1:
                    # settings.current_case += 1
            
    return automation, settings, case, ct

def restart():
    return Game()