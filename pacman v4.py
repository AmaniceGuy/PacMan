'''Author: James Wang
    Date Last Updated: May 28, 2019
    Controls: Arrow keys, Space Bar to start game
    Description: Basic recreation of Pacman game. When the ghosts die, 
    they will teleport back to the center box. The game ends when the player
    has lost all their lives (3) or eaten all the pellets. Eating a fruit or
    a large pellet grants you the ability to eat the ghosts (indicated by a change
    in colour. The all scores are stored in "highscore.txt".
    The game includes a special "glitch"
    
'''
#IMPORT / INITIALIZE    
import pygame
import random
import classes4 as classes
pygame.init()
pygame.mixer.init()

def setEdible(ghosts,isOrNot,player,walls):
    '''This function sets the ghosts to edible or not edible, depending
        on the isOrNot parameter'''
    if isOrNot:
        for ghost in ghosts:
            ghost.setIsEdible()
            ghost.think(player,walls)
    else:
        for ghost in ghosts:
            ghost.setNotEdible()
            ghost.think(player,walls)
        
def menu(highscore,score):
    '''This function displays the Pacman game menu, and it returns either
        True or False. True if they want to play, and False if they want to exit.
        It takes the highscore and as a parameter and displays them on the screen.'''
    #Display
    screen = pygame.display.set_mode((480,640))
    pygame.display.set_caption("Pacman")

    #ENTITIES
    #E - Background
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    #E - Logo
    logo = pygame.image.load("images\Menu\pacman_logo.png")
    logoPos = ((screen.get_width() - logo.get_width())//2,100)
    #E - Text
    smallFont = pygame.font.Font("Fonts\emulogic.ttf",10)
    font = pygame.font.Font("Fonts\emulogic.ttf",20)
    largeFont = pygame.font.Font("Fonts\emulogic.ttf",25)
    highscoreText = largeFont.render("HIGHSCORE",True,(255,255,255))
    scoreText = largeFont.render("YOUR SCORE",True,(255,255,255))
    highscore = font.render(str(highscore),True,(255,255,255))
    score = font.render(str(score),True,(255,255,255))
    start = smallFont.render("PRESS SPACE TO START",True,(255,255,255))

    #E - Surface for all the text
    message = pygame.Surface((480,200))
    message.blit(highscoreText,((480-highscoreText.get_width())//2,0))
    message.blit(highscore,((480-highscore.get_width())//+2,40))
    message.blit(scoreText,((480-scoreText.get_width())//2,80))
    message.blit(score,((480-score.get_width())//2,120))
    message.blit(start,((480-start.get_width())//2,180))
    block = pygame.Surface((480,60))
    block.fill((0,0,0))
    #ACTION
    #A - Assign
    clock = pygame.time.Clock()
    run = True
    flash = 0

    #A - LOOP
    while run:
        #L - Time
        clock.tick(30)

        #L - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playGame = False
            #Player presses space to start the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    playGame = True

        #L - Reresh screen
        screen.blit(background,(0,0))
        screen.blit(logo,logoPos)
        screen.blit(message,(0,400))
        #Flashing text and Refreshing the screen
        flash += 1
        if flash == 20:
            flash = 0
        if flash <= 7:
            screen.blit(block,(0,580))
        pygame.display.flip()
    
    #A - Return playGame to tell main() to play game or not
    return playGame
    
def getGhosts(screen,x,y):
    '''This function returns a list of all the ghosts'''
    #Create a list of ghosts
    ghosts = []
    #Create lists of images for each ghost
    blinky = []
    pinky = []
    inky = []
    clyde = []
    #Load images into each list
    ghostNames = [r"Sprites\Ghosts\blinky","Sprites\Ghosts\pinky","Sprites\Ghosts\inky","Sprites\Ghosts\clyde"]
    directions = ["_right","_up","_left","_down"]
    for ghost in ghostNames:
        if ghost == r"Sprites\Ghosts\blinky":
            for direction in directions:
                blinky.append([pygame.image.load(ghost + direction + ".png"),pygame.image.load(ghost + direction + "_2.png")])
        elif ghost == "Sprites\Ghosts\pinky":
            for direction in directions:
                pinky.append([pygame.image.load(ghost + direction + ".png"),pygame.image.load(ghost + direction + "_2.png")])
        elif ghost == "Sprites\Ghosts\inky":
            for direction in directions:
                inky.append([pygame.image.load(ghost + direction + ".png"),pygame.image.load(ghost + direction + "_2.png")])
        elif ghost == "Sprites\Ghosts\clyde":
            for direction in directions:
                clyde.append([pygame.image.load(ghost + direction + ".png"),pygame.image.load(ghost + direction + "_2.png")]) 
    #Add 4 Ghosts to ghosts
    ghosts.append(classes.Ghost("Blinky",blinky,x,y,screen))
    ghosts.append(classes.Ghost("Pinky",pinky,x+20,y,screen))
    ghosts.append(classes.Ghost("Inky",inky,x+40,y,screen))
    ghosts.append(classes.Ghost("Clyde",clyde,x+60,y,screen))
    return ghosts
        
def getPellets(xOffset,yOffset):
    '''This function returns a list of all the small pellets'''
    #Create a list to store pellets
    pellets = []
    #Add pellet to pellets based on the position of pellets in pelletPos
    pelletPos = pygame.image.load("Images\MazeElements\small_pellets.png")
    for x in range(22,pelletPos.get_width(),4):
        for y in range(2,pelletPos.get_height(),4):
            if pelletPos.get_at((x,y)) != (0,0,0):
                pellets.append(classes.Pellet(x+xOffset,y+yOffset))    
    return pellets

def checkTurn(entity,walls):
    '''This function returns if entity can move in the desired direction'''
    entity.move = True
    offsets = [(1,0),(0,-1),(-1,0),(0,1),(0,0)]
    entity.rect.centerx += offsets[entity.nextDir][0]
    entity.rect.centery += offsets[entity.nextDir][1]
    hit = pygame.sprite.spritecollide(entity,walls,False)
    entity.rect.centerx -= offsets[entity.nextDir][0]
    entity.rect.centery -= offsets[entity.nextDir][1]
    if not hit:
        entity.setDir(entity.nextDir)
    return not(hit)
    
def game():
    '''This function is the main game function. It takes no parameters and
        returns the player's score if they lose all their lives or eat all the
        pellets. Returns False if they want to exit the game'''
    #Game function
    #Display
    screen = pygame.display.set_mode((480,640))
    pygame.display.set_caption("Pacman")
    
    #Entities
    #Maze
    maze = pygame.image.load(r"Images\MazeElements\blank_maze.png")
    mazeYOffset = (screen.get_height() - maze.get_height() ) // 2
    mazeXOffset = (screen.get_width() - maze.get_width() ) // 2
    
    #Background
    background = pygame.Surface(screen.get_size())
    background.blit(maze,(mazeXOffset,mazeYOffset))

    #Sprites
    #S - Player
    player = classes.Pacman(screen.get_width()//2,mazeYOffset + 390,screen)
    
    #S - Ghosts
    ghosts = getGhosts(screen,mazeXOffset+178,mazeYOffset+210)

    #S - Pellets
    pellets = pygame.sprite.Group(getPellets(mazeXOffset,mazeYOffset))
    
    #S - Large Pellets
    largePellets = []
    for xy in [(16,50),(416,50),(16,370),(416,370)]:
        largePellets.append(classes.Fruit(xy[0]+mazeXOffset,xy[1]+mazeYOffset,\
                      "Large Pellet",pygame.image.load("Images\MazeElements\largePellet.png"),screen))
    largePellets = pygame.sprite.Group(largePellets)
    
    #S - Fruits
    fruitX, fruitY = screen.get_width()//2,mazeYOffset + 389
    fruitImages = [pygame.image.load("Sprites\Fruits\cherry.png"),\
                   pygame.image.load("Sprites\Fruits\strawberry.png")]
    fruitNames = ["Cherry","Strawberry"]
    fruit = False

    #S - Walls
    walls = []
    door = classes.Door(mazeXOffset+208,mazeYOffset+198)
    wallArea = pygame.image.load("Images\MazeElements\walls.png")
    for x in range(wallArea.get_width()):
        for y in range(wallArea.get_height()):
            if wallArea.get_at((x,y)) != (0,0,0):
                walls.append(classes.Wall(x + mazeXOffset,y + mazeYOffset))
    walls.append(door)
    scoreKeeper = classes.scoreKeeper(screen)

    #S - Create a group for all sprites
    allSprites = pygame.sprite.OrderedUpdates(pellets,largePellets,ghosts,\
                                              scoreKeeper,player,door)

    #Sound Effects
    eatFruit = pygame.mixer.Sound("Sounds\pacman_eatfruit.wav")
    eatGhost = pygame.mixer.Sound("Sounds\pacman_eatghost.wav")
    loseLife = pygame.mixer.Sound("Sounds\pacman_death.wav")
    loseLife.set_volume(0.5)
    eatPellet = pygame.mixer.Sound("Sounds\pacman_chomp.wav")
                       
    #Action
    #Assign
    playGame = True
    ghostCount = 60
    fruitCount = 299
    edibleCount = 0
    ghostEatCount = 0
    glitch = False
    clock = pygame.time.Clock()

    #main game loop  
    while playGame:
        
        clock.tick(30)

        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playGame = False
                return False
            #Player movement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.nextDir = 0
                if event.key == pygame.K_UP:
                    player.nextDir = 1
                if event.key == pygame.K_LEFT:
                    player.nextDir = 2
                if event.key == pygame.K_DOWN:
                    player.nextDir = 3

        #Check if the game is over (player had no more lives
        #or all the pellets have been eaten
        if not(pellets) or scoreKeeper.lives <= 0:
            playGame = False
        #decrease the amount of time the ghosts are edible
        elif edibleCount:
            edibleCount -= 1
            if edibleCount == 1:
                setEdible(ghosts,False,player,walls)
        #glitch
        elif scoreKeeper.lives == 4:
            walls = [classes.Wall(0,0)]
            glitch = True
            ghosts = ghosts + getGhosts(screen,random.randrange(240),random.randrange(630))
            allSprites = pygame.sprite.OrderedUpdates(pellets,largePellets,ghosts,scoreKeeper,player,door)
            for ghost in ghosts:
                ghost.vel = 3
                ghost.think(player,walls)
            player.vel = 3
            
        #Ghost leaves box after 2 seconds and randomly goes left or right
        if ghostCount > 0:
            ghostCount -= 1
        #ghosts leave box
        elif ghostCount == 0:
            #Set ghostCount to -1 so the code doesn't run
            ghostCount -= 1  
            #Door opens
            door.open()
            for ghost in ghosts:
                ghost.leaving = True
                ghost.think(player,walls)
        #if all the ghosts have left, close the door
        elif ghostCount == -1:
            inBox = []
            for ghost in ghosts:
                inBox.append(not(ghost.inBox))
            if all(inBox):
                door.close()
                ghostCount -= 1
                
        #Spawning fruits 10 seconds after one is eaten     
        if fruitCount in range(1,300):
            fruitCount -= 1
        #after an interval of time, spawn another fruit
        elif not(fruitCount):
            fruitCount = 300
            fruitNum = random.randrange(2)
            fruit = classes.Fruit(fruitX,fruitY,fruitNames[fruitNum],\
                                        fruitImages[fruitNum],screen)
        #Eating fruit
        elif fruit:
            if player.rect.colliderect(fruit.rect):
                eatFruit.play()
                scoreKeeper.playerScore(fruit.getValue())
                fruit = False
                edibleCount = 240
                fruitCount -= 1
                setEdible(ghosts,True,player,walls)

        #Check to see if Pacman has hit a ghost
        hitGhost = pygame.sprite.spritecollide(player,ghosts,False)
        if hitGhost:
            #if he can eat them
            for ghost in hitGhost:
                if ghost.edible:
                    eatGhost.play()
                    scoreKeeper.playerScore(50*(2**ghostEatCount))
                    ghost.reset()
                    ghostCount = 60
                    ghostEatCount += 1
                    if not(edibleCount):
                        ghostEatCount = 0
                #If he cannot eat them
                else:
                    loseLife.play()
                    scoreKeeper.playerLoseLife()
                    player.reset()
                    fruitCount = 299
                    fruit = False
                    
        #Update positions of sprites contained in allSprites
        allSprites.clear(screen,background)
        allSprites.update()
        screen.blit(background,(0,0))
        
        #Check to see if Pacman can turn (won't run into a wall)
        checkTurn(player,walls)

        #Check if the player has eaten a pellet
        if pygame.sprite.spritecollide(player,pellets,True):
            eatPellet.play()
            scoreKeeper.playerScore(1)
        #check if the player has eaten a large pellet
        elif pygame.sprite.spritecollide(player,largePellets,True):
            eatFruit.play()
            scoreKeeper.playerScore(50)
            edibleCount = 240
            setEdible(ghosts,True,player,walls)
        #Check if the player has hit a wall
        elif pygame.sprite.spritecollide(player,walls,False):
            player.stop(walls)
        #glitch feature
        elif player.rect.center == (240,10) or player.rect.center == (240,630):
            scoreKeeper.lives += 1
            scoreKeeper.playerScore(1000)
                
        #Make ghost move in new direction
        for ghost in ghosts:
            if glitch:
                ghost.think(player,walls)
            if ghost.nextDir != 5:
                checkTurn(ghost,walls)
            if ghost.checkInBox() and ghost.leaving:
                if ghost.rect.left == mazeXOffset + 210 :
                    ghost.setDir(1)
            elif ghost.getIsEqual(player) or\
                pygame.sprite.spritecollide(ghost,walls,False):
                ghost.stop(walls)
                ghost.think(player,walls)
        
        #Refresh the screen
        if fruit:
            fruit.draw()
        allSprites.draw(screen)
        pygame.display.flip()
        
    #Return the player's score
    return scoreKeeper.getScore()
    
def main():
    '''This is the main function for the program'''
    #Action
    run = True
    highscore = 0
    file = open("highscore.txt","r")
    #Open the highscores file
    for line in file:
        score = int(line.strip())
        if score > highscore:
            highscore = score
    file = open("highscore.txt","a")
    #Background Music
    pygame.mixer.music.load(r"Sounds\theme.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    
    #Loop
    while run:
        if menu(highscore,score):
            score = game()
            file.write(str(score)+"\n")
            if score > highscore:
                highscore = score
        else:
            run = False
        if not(score):
            run = False
            
    #close and save the new highscore
    #then exit pygame
    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(2000)
    file.close()
    pygame.quit()

main()
