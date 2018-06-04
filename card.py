import time
import pygame
from pygame.locals import *

from card_utils import deactivate


class Card(object):
    def __init__(self, emotion, picture, cardback, position, cardsize, gamerunner):
        self.emotion = emotion
        self.picture = picture
        self.cardback = cardback
        self.position = position
        self.cardsize = cardsize
        self.gamerunner = gamerunner
        self.chosen = False
        self.can_open = True

    def draw(self, screen):
        if self.chosen:
            return
        img = pygame.image.load(self.cardback)
        img = pygame.transform.scale(img, (self.cardsize[0], self.cardsize[1]))
        screen.blit(img, self.position)
        pygame.display.flip()
        print(self.position)
        self.rect = Rect(self.position[0], self.position[1], self.cardsize[0], self.cardsize[1])
        self.screen = screen

    def load_emotion_image(self):
        img = pygame.image.load(self.picture)
        self.screen.blit(img, self.position)
        pygame.display.flip()

    def clear(self):
        img = pygame.image.load('emotion_recognition_game_data/black.jpg')
        self.screen.blit(img, self.position)
        pygame.display.flip()

    def process_event(self, event, cards, screen):
        global previous_time
        mouse_pos = pygame.mouse.get_pos()
        inside = self.rect.collidepoint(mouse_pos)
        if inside:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.chosen == False and self.can_open == True:
                self.chosen = True
                previous_time = time.time()
                self.load_emotion_image()
                self.gamerunner.send_event('athena.games.emorec.card_opened', 'emorec_game', self.emotion)
                # time.sleep(5)
                deactivate(cards, screen)


class CardHolder(object):
    def __init__(self, position, cardsize):
        self.position = position
        self.cardsize = cardsize

    def draw(self, screen):
        pygame.draw.rect(screen, [200, 200, 200], Rect([0, 0], self.cardsize), 3)
