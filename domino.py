import pygame
import random

# initialize Pygame
pygame.init()

# set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dominoes")

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up the fonts
FONT_SIZE = 30
font = pygame.font.SysFont(None, FONT_SIZE)

# set up the game
dominoes = []
for i in range(7):
    for j in range(i, 7):
        dominoes.append((i, j))

random.shuffle(dominoes)
player_hand = dominoes[:7]
computer_hand = dominoes[7:14]
board = [dominoes[14]]

# set up the game loop
clock = pygame.time.Clock()
game_over = False

while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if the user clicked on a domino in their hand
            pos = pygame.mouse.get_pos()
            for i, domino in enumerate(player_hand):
                x = 150 + i * 50
                y = 450
                if x <= pos[0] <= x + 40 and y <= pos[1] <= y + 60:
                    # check if the domino can be placed on the board
                    if domino[0] == board[-1][1]:
                        board.append(domino)
                        player_hand.remove(domino)
                    elif domino[1] == board[-1][1]:
                        board.append((domino[1], domino[0]))
                        player_hand.remove(domino)
                    elif domino[0] == board[0][0]:
                        board.insert(0, (domino[1], domino[0]))
                        player_hand.remove(domino)
                    elif domino[1] == board[0][0]:
                        board.insert(0, domino)
                        player_hand.remove(domino)

    # draw the board
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, (100, 100, 600, 400), 2)
    pygame.draw.rect(screen, BLACK, (150, 150, 500, 300), 2)

    # draw the player's hand
    for i, domino in enumerate(player_hand):
        x = 150 + i * 50
        y = 450
        pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)
        text = font.render(f"{domino[0]}-{domino[1]}", True, BLACK)
        screen.blit(text, (x + 5, y + 5))

    # draw the computer's hand
    for i, domino in enumerate(computer_hand):
        x = 150 + i * 50
        y = 90
        pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)

    # draw the board
    for i, domino in enumerate(board):
        x = 350 - i * 50
        y = 300
        pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)
        text = font.render(f"{domino[1]}-{domino[0]}", True, BLACK)
        screen.blit(text, (x + 5, y + 5))

    # update the display
    pygame.display.update()

    # limit the frame rate
    clock.tick(60)

# quit Pygame
pygame.quit()