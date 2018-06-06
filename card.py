import time
import pygame
from pygame.locals import *

from card_utils import redraw

HOLDER1 = 'cardholder1'
HOLDER2 = 'cardholder2'


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
        self.can_open = True
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
        mouse_pos = pygame.mouse.get_pos()
        inside = self.rect.collidepoint(mouse_pos)
        if inside:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen == False and self.can_open == True:
                # WHEN THE USER SELECTS A CARD FROM THE TOP
                previous_time = time.time()
                if game_dict['cardholders_full'] == 0:
                    self.chosen = True
                    self.chose_number(0)
                    cards[HOLDER1].chosen = True  # Card in first cardholder
                    game_dict['cardholders_full'] += 1
                    game_dict['current_sum'] += self.number
                    # --- SELECT FIRST CARD --- #
                    self.gamerunner.send_event('athena.games.sums.card_selected', 'sums_game', self.number)
                elif game_dict['cardholders_full'] == 1 and cards[HOLDER1].chosen:
                    self.chosen = True
                    self.chose_number(1)
                    cards[HOLDER2].chosen = True  # Card in second cardholder
                    game_dict['cardholders_full'] += 1
                    game_dict['current_sum'] += self.number
                    self.gamerunner.send_event('athena.games.sums.card_selected', 'sums_game', self.number)
                elif game_dict['cardholders_full'] == 1 and cards[HOLDER2].chosen:
                    self.chosen = True
                    self.chose_number(0)
                    cards[HOLDER1].chosen = True  # Card in first cardholder
                    game_dict['cardholders_full'] += 1
                    game_dict['current_sum'] += self.number
                    self.gamerunner.send_event('athena.games.sums.card_selected', 'sums_game', self.number)
                else:
                    print('Cardholders full!')
                if game_dict['cardholders_full'] == 2:  # Calculate sum and evaluate
                    if game_dict['current_sum'] == 4:
                        cards['correctwrong_box'].color = (0, 200, 0)
                        cards['correct'].toggle_hidden()
                        self.gamerunner.send_event('athena.games.sums.sumcorrect', 'sums_game')
                        print('Correct!')
                    else:
                        cards['correctwrong_box'].color = (200, 0, 0)
                        cards['wrong'].toggle_hidden()
                        self.gamerunner.send_event('athena.games.sums.sumwrong', 'sums_game')
                        print('Wrong!')
                redraw(cards, screen)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen == True and self.can_open == True:
                previous_time = time.time()
                if game_dict['cardholders_full'] > 0:
                    self.chosen = False
                    i = self.reset_number()
                    if i == 0:
                        cards[HOLDER1].chosen = False  # Card removed from first cardholder
                    else:
                        cards[HOLDER2].chosen = False  # Card removed from second cardholder
                    game_dict['cardholders_full'] -= 1
                    game_dict['current_sum'] -= self.number
                    cards['correctwrong_box'].color = (0, 0, 0)
                    cards['correct'].hide_if_active()
                    cards['wrong'].hide_if_active()
                    redraw(cards, screen)
                else:
                    print('All cardholders empty!')
