def redraw(cards, screen):
    screen.fill((0, 0, 0))
    for card in cards:
        card.draw(screen)


def deactivate(cards, screen):
    for card in cards:
        card.can_open = False


def activate(cards, screen):
    for card in cards:
        card.can_open = True
