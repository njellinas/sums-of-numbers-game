#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
import time

STOP_EMOREC = USEREVENT + 2
global previous_time

def redraw(cards, screen):
    screen.fill((0,0,0))
    for card in cards:
        card.draw(screen)

def deactivate(cards, screen):
    for card in cards:
        card.can_open = False

def activate(cards, screen):
    for card in cards:
        card.can_open = True

class Card:
    def __init__(self, emotion, picture, cardback, position, gamerunner):
        self.emotion = emotion
        self.picture = picture
        self.cardback = cardback
        self.position = position
        self.gamerunner = gamerunner
        self.chosen = False
        self.can_open = True

    def draw(self, screen):
        if self.chosen: 
            return
        img = pygame.image.load(self.cardback)
        screen.blit(img, self.position)
        pygame.display.flip()
        self.rect = Rect(self.position[0], self.position[1], img.get_width(), img.get_height())
        self.screen = screen

    def load_emotion_image(self):
        img = pygame.image.load(self.picture)
        self.screen.blit(img, self.position)
        pygame.display.flip()
        
    def clear(self):
        img = pygame.image.load('emotion_recognition_game_data/black.jpg');
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
                deactivate(cards,screen)





def start_sums_game(screen, gamerunner):
    global previous_time
#    pygame.init()
    screen.fill((0,0,0))
 #   screen = create_screen()
    pygame.display.set_caption('Emotion Recognition')

    previous_time = -200

    cardback = "emotion_recognition_game_data/question.jpg"

    w, h = pygame.display.get_surface().get_size()

    cards = []

    card = Card("happiness", "emotion_recognition_game_data/inside-out-happiness.jpg", cardback, (150,50), gamerunner)
    card.draw(screen)

    cards.append(card)

    card = Card("fear", "emotion_recognition_game_data/inside-out-fear.jpg", cardback, (750,50), gamerunner)
    card.draw(screen)

    cards.append(card)

    card = Card("disgust", "emotion_recognition_game_data/inside-out-disgust.jpg", cardback, (1350,50), gamerunner)
    card.draw(screen)

    cards.append(card)

    card = Card("anger", "emotion_recognition_game_data/inside-out-anger.jpg", cardback, (150,550), gamerunner)
    card.draw(screen)

    cards.append(card)

    card = Card("sadness", "emotion_recognition_game_data/inside-out-sadness.jpg", cardback, (750,550), gamerunner)
    card.draw(screen)

    cards.append(card)

    # card = Card("surprise", "emotion_recognition_game_data/inside-out-surprise.jpg", cardback, (1350,550), gamerunner)
    # card.draw(screen)

    # cards.append(card)

    # add clock so that cpu does not go to 100%
    clock = pygame.time.Clock()

    while 1:
        clock.tick(30)
        # process pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == QUIT or event.type == STOP_EMOREC:
                return

            for card in cards:
                card.process_event(event, cards, screen)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                redraw(cards, screen)
                activate(cards,screen)
    


