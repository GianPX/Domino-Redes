import pygame, random, serial, json

#Serial Functions
def write(header,object):
    ser.write((header+json.dumps(object)+'\n').encode('utf-8'))

def writeText(text):
    ser.write((text+'\n').encode('utf-8'))

def read():
    text=ser.readline()
    text=text.decode('utf-8')
    text=text.replace('\n','')
    return text

def writeAll():
    write('b',board)
    write('d',dominoes)
    write('p',player_hand)
    write('c',computer_hand)

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

turn = bool

#set up Serial Conection
ser = serial.Serial()
ser.baudrate = 9600
ser.timeout = 0.1
ser.port = input('Ingrese el nombre del puerto serial: ')
ser.open()
playerNumber = input('Ingrese el número del jugador (1/2): ')

#Set up game
if playerNumber == '1':
    print('Esperando jugador 2...')
    ready = False
    while not ready:
        writeAll()
        readyText=read()
        if readyText == 'ready':
            ready=True
            print('Empieza el juego')
    turn = True
elif playerNumber == '2':
    dominoesReady = False
    boardReady = False
    player_handReady = False
    computer_handReady = False
    ready = False
    while not ready:
        text=read()
        match text[0]:
            case 'b':
                text=text.replace('b','')
                board=json.loads(text)
                boardReady = True
            case 'd':
                text=text.replace('d','')
                dominoes=json.loads(text)
                dominoesReady = True
            case 'p':
                text=text.replace('p','')
                computer_hand=json.loads(text)
                computer_handReady=True
            case 'c':
                text=text.replace('c','')
                player_hand=json.loads(text)
                player_handReady=True
        if boardReady and dominoesReady and player_handReady and computer_handReady:
            ready=True
            writeText('ready')
    turn = False
# set up the game loop
clock = pygame.time.Clock()
game_over = False

while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if turn:
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
                            writeText('your turn')
                            writeAll()
                            turn = False
                        elif domino[1] == board[-1][1]:
                            board.append((domino[1], domino[0]))
                            player_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            turn = False
                        elif domino[0] == board[0][0]:
                            board.insert(0, (domino[1], domino[0]))
                            player_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            turn = False
                        elif domino[1] == board[0][0]:
                            board.insert(0, domino)
                            player_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            turn = False

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
        x = 350+(len(board)-1)*25 - i * 50
        y = 300
        pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)
        text = font.render(f"{domino[1]}-{domino[0]}", True, BLACK)
        screen.blit(text, (x + 5, y + 5))

    winLabel = font.render("GANASTE!!!",True,(255,255,255))
    loseLabel = font.render("PERDISTE...",True,(255,25,255))

    if len(player_hand) ==0:
        screen.blit(winLabel,(350,30))
        game_over = True
    if len(computer_hand) ==0:
        screen.blit(loseLabel,(350,30))
        game_over = True

    
    # update the display
    pygame.display.update()

    #Receive game information
    if not turn:
        text=read()
        if text == 'your turn':
            dominoesReady = False
            boardReady = False
            player_handReady = False
            computer_handReady = False
            ready = False
            while not ready:
                text=read()
                match text[0]:
                    case 'b':
                        text=text.replace('b','')
                        board=json.loads(text)
                        boardReady = True
                    case 'd':
                        text=text.replace('d','')
                        dominoes=json.loads(text)
                        dominoesReady = True
                    case 'p':
                        text=text.replace('p','')
                        computer_hand=json.loads(text)
                        computer_handReady=True
                    case 'c':
                        text=text.replace('c','')
                        player_hand=json.loads(text)
                        player_handReady=True
                if boardReady and dominoesReady and player_handReady and computer_handReady:
                    ready = True
                    turn=True

    # limit the frame rate
    clock.tick(60)

# quit Pygame
#pygame.quit()