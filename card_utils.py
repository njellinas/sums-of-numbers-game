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
