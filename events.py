from pygame.locals import USEREVENT

# ----- EVENTS ----- #
START_SUMS = USEREVENT + 1
STOP_SUMS = USEREVENT + 2

ENABLECARDS = USEREVENT + 3
DISABLECARDS = USEREVENT + 4

ROBOTWRONGSUMSELECT = USEREVENT + 5
ROBOTSUMMAKE = USEREVENT + 6
ROBOTCORRECTSUMSELECT = USEREVENT + 7
CHILDRETRY = USEREVENT + 8
RESETCARDHOLDER = USEREVENT + 9
