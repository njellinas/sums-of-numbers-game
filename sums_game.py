#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
import time

from card import Card, CardHolder
from card_utils import activate, redraw

STOP_EMOREC = USEREVENT + 2
global previous_time


def start_sums_game(screen, gamerunner):
    global previous_time
    #    pygame.init()
    screen.fill((0, 0, 0))
    #   screen = create_screen()
    pygame.display.set_caption('Emotion Recognition')

    previous_time = -200

    cardback = "emotion_recognition_game_data/question.jpg"

    # Screen size
    w, h = pygame.display.get_surface().get_size()
    print(w, h)
    # Card width
    cw = int(0.14 * w)
    # Card height
    ch = int(0.2 * h)
    # Space between cards
    s = int((0.8 * w - 5 * cw) / 6)
    cards = []

    card_posx = int(0.1 * w + s)  # + cw / 2)
    card_posy = 0.2 * h
    card = Card("happiness", "sums_game_data/zero.gif", cardback,
                (card_posx, card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards.append(card)

    card_posx += cw + s
    card = Card("fear", "sums_game_data/one.gif", cardback,
                (card_posx, card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards.append(card)

    card_posx += cw + s
    card = Card("disgust", "sums_game_data/two.gif", cardback,
                (card_posx, card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards.append(card)

    card_posx += cw + s
    card = Card("anger", "sums_game_data/three.gif", cardback,
                (card_posx, card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards.append(card)

    card_posx += cw + s
    card = Card("sadness", "sums_game_data/four.gif", cardback,
                (card_posx, card_posy), (cw, ch), gamerunner)
    card.draw(screen)

    cards.append(card)

    # DRAW CARD HOLDERS #
    # cardholder1 = CardHolder((300, 300), (cw, ch))
    # cardholder1.draw(screen)

    # add clock so that cpu does not go to 100%
    clock = pygame.time.Clock()

    # EVENT PROCESSING
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
                activate(cards, screen)
