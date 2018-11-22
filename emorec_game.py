#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
import time

from config import cfg
from events import GAME_EVENT
from card import Card

class EmorecGame(object):
    def __init__(self, cfg, screen, gamerunner):
        self.cfg = cfg
        self.screen = screen
        self.gamerunner = gamerunner
        # Screen size
        self.w, self.h = pygame.display.get_surface().get_size()
        self.cw = int(0.2 * self.w)
        self.ch = int(0.5 * self.h)
        self.card_posx = int((self.w - self.cw) / 2)
        self.card_posy = int((self.h - self.ch) / 2)
    
    def process_game_event(self, event):
        if event.name == 'athena.games.emorec.clearcards':
            self.clear_cards()
        elif event.name == 'athena.games.emorec.showhappinessDim':
            self.show_happinessDim_card()
        elif event.name == 'athena.games.emorec.showsadnessDim':
            self.show_sadnessDim_card()
        elif event.name == 'athena.games.emorec.showfearDim':
            self.show_fearDim_card()
        elif event.name == 'athena.games.emorec.showangerDim':
            self.show_angerDim_card()
        elif event.name == 'athena.games.emorec.showsadnessAnd':
            self.show_sadnessAnd_card()
        elif event.name == 'athena.games.emorec.showfearAnd':
            self.show_fearAnd_card()
        elif event.name == 'athena.games.emorec.showangerAnd':
            self.show_angerAnd_card()

    def show_happinessDim_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(0, self.cfg['happyDim_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)

    def show_sadnessDim_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(1, self.cfg['sadDim_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)
    
    def show_sadnessAnd_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(1, self.cfg['sadAnd_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)
    
    def show_fearDim_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(1, self.cfg['fearDim_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)
    
    def show_fearAnd_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(1, self.cfg['fearAnd_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)
    
    def show_angerDim_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(1, self.cfg['angerDim_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)
    
    def show_angerAnd_card(self):
        pygame.display.set_caption('Emorec Game')
        cardback = self.cfg['cardback']

        card = Card(1, self.cfg['angerAnd_card'], cardback,
                    (self.card_posx, self.card_posy), (self.cw, self.ch), self.gamerunner)
        card.draw(self.screen)

    def clear_cards(self):
        pygame.display.set_caption('Emorec Game')
        self.screen.fill(cfg['background_color'])
        pygame.display.flip()
        
