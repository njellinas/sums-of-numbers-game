#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from random import shuffle
import os
import time

from card import Card
from card_utils import activate, redraw

STOP_SUMS = USEREVENT + 2
global previous_time


def start_sums_game(screen, gamerunner):
    global previous_time
    #    pygame.init()
    screen.fill((0, 0, 0))
    #   screen = create_screen()
    pygame.display.set_caption('Sums Game')

    previous_time = -200

    cardback = "sums_game_data/black.jpg"

    # Screen size
    w, h = pygame.display.get_surface().get_size()
    print(w, h)

    # -------------------------- START GAME EVENT ---------------------------------#
    gamerunner.send_event('athena.games.sums.start', 'sums_game')

    # ----------------------------------- GAME PARAMETERS -------------------------#
    number_of_top_cards = 6

    # Card width
    cw = int(0.12 * w)
    # Card height
    ch = int(0.3 * h)
    # Space between cards
    s = int((0.9 * w - number_of_top_cards * cw) / (number_of_top_cards + 1))
    cards = {}

    card_posx_list = [0 for i in range(number_of_top_cards)]
    card_posx_list[0] = int(0.05 * w + s)
    for i in range(1, number_of_top_cards):
        card_posx_list[i] = card_posx_list[i - 1] + cw + s
    shuffle(card_posx_list)
    card_posy = 0.1 * h
    card = Card(0, "sums_game_data/zero.gif", cardback,
                (card_posx_list[0], card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards[0] = card

    card = Card(1, "sums_game_data/one.gif", cardback,
                (card_posx_list[1], card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards[1] = card

    card = Card(2, "sums_game_data/two.gif", cardback,
                (card_posx_list[2], card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards[2] = card

    card = Card(3, "sums_game_data/three.gif", cardback,
                (card_posx_list[3], card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards[3] = card

    card = Card(4, "sums_game_data/four.gif", cardback,
                (card_posx_list[4], card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards[4] = card

    card = Card(2, "sums_game_data/two.gif", cardback,
                (card_posx_list[5], card_posy), (cw, ch), gamerunner)
    card.draw(screen)
    cards[22] = card

    # SECOND LINE
    second_line_h = h - 0.1 * h - ch

    # SYMBOLS SIZES
    cw2 = int(0.5 * cw)
    ch2 = int(0.5 * ch)
    # Distance from the sides = k
    k = int(0.5 * (w - 4 * s - 3 * cw - 2 * cw2))

    # DRAW SYMBOLS
    card2_posx = k + cw + s
    card2_posy = second_line_h + int(0.5 * (cw - cw2))
    card2 = Card("plus", "sums_game_data/plus.jpg", cardback,
                 (card2_posx, card2_posy), (cw2, ch2), gamerunner)
    card2.can_open = False
    card2.draw(screen)
    cards['plus'] = card2

    card2_posx = card2_posx + cw2 + 2 * s + cw
    card2 = Card("equal", "sums_game_data/equal.png", cardback,
                 (card2_posx, card2_posy), (cw2, ch2), gamerunner)
    card2.can_open = False
    card2.draw(screen)
    cards['equal'] = card2

    # DRAW CARDHOLDERS #
    cardholder1_posx = k
    cardholder1_posy = second_line_h
    cardholder1 = Card("cardholder1", "sums_game_data/equal.png", cardback,
                       (cardholder1_posx, cardholder1_posy), (cw, ch), gamerunner,
                       cardholder=True)
    cardholder1.can_open = False
    cardholder1.draw(screen)
    cards['cardholder1'] = cardholder1

    cardholder2_posx = cardholder1_posx + cw + cw2 + 2 * s
    cardholder2_posy = cardholder1_posy
    cardholder2 = Card("cardholder1", "sums_game_data/equal.png", cardback,
                       (cardholder2_posx, cardholder2_posy), (cw, ch), gamerunner,
                       cardholder=True)
    cardholder2.can_open = False
    cardholder2.draw(screen)
    cards['cardholder2'] = cardholder2

    # LAST CARD 4
    card3_posx = cardholder2_posx + cw + 2 * s + cw2
    card3 = Card(4, "sums_game_data/four.gif", cardback,
                 (card3_posx, cardholder2_posy), (cw, ch), gamerunner)
    card3.can_open = False
    card3.draw(screen)
    cards['target_sum'] = card3

    # CORRECT AND WRONG BOX
    cory = int(h / 2 + (h - 0.2 * h - 2 * ch) / 4)
    corx = k - s
    corw = w - 2 * k + 2 * s
    corh = int(ch + (h - 0.2 * h - 2 * ch) / 2)
    cor = Card("correct", "sums_game_data/equal.png", cardback,
               (corx, cory), (corw, corh), gamerunner, cardholder=True, color=(0, 0, 0))
    cor.can_open = False
    cor.draw(screen)
    cards['correctwrong_box'] = cor

    # CORRECT SIGN
    corsign_w = int(0.7 * cw2)
    corsign_h = int(0.7 * ch2)
    corsign_x = corx + corw + s
    corsign_y = int(cory + (corh - corsign_h) / 2)
    corsign = Card("correct_sign", cardback, "sums_game_data/correct.png",
                   (corsign_x, corsign_y), (corsign_w, corsign_h), gamerunner)
    corsign.can_open = False
    corsign.draw(screen)
    cards['correct'] = corsign

    # WRONG SIGN
    wrongsign_x = corx - s - corsign_w
    wrongsign = Card("wrong_sign", cardback, "sums_game_data/wrong.png",
                     (wrongsign_x, corsign_y), (corsign_w, corsign_h), gamerunner)
    wrongsign.can_open = False
    wrongsign.draw(screen)
    cards['wrong'] = wrongsign

    # PASS THE CARDHOLDERS POSITIONS AS PARAMETERS
    for key in cards:
        cards[key].cardholder_positions = ((cardholder1_posx, cardholder1_posy), (cardholder2_posx, cardholder2_posy))

    # GAME DICTIONARY
    game_dict = {'cardholders_full': 0, 'current_sum': 0}

    # add clock so that cpu does not go to 100%
    clock = pygame.time.Clock()

    # EVENT PROCESSING
    while 1:
        clock.tick(30)
        # process pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == QUIT or event.type == STOP_SUMS:
                return

            for key in cards:
                cards[key].process_event(event, cards, screen, game_dict=game_dict)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                redraw(cards, screen)
                activate(cards, screen)
