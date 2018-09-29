import time
import pygame
from pygame.locals import *

from card_utils import redraw, activate_numbers, deactivate_numbers
from events import ENABLECARDS, DISABLECARDS, ROBOTWRONGSUMSELECT, ROBOTSUMMAKE, ROBOTCORRECTSUMSELECT, CHILDRETRY, RESETCARDHOLDER
from sums_game_utils import select_number, deselect_number, robot_make_wrong_sum, open_only_first_cardholder, \
    robot_make_correct_sum, robot_make_first_choice, select_number_once, robot_put_number, robot_put_correct_number

HOLDER1 = 'cardholder1'
HOLDER2 = 'cardholder2'

class Card(object):
    def __init__(self, number, picture, cardback, position, cardsize, gamerunner, cardholder=False,
                 color=(200, 200, 200), bord_size=3):
        self.number = number
        self.picture = picture
        self.cardback = cardback
        self.position = position
        self.cardsize = cardsize
        self.gamerunner = gamerunner
        self.chosen = False
        self.chosen_once = False
        self.can_open = False  # Start deactivated
        self.cardholder = cardholder
        self.color = color

        self.back = pygame.image.load(self.cardback)
        self.back = pygame.transform.scale(self.back, (self.cardsize[0], self.cardsize[1]))
        self.img = pygame.image.load(self.picture)
        self.img = pygame.transform.scale(self.img, (self.cardsize[0], self.cardsize[1]))
        self.cardholder_positions = ((0, 0), (0, 0))
        self.in_cardholder = 0
        self.bord_size = bord_size

        self.current_position = self.position

    def draw(self, screen):
        if self.cardholder:
            pygame.draw.rect(screen, self.color, Rect([self.position[0], self.position[1]], self.cardsize), self.bord_size)
            pygame.display.flip()
            self.rect = Rect(self.current_position[0], self.current_position[1], self.cardsize[0], self.cardsize[1])
            self.screen = screen
        else:
            screen.blit(self.img, self.current_position)
            pygame.display.flip()
            # print(self.position)
            self.rect = Rect(self.current_position[0], self.current_position[1], self.cardsize[0], self.cardsize[1])
            self.screen = screen

    def chose_number(self, i):
        self.current_position = self.cardholder_positions[i]
        self.in_cardholder = i

    def reset_number(self):
        self.current_position = self.position
        i = self.in_cardholder
        self.in_cardholder = 0
        return i

    def clear(self):
        img = pygame.image.load('sums_game_data/green.png')
        self.screen.blit(img, self.position)
        pygame.display.flip()

    def toggle(self):
        tmp = self.back
        self.back = self.img
        self.img = tmp

    def toggle_hidden(self):
        self.toggle()
        self.chosen = not self.chosen

    def hide_if_active(self):
        if self.chosen:
            self.toggle_hidden()

    def process_event(self, event, cards, screen, game_dict):
        global previous_time

        # --------------- EVENTS FOR ACTIVATING DEACTIVATING CARDS ---------#
        if event.type == ENABLECARDS:
            activate_numbers(cards=cards)
        elif event.type == DISABLECARDS:
            deactivate_numbers(cards=cards)

        # -------- EVENTS FOR ROBOT SUM WRONG ---------- #
        elif event.type == ROBOTWRONGSUMSELECT:
            open_only_first_cardholder(card=self, cards=cards, game_dict=game_dict, screen=screen)
            robot_make_wrong_sum(card=self, cards=cards, game_dict=game_dict, screen=screen)
        elif event.type == ROBOTSUMMAKE:
            robot_put_number(card=self, cards=cards, game_dict=game_dict, screen=screen)

        # -------- EVENTS FOR ROBOT SUM CORRECT ---------- #
        elif event.type == ROBOTCORRECTSUMSELECT:
            open_only_first_cardholder(card=self, cards=cards, game_dict=game_dict, screen=screen)
            robot_make_correct_sum(card=self, cards=cards, game_dict=game_dict, screen=screen)

        # -------- EVENTS FOR REPLAY ---------- #
        elif event.type == CHILDRETRY:
            open_only_first_cardholder(card=self, cards=cards, game_dict=game_dict, screen=screen)
        
        # -------- GENERAL EVENTS ---------- #
        elif event.type == RESETCARDHOLDER:
            open_only_first_cardholder(card=self, cards=cards, game_dict=game_dict, screen=screen)

        # ----------------- EVENTS FOR SELECTING CARDS -------------- #
        mouse_pos = pygame.mouse.get_pos()
        inside = self.rect.collidepoint(mouse_pos)
        if inside:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen_once and self.chosen == False and self.can_open:
                previous_time = time.time()
                select_number(card=self, cards=cards, game_dict=game_dict, screen=screen)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen and self.can_open:
                # WHEN THE USER SELECTS A CARD FROM THE BOTTOM
                previous_time = time.time()
                deselect_number(card=self, cards=cards, game_dict=game_dict, screen=screen)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen_once == False and self.can_open and not self.chosen and game_dict['cardholders_full'] < 2:
                previous_time = time.time()
                select_number_once(card=self, cards=cards, game_dict=game_dict, screen=screen)

    def process_event_wizard(self, event, cards, screen, game_dict):
        global previous_time
        mouse_pos = pygame.mouse.get_pos()
        inside = self.rect.collidepoint(mouse_pos)
        if inside:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen_once and self.chosen == False and self.can_open:
                # cards[-1].clear()
                # WHEN THE USER SELECTS A CARD FROM THE TOP
                previous_time = time.time()
                if game_dict['cardholders_full'] == 0:
                    self.chosen = True
                    self.chose_number(0)
                    cards[HOLDER1].chosen = True  # Card in first cardholder
                    game_dict['cardholders_full'] += 1
                    game_dict['current_sum'] += self.number
                    # self.gamerunner.send_event('athena.games.emorec.card_opened', 'emorec_game', self.number)
                elif game_dict['cardholders_full'] == 1 and cards[HOLDER1].chosen:
                    self.chosen = True
                    self.chose_number(1)
                    cards[HOLDER2].chosen = True  # Card in second cardholder
                    game_dict['cardholders_full'] += 1
                    game_dict['current_sum'] += self.number
                elif game_dict['cardholders_full'] == 1 and cards[HOLDER2].chosen:
                    self.chosen = True
                    self.chose_number(0)
                    cards[HOLDER1].chosen = True  # Card in first cardholder
                    game_dict['cardholders_full'] += 1
                    game_dict['current_sum'] += self.number
                else:
                    print('Cardholders full!')
                if game_dict['cardholders_full'] == 2:  # Calculate sum and evaluate
                    if game_dict['current_sum'] == 4:
                        cards['correctwrong_box'].color = (0, 200, 0)
                        cards['correct'].toggle_hidden()
                        print('Correct!')
                    else:
                        cards['correctwrong_box'].color = (200, 0, 0)
                        cards['wrong'].toggle_hidden()
                        print('Wrong!')
                redraw(cards, screen)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen and self.can_open:
                previous_time = time.time()
                if game_dict['cardholders_full'] > 0:
                    self.chosen = False
                    self.chosen_once = False
                    i = self.reset_number()
                    if i == 0:
                        cards[HOLDER1].chosen = False  # Card removed from first cardholder
                    else:
                        cards[HOLDER2].chosen = False  # Card removed from second cardholder
                    game_dict['cardholders_full'] -= 1
                    game_dict['current_sum'] -= self.number
                    cards['correctwrong_box'].color = (81, 193, 206)
                    cards['correct'].hide_if_active()
                    cards['wrong'].hide_if_active()
                    redraw(cards, screen)
                else:
                    print('All cardholders empty!')
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen_once == False and self.can_open and not self.chosen and game_dict['cardholders_full'] < 2:
                flag = False
                for key in [0, 1, 2, 3, 4]:
                    if cards[key].chosen_once:
                        cards[key].chosen_once = False
                        flag = True
                        self.chosen_once = True
                        redraw(cards, screen)
                        game_dict['cardholderc'].position = (self.position[0]-5, self.position[1]-5)
                        game_dict['cardholderc'].draw(screen)
                if not flag:
                    self.chosen_once = True
                    game_dict['cardholderc'].position = (self.position[0]-5, self.position[1]-5)
                    game_dict['cardholderc'].draw(screen)
