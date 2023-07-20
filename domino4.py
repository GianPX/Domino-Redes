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
    write('u',player1_hand)
    write('d',player2_hand)
    write('t',player3_hand)
    write('c',player4_hand)

# initialize Pygame
pygame.init()

# set up the display
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
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
player1_hand = dominoes[:7]
player2_hand = dominoes[7:14]
player3_hand = dominoes[14:21]
player4_hand = dominoes[21:28]
board = []

#Variables
turn = bool
yourScore = 0
rivalScore = 0
gameWin = False
gameLose = False
gameDraw = False
round = 0
contPass = 0
countPossiblePlays = 0

#set up Serial Conection
ser = serial.Serial()
ser.baudrate = 9600
ser.timeout = 0.1
#ser.port = input('Ingrese el nombre del puerto serial: ')
ser.port = 'COM1'
ser.open()
playerNumber = input('Ingrese el número del jugador (1/2/3/4): ')

#Set up game
if playerNumber == '1':
    print('Esperando jugadores...')
    ready = False
    writeAll()
    while not ready:
        readyText=read()
        if readyText == 'ready':
            ready=True
            print('Empieza el juego')
    turn = True

else:
    player1_handReady = False
    player2_handReady = False
    player3_handReady = False
    player4_handReady = False
    ready = False
    while not ready:
        text=read()
        match text[0]:
            case 'u':
                text=text.replace('u','')
                player4_hand=json.loads(text)
                player4_handReady = True
            case 'd':
                text=text.replace('d','')
                player1_hand=json.loads(text)
                player1_handReady = True
            case 't':
                text=text.replace('t','')
                player2_hand=json.loads(text)
                player2_handReady = True
            case 'c':
                text=text.replace('c','')
                player3_hand=json.loads(text)
                player3_handReady = True
        if player1_handReady and player2_handReady and player3_handReady and player4_handReady:
            ready=True
            writeText('ready')
            writeAll()
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
                for i, domino in enumerate(player1_hand):
                    x = 150 + i * 50
                    y = 450
                    if x <= pos[0] <= x + 40 and y <= pos[1] <= y + 60:
                        # check if the domino can be placed on the board
                        if len(board) == 0:
                            
                            
                            
                            board.append(domino)
                            player1_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            round+=1
                            turn = False
                            contPass = 0
                        elif domino[0] == board[-1][1]:
                            
                            countPossiblePlays += 1;
                            
                            board.append(domino)
                            player1_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            round+=1
                            turn = False
                            contPass = 0
                        elif domino[1] == board[-1][1]:
                            board.append((domino[1], domino[0]))
                            player1_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            round+=1
                            turn = False
                            contPass = 0
                        elif domino[0] == board[0][0]:
                            board.insert(0, (domino[1], domino[0]))
                            player1_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            round+=1
                            turn = False
                            contPass = 0
                        elif domino[1] == board[0][0]:
                            board.insert(0, domino) #Estos inserts se eliminarian CREO para que no inserte el domino
                            player1_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            round+=1
                            turn = False
                            contPass = 0
                            
                    #Luego de chequear iria aqui la logica de insertarlo
                    
                    
                    
                    #PlayRright Button Logic 
                            board.insert(0, domino)
                            player1_hand.remove(domino)
                            writeText('your turn')
                            writeAll()
                            round+=1
                            turn = False
                            contPass = 0
                    #Si esta bien es lo mismo para PlayLeft
                    
                    
                    
                    
                #Pass button logic
                if passButton.collidepoint(pos):
                    contPass+=1
                    writeText('pass')
                    writeText(str(contPass))
                    writeText('your turn')
                    writeAll()
                    turn = False
                #Restart Logic
                if (gameLose or gameWin or gameDraw) and restartButton.collidepoint(pos):
                    #count points
                    acum=0
                    if gameWin:
                        for i,domino in enumerate(player2_hand):
                            acum=acum+domino[0]+domino[1]
                        yourScore=yourScore+acum
                        for i,domino in enumerate(player4_hand):
                            acum=acum+domino[0]+domino[1]
                        yourScore=yourScore+acum
                    else:
                        for i,domino in enumerate(player1_hand):
                            acum=acum+domino[0]+domino[1]
                        rivalScore=rivalScore+acum
                        for i,domino in enumerate(player3_hand):
                            acum=acum+domino[0]+domino[1]
                        yourScore=yourScore+acum
                    round=0
                    writeText('scores')
                    writeText(str(yourScore))
                    writeText(str(rivalScore))
                    #set game again
                    dominoes = []
                    for i in range(7):
                        for j in range(i, 7):
                            dominoes.append((i, j))

                    random.shuffle(dominoes)
                    player_hand = dominoes[:7]
                    computer_hand = dominoes[7:14]
                    board = [dominoes[14]]
                    dominoes = dominoes[15:28]
                    writeText('your turn')
                    writeAll()
                    turn = False
                    gameWin = False
                    gameLose = False
                    gameDraw = False 
                #quit logic                   
                if (gameLose or gameWin or gameDraw) and quitButton.collidepoint(pos):
                    game_over = True
                    pygame.quit()

    # draw the board
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, (100, 100, 600, 400), 2)
    pygame.draw.rect(screen, BLACK, (150, 150, 500, 300), 2)

    # draw the player1's hand
    for i, domino in enumerate(player1_hand):
        x = 150 + i * 50
        y = 450
        pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)
        text = font.render(f"{domino[0]}-{domino[1]}", True, BLACK)
        screen.blit(text, (x + 5, y + 5))

    # draw the player2's hand
    for i, domino in enumerate(player2_hand):
        x = 650
        y = 150 + i * 42
        pygame.draw.rect(screen, WHITE, (x, y, 60, 40))
        pygame.draw.rect(screen, BLACK, (x, y, 60, 40), 2)

    # draw the player3's hand
    for i, domino in enumerate(player3_hand):
        x = 150 + i * 50
        y = 90
        pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)

    # draw the player4's hand
    for i, domino in enumerate(player4_hand):
        x = 90
        y = 150 + i * 42
        pygame.draw.rect(screen, WHITE, (x, y, 60, 40))
        pygame.draw.rect(screen, BLACK, (x, y, 60, 40), 2)

    # draw the board
    if len(board)>0:
        for i, domino in enumerate(board):
            x = 350+(len(board)-1)*40 - i * 50
            y = 300
            pygame.draw.rect(screen, WHITE, (x, y, 40, 60))
            pygame.draw.rect(screen, BLACK, (x, y, 40, 60), 2)
            text = font.render(f"{domino[1]}-{domino[0]}", True, BLACK)
            screen.blit(text, (x + 5, y + 5))

    #Pass button
    passText = font.render('Pasar',True,BLACK)
    passButton = pygame.Rect(650,520,100,50)
    pygame.draw.rect(screen,WHITE,passButton)
    pygame.draw.rect(screen,BLACK,passButton,2)
    screen.blit(passText,(668,535))

    #PlayRright button
    PlayRrightText = font.render('Jugar derecha',True,BLACK)
    PlayRrightButton = pygame.Rect(450,520,180,50)
    pygame.draw.rect(screen,WHITE,PlayRrightButton)
    pygame.draw.rect(screen,BLACK,PlayRrightButton,2)
    screen.blit(PlayRrightText,(468,535))

    #PlayLeft button
    PlayLeftText = font.render('Jugar izquierda',True,BLACK)
    PlayLeftButton = pygame.Rect(250,520,190,50)
    pygame.draw.rect(screen,WHITE,PlayLeftButton)
    pygame.draw.rect(screen,BLACK,PlayLeftButton,2)
    screen.blit(PlayLeftText,(268,535))

    #Win and lose labels
    winLabel = font.render("GANASTE!!!",True,(255,255,255))
    loseLabel = font.render("PERDISTE...",True,(255,25,255))

    #Check if win
    if len(player1_hand)==0 or len(player3_hand)==0:
        screen.blit(winLabel,(350,30))
        gameWin = True
    if len(player2_hand) ==0 or len(player4_hand)==0:
        screen.blit(loseLabel,(350,30))
        gameLose = True

    #show scores
    yourScoreText = font.render('Tus puntos: '+str(yourScore),True,BLACK)
    rivalScoreText = font.render('Puntos del rival: '+str(yourScore),True,BLACK)
    screen.blit(yourScoreText,(600,10))
    screen.blit(rivalScoreText,(600,30))

    #restart window
    window = pygame.Rect(250,200,300,150)
    restartButton = pygame.Rect(275,275,100,50)
    quitButton = pygame.Rect(425,275,100,50)
    restartText = font.render('Desea jugar otra ronda?',True,BLACK)
    yesText = font.render('Si',True,WHITE)
    noText = font.render('NO',True,WHITE)

    #show restart window
    if gameWin or gameLose or gameDraw:  
        pygame.draw.rect(screen,WHITE,window)
        pygame.draw.rect(screen,BLUE,window,2)
        pygame.draw.rect(screen,BLUE,restartButton)
        pygame.draw.rect(screen,RED,quitButton)
        screen.blit(restartText,(275,210))
        screen.blit(yesText,(310,290))
        screen.blit(noText,(460,290))

    # update the display
    pygame.display.update()

    #Receive game information
    if (not turn)  or gameWin or gameLose:
        text=read()
        if text == 'your turn' or text == ('update'+str(round)):
            
            if text == 'your turn': 
                turn=True
            player1_handReady = False
            player2_handReady = False
            player3_handReady = False
            player4_handReady = False
            boardReady = False
            ready = False
            while not ready:
                text=read()
                match text[0]:
                    case 'b':
                        text=text.replace('b','')
                        board=json.loads(text)
                        boardReady = True
                    case 'u':
                        text=text.replace('u','')
                        player4_hand=json.loads(text)
                        player4_handReady = True
                    case 'd':
                        text=text.replace('d','')
                        player1_hand=json.loads(text)
                        player1_handReady = True
                    case 't':
                        text=text.replace('t','')
                        player2_hand=json.loads(text)
                        player2_handReady = True
                    case 'c':
                        text=text.replace('c','')
                        player3_hand=json.loads(text)
                        player3_handReady = True
                if player1_handReady and player2_handReady and player3_handReady and player4_handReady and boardReady:
                    ready=True
                    writeText('update'+str(round))
                    writeAll()
        elif text=="pass":
            text=read()
            contPass=int(text)
            if contPass==4:
                gameDraw = True
    # limit the frame rate
    clock.tick(60)

# quit Pygame
#pygame.quit()