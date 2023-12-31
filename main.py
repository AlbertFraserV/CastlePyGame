import pygame
import random
from deck import Card, Deck
from player import Player
from setup import Setup
from rules import Rules
from draw import Draw
from config import Config


# Initialize the Pygame font
pygame.font.init()
font = pygame.font.Font(None, 36)  # Choose the font size

#Initialize window
pygame.init()
window_x = 800  
window_y = 800
config = Config(window_x,window_y)
window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Card Game")

#Initialize game state properties
center_pile = []
entire_pile =[]
active_player = None

#Initialize game objects
running = True
deck = Deck()
deck.shuffle()
card_images = deck.load_card_images('CuteCards.png')
player = Player(config, "Player 1", "human", 0, False, None)
computer = Player(config, "Computer 1", "computer", 1, False, None)
player_list = [player, computer]
rules = Rules(config, player_list, debug_mode = True)
setup = Setup(config, player_list)
draw_tool = Draw(config, window, player_list, card_images, font)

while running:
    # Event handling
    # During the event handling phase:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and len(player.castle) < 6:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, (card_rect, card) in enumerate(zip(player.hand_rect, player.hand)):
                if card_rect.collidepoint(mouse_x, mouse_y):
                    player.castle_rect.append(player.castle_rect[len(player.castle_rect)-3])
                    player.castle.append(card)
                    player.hand_rect.pop(i)  # Remove the card's Rect from hand
                    player.hand.pop(i)  # Remove the card from hand
                    break

        if active_player:
            next_player = active_player.play_hand(event, center_pile, entire_pile, deck, player_list)
            #Clear the deck if 10 is played
            if len(entire_pile) > 0:
                if entire_pile[-1].rank == "Ten":
                    entire_pile.clear()
                    center_pile.clear()
                    active_player.refill_hand(deck)
                    continue
                if rules.check_four_in_a_row(entire_pile):
                    entire_pile.clear()
                    center_pile.clear()
                    active_player.refill_hand(deck)
                    continue
            active_player.refill_hand(deck)
            active_player = next_player

    ####Setup the game
    #Create both player's initial Castle and their locations on-screen.
    if not player.castle and not computer.castle and len(deck.cards) > 0:
        setup.setup_castle(deck)

    #Create bother player's hands and their locations on screen
    if not player.hand and not computer.hand and len(deck.cards) > 0:
        setup.deal_init_hand(deck)

    #Have the computer player randomly select which cards to put on the castle.
    if len(computer.castle) == 3 and len(deck.cards) > 0:
        setup.computer_place_castle_cards()

    #Place starting pile card
    if len(computer.castle) == 6 and len(player.castle) == 6 and len(deck.cards) > 0:
        if len(deck.cards) == 34:
            active_player = setup.find_and_place_starting_card(center_pile, entire_pile)
            if len(player.hand) < 3:
                player.hand.append(deck.draw_card())
                player.hand_rect.append(pygame.Rect(0, window_y-200, deck.card_width, deck.card_height))
            if len(computer.hand) < 3:
                computer.hand.append(deck.draw_card())
                computer.hand_rect.append(pygame.Rect(0, window_y-800, deck.card_width, deck.card_height))

    window.fill((0, 0, 0))  # Clear the screen
    draw_tool.draw_cards(center_pile, entire_pile, deck)  # Draw all cards
    textsurface = font.render(str(len(entire_pile)), False, (255, 255, 255))
    window.blit(textsurface,(window_x/2-deck.card_width-300, window_y/2-deck.card_height+50))
    pygame.display.flip()  # Update the display
    # if played:
    #     pygame.time.wait(1000)  # Wait for a second
    #     played = False  # Reset card_played to False

pygame.quit()