import pygame
import random

# Pygame setup
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Card Game")

# Card class
class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

# Deck class
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", 
                 "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace", "Back"]
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        for suit in suits:
            for rank, value in zip(ranks, values):
                self.cards.append(Card(suit, rank, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()
    
    def load_card_images(self, filename):
        card_images = {}
        ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", 
                "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace", "Joker", "Back"]
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        
        # Load the sprite sheet
        sprite_sheet = pygame.image.load(filename).convert_alpha()

        # Assume each card image is 73 pixels wide and 98 pixels high
        # You'll need to change these numbers if your sprite sheet has different dimensions
        self.card_width = 100
        self.card_height = 144

        for suit in suits:
            for rank in ranks:
                if ((rank == "Joker")):
                    continue
                # Calculate the position of the card image on the sprite sheet
                x = ranks.index(rank) * self.card_width
                y = suits.index(suit) * self.card_height

                # Extract the card image
                image = sprite_sheet.subsurface(pygame.Rect(x, y, self.card_width, self.card_height))

                # Add the card image to the dictionary
                card_images[(rank, suit)] = image

        # print(card_images)
        return card_images

