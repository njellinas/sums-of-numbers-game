import time
import pygame
from pygame.locals import *

from card_utils import redraw, activate_numbers, deactivate_numbers
from run_all_games import ENABLECARDS, DISABLECARDS, ROBOTWRONGSUM, CHILDSHOWCORRECT, ROBOTCORRECTSUM, TOGETHERSUM, \
    CHILDRETRY
from sums_game_utils import select_number, deselect_number, robot_make_wrong_sum, open_only_second_cardholder, \
    robot_make_correct_sum, robot_make_first_choice


class Card(object):
    def __init__(self, number, picture, cardback, position, cardsize, gamerunner, cardholder=False,
                 color=(200, 200, 200)):
        self.number = number
        self.picture = picture
        self.cardback = cardback
        self.position = position
        self.cardsize = cardsize
        self.gamerunner = gamerunner
        self.chosen = False
        self.can_open = False  # Start deactivated
        self.cardholder = cardholder
        self.color = color

        self.back = pygame.image.load(self.cardback)
        self.back = pygame.transform.scale(self.back, (self.cardsize[0], self.cardsize[1]))
        self.img = pygame.image.load(self.picture)
        self.img = pygame.transform.scale(self.img, (self.cardsize[0], self.cardsize[1]))
        self.cardholder_positions = ((0, 0), (0, 0))
        self.in_cardholder = 0

        self.current_position = self.position

    def draw(self, screen):
        if self.cardholder:
            pygame.draw.rect(screen, self.color, Rect([self.position[0], self.position[1]], self.cardsize), 3)
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
        img = pygame.image.load('emotion_recognition_game_data/black.jpg')
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
        elif event.type == ROBOTWRONGSUM:
            robot_make_wrong_sum(cards=cards, game_dict=game_dict, screen=screen)
        elif event.type == CHILDSHOWCORRECT:
            open_only_second_cardholder(cards=cards, game_dict=game_dict, screen=screen)

        # -------- EVENTS FOR ROBOT SUM CORRECT ---------- #
        elif event.type == ROBOTCORRECTSUM:
            robot_make_correct_sum(cards=cards, game_dict=game_dict, screen=screen)

        # -------- EVENTS FOR ROBOT SUM CORRECT ---------- #
        elif event.type == TOGETHERSUM:
            robot_make_first_choice(cards=cards, game_dict=game_dict, screen=screen)
        elif event.type == CHILDRETRY:
            open_only_second_cardholder(cards=cards, game_dict=game_dict, screen=screen)

        # ----------------- EVENTS FOR SELECTING CARDS -------------- #
        mouse_pos = pygame.mouse.get_pos()
        inside = self.rect.collidepoint(mouse_pos)
        if inside:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not self.chosen and self.can_open:
                # WHEN THE USER SELECTS A CARD FROM THE TOP
                previous_time = time.time()
                select_number(card=self, cards=cards, game_dict=game_dict, screen=screen)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen and self.can_open:
                # WHEN THE USER SELECTS A CARD FROM THE BOTTOM
                previous_time = time.time()
                deselect_number(card=self, cards=cards, game_dict=game_dict, screen=screen)
