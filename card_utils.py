def redraw(cards, screen):
    screen.fill((0, 0, 0))
    for key in cards:
        cards[key].draw(screen)


def deactivate(cards, screen):
    for key in cards:
        cards[key].can_open = False


def activate(cards, screen):
    for key in cards:
        cards[key].can_open = True


def activate_numbers(cards):
    for key in [0, 1, 2, 3, 4, 22]:
        cards[key].can_open = True


def deactivate_numbers(cards):
    for key in [0, 1, 2, 3, 4, 22]:
        cards[key].can_open = False
