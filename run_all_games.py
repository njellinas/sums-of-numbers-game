import os
import sys
from sums_game import SumsGame
import pygame
from pygame.locals import *
import socket
import threading
import json
from events import *
from config import cfg

class GameRunner(object):
    """docstring for GameRunner"""

    def __init__(self, wizard_mode):
        super(GameRunner, self).__init__()
        pygame.init()
        self.infoObject = pygame.display.Info()
        if cfg['screen_size']:
            screen_size = cfg['screen_size']
        else:
            screen_size = (self.infoObject.current_w, self.infoObject.current_h)
        self.screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
        bg = pygame.image.load(cfg['cardback'])
        self.bg = pygame.transform.scale(bg, screen_size)
        self.event_id = 1

        if not wizard_mode:
            self.t1 = threading.Thread(target=self.connect_to_broker)
            self.t1.daemon = True
            self.t1.start()
            self.connected = True
            self.run_games()
        else:
            self.connected = False
            self.run_games_wizard()

    def readlines(self, sock, recv_buffer=4096, delim='\n'):
        buffer = ''
        data = True
        while data:
            data = sock.recv(recv_buffer)
            buffer += data

            while buffer.find(delim) != -1:
                line, buffer = buffer.split('\n', 1)
                yield line
        return

    # ------------- THREAD 1 ------------- #
    def connect_to_broker(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipaddress = '192.168.2.8'
        port = 1932
        # Connect the socket to the port where the server is listening
        server_address = (ipaddress, port)
        self.sock.connect(server_address)
        message = 'CONNECT furhat games \n'
        self.sock.sendall(message)

        l = self.sock.recv(8192)
        print l

        message = 'SUBSCRIBE athena.games.** \n'
        self.sock.sendall(message)

        for line in self.readlines(self.sock):
            print('line: ', line)
            if line.startswith("EVENT"):
                data_arr = line.split()
                event_name = data_arr[1]
                self.game_state = "waiting"
                if event_name == "athena.games.sums.showcards" and self.game_state != "SUMS":
                    self.game_state = "SUMS"
                    pygame.event.post(pygame.event.Event(START_SUMS, {}))
                elif event_name == "athena.games.sums.stop":
                    pygame.event.post(pygame.event.Event(STOP_SUMS, {}))
                elif event_name == 'athena.games.sums.enablecards':
                    pygame.event.post(pygame.event.Event(ENABLECARDS, {}))
                elif event_name == 'athena.games.sums.disablecards':
                    pygame.event.post(pygame.event.Event(DISABLECARDS, {}))
                elif event_name == 'athena.games.sums.robotwrongsum.select':
                    pygame.event.post(pygame.event.Event(ROBOTWRONGSUMSELECT, {}))
                elif event_name == 'athena.games.sums.robotsum.make':
                    pygame.event.post(pygame.event.Event(ROBOTSUMMAKE, {}))
                elif event_name == 'athena.games.sums.robotcorrectsum.select':
                    pygame.event.post(pygame.event.Event(ROBOTCORRECTSUMSELECT, {}))
                elif event_name == 'athena.games.sums.resetcardholder':
                    pygame.event.post(pygame.event.Event(RESETCARDHOLDER, {}))
                elif event_name == 'athena.games.sums.childretry':
                    pygame.event.post(pygame.event.Event(CHILDRETRY, {}))

    def send_event(self, event_name, sender, text=None):
        if not self.connected:
            return
        data = {}
        data["class"] = "iristk.system.Event"
        data["event_name"] = event_name
        if text:
            data["text"] = text
        data["event_sender"] = sender
        data["event_id"] = "gamerunner" + str(self.event_id)

        json_data = json.dumps(data)

        message = "EVENT " + event_name + " " + str(len(json_data)) + " \n"
        # print message
        # print json_data
        self.sock.sendall(message)
        self.sock.sendall(json_data)

        self.event_id += 1

    def screensaver(self):
        self.screen.fill(cfg['background_color'])
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()

    # ------------- THREAD 2 --------------- #
    def run_games(self):
        self.screensaver()
        clock = pygame.time.Clock()

        sumsgame = SumsGame(cfg=cfg, screen=self.screen, gamerunner=self, wizard_mode=False)

        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == START_SUMS:
                    sumsgame.init_game()
                    self.screensaver()
                # escape key
                if event.type == QUIT:
                    return

    def clear_screen(self):
        self.screen.fill(cfg['background_color'])
        pygame.display.flip()

    def run_games_wizard(self):
        clock = pygame.time.Clock()

        keep = True
        sumsgame = SumsGame(cfg=cfg, screen=self.screen, gamerunner=self, wizard_mode=True)

        while keep:
            clock.tick(30)
            self.clear_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    keep = False

                if event.type == QUIT:
                    keep = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    sumsgame.init_game()


def main():
    if sys.argv[-1] == 'woz':
        game_runner = GameRunner(wizard_mode=True)
    else:
        game_runner = GameRunner(wizard_mode=False)


if __name__ == '__main__':
    main()
