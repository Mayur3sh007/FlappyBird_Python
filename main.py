import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import *     # Basic pygame imports

# Global Variables for the game
FPS = 32                            #Frames per Sec to make game smoother
SCREENWIDTH = 289                   #Set on the basis of trail & error so that we get a display suitable for phone
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  #Initalise screen witdth & height
GROUNDY = SCREENHEIGHT * 0.8  #We giving 80% of Screen Height to GroundY
#Importing display,sounds, player icons etc
GAME_SPRITES = {}  
GAME_SOUNDS = {}    
PLAYER = 'gallery/sprites/bird.png'             
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    #Shows welcome images on the screen & we R blitting only in integers for simplicity
    playerx = int(SCREENWIDTH/2.3)  #Bird's x position is screen width /2.3 (This 2.3 I got from Experimenting birds position to my desired postion)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/3)   # to get it to center heightwise
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)   # to get it to center widthwise
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():     #pygame.event.get() --> records users response on keyboard

            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE): # KEYDOWN means if any key is pressed and if that key (K_ESCAPE)  is Ecape key then
                pygame.quit()   #quit game
                sys.exit()      #exit program

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP): #if key is pressed and its SPACEBAR or UP key then
                return #Goes to our main def_innit function and then proceeds to execute mainGame() function
            
            else:   #Display our Welcome Scrren
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    

                pygame.display.update() #unitl this function runs our Screen wont display
                FPSCLOCK.tick(FPS)      #TO limit/control our FPS

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)  #Our bird's position on X after starting game
    playery = int(SCREENWIDTH/2)  #Our bird's position on Y after starting game(I have set diff position of bird on welcome screen & on starting game coz of design)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}, 
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0: #While bird is flying
                    playerVelY = playerFlapAccv  #Normal vel on Y axis becomes Acclerated
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()  #play sounds of flapping & this 'wing' is intialised in our main def


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed & isCollide is created further in our COde
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2  #we are getting center of bird(on X axis) by --> CurrentBirdPosition + BirdWidth/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2      #Get center of Pipe(on X axis)
            if pipeMidPos <= playerMidPos < pipeMidPos +4: #if center of our Bird is between Pipe's Center & Pipe's Center + or - 4 then we give a point
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY < playerMaxVelY and not playerFlapped:  
            playerVelY += playerAccY  #So bird Falls faster

        if playerFlapped:
            playerFlapped = False       #False bocz--->if player presses key again then it will agaian Bcome True so this func will again Start/Run---> inshort we keep checking if Player is still pressing UP/SPACE keys0
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)#only make bird fly(increase playery position) when player is not on GND
#how min works--> if GROUNDY[totalHeight-ground Height] - playerHeight - player's y pos  = 0[there's no height left betn bird and ground] then the minimum betn this and playerVelY becomes zero  --> So bird's y position doesnt change --->So it doesnt fly

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):   #zipping is like combining0
            upperPipe['x'] += pipeVelX  #goes to left(as we have put vel as -ve in earlier declaration) with pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width(): #if pipe's x location goes beyond negative(out towards left of screen) i.e becomes -ve of PipeWidth 
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Blitting Display resources
        SCREEN.blit(GAME_SPRITES['background'], (0, 0)) #Blit from origins
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]       #To display Score-->list(str(score) = 21 BECOMES 2 1 --> so we can use Images of Digits
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2  #W ecreate a new Variable To get position to center the Digits(in terms of X)

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25  or playery < 0:
#Player either touches Ground[-25 is around height of our bird so it only registers when our bird is really in contact with Ground & not when its near the ground] OR if player goes in -ve hieght[Player goes above ceiling of Screen]
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()): 
#if birds yPosition is less than (pipeHeight+pipes y position) & (players x postion-pipes x position) is less than pipe width [that is if birds on left side of pipe means its crashed into it)
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes: # reversed Logic for Straight Pipe
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False  #By default if above cases R not true then player has not collided

def getRandomPipe():
    #Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3.5#The certain amt of space(is futher used to decide how much space we leave between 2 pair of pipes) --->Increase this to decrease the space between 2 obstacles
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset)) #BottomPipe-->height = offset+randomNumber from 0 to(totalScreen-GroundIMG-alittleMoreSpace than offset)
    pipeX = SCREENWIDTH + 10   #SO pipe is not immediately on screen when game starts we start creating pipes at this distance && X is same for both pipes
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper/Reversed Pipe
        {'x': pipeX, 'y': y2} #lower/Straight Pipe
    ]
    return pipe





 #Main Func 
if __name__ == "__main__": #def init 
    # This will be the main point from where our game will start

    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()  #To control FPS 

    pygame.display.set_caption('Flappy Bird')

    #Game Images---> we create Dictionaries of Game sprites with info stored in the Tuples of Dictionaries

    GAME_SPRITES['numbers'] = (        #here game sprite's numbers are a tuple and so we insert all our numbers pmh in them
        
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),  #convert_alpha is a func for fast rendering/loading images in our game
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
     #We firstly display PIPE normally then --> we rotated our pipe image by 180deg & rendered it --> this is all in a Single Tuple of our PIPE Dictionary
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
                           pygame.image.load(PIPE).convert_alpha()
                           )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()  #Only focuses on Image pixelsnot its transparency(aplha)
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()     #focuses on both aspects

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
