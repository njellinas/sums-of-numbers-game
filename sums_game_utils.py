import random
import time
import pygame.time

from card_utils import deactivate_numbers, redraw, activate_numbers

HOLDER1 = 'cardholder1'
HOLDER2 = 'cardholder2'


def select_number_once(card, cards, game_dict, screen):
    flag = False
    for key in [0, 1, 2, 3, 4]:
        if cards[key].chosen_once:
            cards[key].chosen_once = False
            flag = True
            card.chosen_once = True
            redraw(cards, screen)
            game_dict['cardholderc'].position = (card.position[0]-5, card.position[1]-5)
            game_dict['cardholderc'].draw(screen)
    if not flag:
        card.chosen_once = True
        game_dict['cardholderc'].position = (card.position[0]-5, card.position[1]-5)
        game_dict['cardholderc'].draw(screen)

def select_number(card, cards, game_dict, screen):
    if game_dict['cardholders_full'] == 0:
        card.chosen = True
        card.chose_number(0)
        cards[HOLDER1].chosen = True  # Card in first cardholder
        game_dict['cardholders_full'] += 1
        game_dict['current_sum'] += card.number
        # --- SELECT FIRST CARD --- #
        card.gamerunner.send_event('athena.games.sums.card_selected', 'sums_game', card.number)
    elif game_dict['cardholders_full'] == 1 and cards[HOLDER1].chosen:
        card.chosen = True
        card.chose_number(1)
        cards[HOLDER2].chosen = True  # Card in second cardholder
        game_dict['cardholders_full'] += 1
        game_dict['current_sum'] += card.number
        card.gamerunner.send_event('athena.games.sums.card_selected', 'sums_game', card.number)
    elif game_dict['cardholders_full'] == 1 and cards[HOLDER2].chosen:
        card.chosen = True
        card.chose_number(0)
        cards[HOLDER1].chosen = True  # Card in first cardholder
        game_dict['cardholder1_card'] = card
        game_dict['cardholders_full'] += 1
        game_dict['current_sum'] += card.number
        card.gamerunner.send_event('athena.games.sums.card_selected', 'sums_game', card.number)
    else:
        print('Cardholders full!')
    if game_dict['cardholders_full'] == 2:  # Calculate sum and evaluate
        if game_dict['current_sum'] == 4:
            cards['correctwrong_box'].color = (0, 200, 0)
            cards['correct'].toggle_hidden()
            card.gamerunner.send_event('athena.games.sums.sumcorrect', 'sums_game', text='child')
            deactivate_numbers(cards=cards)
            print('Correct!')
        else:
            cards['correctwrong_box'].color = (200, 0, 0)
            cards['wrong'].toggle_hidden()
            card.gamerunner.send_event('athena.games.sums.sumwrong', 'sums_game', text='child')
            deactivate_numbers(cards=cards)
            print('Wrong!')
    redraw(cards, screen)

def deselect_number(card, cards, game_dict, screen):
    if game_dict['cardholders_full'] > 0:
        card.chosen = False
        card.chosen_once = False
        i = card.reset_number()
        if i == 0:
            cards[HOLDER1].chosen = False  # Card removed from first cardholder
        else:
            cards[HOLDER2].chosen = False  # Card removed from second cardholder
        game_dict['cardholders_full'] -= 1
        game_dict['current_sum'] -= card.number
        cards['correctwrong_box'].color = (81, 193, 206)
        cards['correct'].hide_if_active()
        cards['wrong'].hide_if_active()
        redraw(cards, screen)
    else:
        print('All cardholders empty!')

def open_only_first_cardholder(cards, game_dict, screen):
    if cards[HOLDER1].chosen:
        card1 = game_dict['cardholder1_card']
        card1.chosen = False
        card1.chosen_once = False
        i = card1.reset_number()
        cards[HOLDER1].chosen = False  # Card removed from first cardholder
        game_dict['cardholders_full'] -= 1
        game_dict['current_sum'] -= card1.number
        cards['correctwrong_box'].color = (81, 193, 206)
        cards['correct'].hide_if_active()
        cards['wrong'].hide_if_active()
        activate_numbers(cards)
        redraw(cards, screen)

def robot_make_wrong_sum(cards, game_dict, screen):
    card_numbers = [0, 1, 2, 3, 4]
    random.shuffle(card_numbers)
    second = game_dict['current_second']
    for i in card_numbers:
        if i + second != 4:
            select_number_once(cards[i], cards, game_dict, screen)
            game_dict['robot_select'] = i
            break
    deactivate_numbers(cards)
    cards[0].gamerunner.send_event('athena.games.sums.robotsumready', 'sums_game', text=str(i))

def robot_make_correct_sum(cards, game_dict, screen):
    card_numbers = [0, 1, 2, 3, 4]
    second = game_dict['current_second']
    for i in card_numbers:
        if i + second == 4:
            select_number_once(cards[i], cards, game_dict, screen)
            game_dict['robot_select'] = i
            break
    deactivate_numbers(cards)
    cards[0].gamerunner.send_event('athena.games.sums.robotsumready', 'sums_game', text=str(i))

def robot_put_number(cards, game_dict, screen):
    select_number(cards[game_dict['robot_select']], cards, game_dict, screen )
    print(game_dict['current_sum'])
    if game_dict['current_sum'] != 4:
        cards[0].gamerunner.send_event('athena.games.sums.sumwrong', 'sums_game', text='robot')
    else:
        cards[0].gamerunner.send_event('athena.games.sums.sumcorrect', 'sums_game', text='robot')

def robot_make_first_choice(card, cards, game_dict, screen):
    card_numbers = [0, 1, 2, 3, 4]
    card = cards[random.choice(card_numbers)]
    select_number(card, cards, game_dict, screen)
    activate_numbers(cards)
    card.can_open = False
