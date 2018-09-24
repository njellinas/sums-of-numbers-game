import os
import sys
import sums_game
import pygame
from pygame.locals import *
import socket
import threading
import json

START_SUMS = USEREVENT + 1
STOP_SUMS = USEREVENT + 2
MODE = "ASD"

# ----- EVENTS ----- #
ENABLECARDS = USEREVENT + 3
DISABLECARDS = USEREVENT + 4

ROBOTWRONGSUMSELECT = USEREVENT + 5
ROBOTWRONGSUMMAKE = USEREVENT + 6
CHILDSHOWCORRECT = USEREVENT + 7
ROBOTCORRECTSUM = USEREVENT + 8
CHILDRETRY = USEREVENT + 9


class GameRunner(object):
    """docstring for GameRunner"""

    def __init__(self, wizard_mode):
        super(GameRunner, self).__init__()
        pygame.init()
        self.infoObject = pygame.display.Info()
        screen_size = (self.infoObject.current_w, self.infoObject.current_h)
        # screen_size = (1024, 768)
        self.screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
        bg = pygame.image.load("sums_game_data/green.png")
        self.bg = pygame.transform.scale(bg, screen_size)
        self.game_state = "SCREENSAVER"
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

    def connect_to_broker(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipaddress = '192.168.0.127'
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
            print line
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
                elif event_name == 'athena.games.sums.robotwrongsum.make':
                    pygame.event.post(pygame.event.Event(ROBOTWRONGSUMMAKE, {}))
                elif event_name == 'athena.games.sums.childshowcorrect':
                    pygame.event.post(pygame.event.Event(CHILDSHOWCORRECT, {}))
                elif event_name == 'athena.games.sums.robotcorrectsum':
                    pygame.event.post(pygame.event.Event(ROBOTCORRECTSUM, {}))
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
        self.screen.fill((81, 193, 206))
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()

    def run_games(self):
        self.screensaver()
        clock = pygame.time.Clock()

        keep = True
        # gesture_recognition_game.start_gesture_game(self.screen)

        while keep:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h),
                                                          pygame.NOFRAME)
                if event.type == START_SUMS:
                    sums_game.start_sums_game(self.screen, self, wizard_mode=False)
                    self.screensaver()
                if event.type == QUIT:
                    return

    def clear_screen(self):
        self.screen.fill((81, 193, 206))
        pygame.display.flip()

    def run_games_wizard(self):
        clock = pygame.time.Clock()

        keep = True

        while keep:
            clock.tick(30)
            self.clear_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    keep = False

                if event.type == QUIT:
                    keep = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    sums_game.start_sums_game(self.screen, self, wizard_mode=True)

    def run_games_wizard_1(self):
        # self.screensaver_wizard()

        # farm_game.start_farm_game(self.screen, self)

        self.screensaver_wizard()

        # emotion_recognition_game.start_emotion_game(self.screen, self)

        # self.screensaver_wizard()

        # pantomime_game.start_pantomime_game(self.screen, self, game_type=MODE)

        # self.screensaver_wizard()

        # moving_in_game.start_moving_in(self.screen)

        # self.screensaver_wizard()


def main():
    if sys.argv[-1] == 'woz':
        game_runner = GameRunner(wizard_mode=True)
    else:
        game_runner = GameRunner(wizard_mode=False)


if __name__ == '__main__':
    main()
