'''Author: James Wang
    Last Updated on: May 28, 2019
    Description: Class module for pacman game. Contains all classes
'''

import pygame
import subprocess
import random
##subprocess.call([r'E:\Pacman\matrix.bat'])
pygame.init()

class Wall(pygame.sprite.Sprite):
    '''This class defines the wall Sprite'''
    def __init__(self,x,y):
        '''Initializer function for wall class'''
        #Call parent __init__ function
        pygame.sprite.Sprite.__init__(self)
        #Create surface and rect object and position it on the screen
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

class Door(pygame.sprite.Sprite):
    '''This subclass defines the Door Sprite'''
    def __init__(self,x,y):
        '''Initializer function for door class'''
        #Call parent __init__ function
        Wall.__init__(self,x,y)
        #Create surface and rect object
        self.image = pygame.Surface((32,10))
        self.image.fill((255,255,255))
        #Instance variables
        self.opening = False
        self.closing = False

    def open(self):
        '''This function opens the door'''
        self.opening = True

    def close(self):
        '''This function closes the door'''
        self.closing = True

    def update(self):
        '''This function updates the position of the sprite'''
        if self.opening:
            self.rect.left -= 1
            if self.rect.right <= 185:
                self.opening = False
        elif self.closing:
            self.rect.left += 1
            if self.rect.centerx >= 226:
                self.closing = False
                self.rect.centerx = 226
                  
class Pellet(pygame.sprite.Sprite):
    '''This class defines the Pellet class'''
    def __init__(self,x,y):
        '''Initializer function for the Pellet class'''
        #Call parent __init__ function
        pygame.sprite.Sprite.__init__(self)
        #Create surface and rect object
        self.image = pygame.Surface((4,4))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        #Position pellet
        self.rect.top = y
        self.rect.left = x
        #Its point value
        self.points = 1

    def getValue(self):
        '''This function returns the value of the Pellet'''
        return self.points

class Fruit(Pellet):
    '''This class defines the Fruit class'''
    def __init__(self,x,y,name,image,screen):
        '''Initialzer function for the fruit class'''
        #Call parent __init__ function
        Pellet.__init__(self,0,0)
        #Create surface and rect object
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        #Reposition fruit
        self.rect.centerx = x
        self.rect.bottom = y
        self.name = name
        #Set its point value based on what fruit it is
        if name == "Cherry":
            self.points = 100
        elif name == "Strawberry":
            self.points = 150
        else:
            self.points = 50
            self.rect.topleft = (x,y)

    def draw(self):
        '''This function draws the fruit image on the screen'''
        self.screen.blit(self.image,(self.rect.left,self.rect.top))
        
class Entity(pygame.sprite.Sprite):
    '''This class defines the Entity class, and is the general class used
    for all sprites with dynamic movement'''
    def __init__(self,name,x,y,screen):
        '''Initalizer function for the entity class'''
        #Call parent __init__ function
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        #Create rect object
        self.rect = self.image.get_rect()
        #Declare instance variables
        self.imageCount = 0
        self.name = name
        self.vel = 2
        self.dir = 3
        self.nextDir = 0
        self.isMove = True
        #Declare integer for each direction
        self.right, self.up,self.left,self.down = 0,1,2,3
        
    def setDir(self,dirNum):
        '''This function takes 1 integer parameter that represents
        1 of 4 directions and sets the entity's direction to that value'''
        self.dir = dirNum
        self.isMove = True

    def stop(self,walls):
        '''This function stops the entity when it collides with a wall'''
        self.isMove = False
        for i in range(3):
            if pygame.sprite.spritecollide(self,walls,False):
                if self.dir == 0:
                    self.rect.centerx -= 1
                elif self.dir == 1:
                    self.rect.centery += 1
                elif self.dir == 2:
                    self.rect.centerx += 1
                elif self.dir == 3:
                    self.rect.centery -= 1

    def update(self):
        '''This function updates the position and image of the sprite'''
        #Cycle the sprite image
        self.changeImage()
        #reposition the sprite
        if self.isMove:
            if self.dir == 0:
                self.rect.centerx += self.vel
            elif self.dir == 1:
                self.rect.centery -= self.vel
            elif self.dir == 2:
                self.rect.centerx -= self.vel
            elif self.dir == 3:
                self.rect.centery += self.vel

        #if the player leaves the screen, they will appear on the opposite side
        if self.rect.left >= self.screen.get_width():
           self.rect.right = 0
        elif self.rect.right <= 0:
            self.rect.left = self.screen.get_width()
        elif self.rect.bottom <= 0:
            self.rect.top = self.screen.get_height()
        elif self.rect.top >= self.screen.get_height():
            self.rect.bottom = 0
              
class Ghost(Entity):
    '''This class defines the Ghost class. It inherits from the Entity class'''
    def __init__(self,name,images,x,y,screen):
        '''Initialzer function for the Ghost class'''
        #Load images
        self.default = images
        self.images = self.default
        self.blue = [pygame.image.load(r"Sprites\Ghosts\blue.png"),\
                     pygame.image.load(r"Sprites\Ghosts\blue_2.png")]
        self.white = [pygame.image.load("Sprites\Ghosts\white.png"),\
                      pygame.image.load("Sprites\Ghosts\white_2.png")]
        self.image = self.images[0][0]
        #Call parent __init__ function
        Entity.__init__(self,name,None,None,screen)
        #Position Ghost
        self.startPos = (x,y)
        self.rect.topleft = (x,y)
        self.ghostBox = y
        #Declare instance variables
        self.offsets = [(1,0),(0,-1),(-1,0),(0,1),(0,0)]
        self.dir = 0
        self.leaving = False
        self.move = False
        self.inBox = True
        self.nextDir = 5
        self.wasEqual = False
        self.edible = False

    def getIsEqual(self,player):
        '''This function returns if the ghost has the same
            y or x as the player'''
        if self.rect.centerx == player.rect.centerx or\
           self.rect.centery == player.rect.centery:
            if self.wasEqual:
                return False
            else:
                self.wasEqual = True
                return True
        else:
            self.wasEqual = False
            return False
        
    def changeImage(self):
        '''This function cycles the ghost images'''
        self.imageCount += 1
        if self.imageCount == 2:
            self.imageCount = 0
        if not self.edible:
            self.image = self.images[self.dir][self.imageCount]
        else:
            self.edible -= 1
            if self.edible <= 60:
                if self.imageCount == 1:
                    self.image = self.white[self.imageCount]
                    return
                else:
                    pass
            self.image = self.blue[self.imageCount]
            
    def reset(self):
        '''This function resets all the instance variables to their default values'''
        self.rect.topleft = self.startPos
        self.setNotEdible()
        self.leaving = False
        self.move = False
        self.inBox = True
        self.nextDir = 5
        
    def leaveBox(self):
        '''This function defines the behaviour of the ghost when it is
        leaving the box'''
        if self.rect.centerx > self.screen.get_width()//2:
            self.setDir(self.left)
        elif self.rect.centerx < self.screen.get_width()//2:
            self.setDir(self.right)

    def setIsEdible(self):
        '''This function makes the ghosts run away from pacman'''
        self.right,self.up,self.left,self.down = 2, 3, 0,1
        self.vel = 1
        self.edible = 300

    def setNotEdible(self):
        '''This function makes the ghosts not edible'''
        self.right,self.up,self.left,self.down = 0,1,2,3
        self.edible = 0
        self.vel = 2
        
    def checkInBox(self):
        '''This function checks if the ghost is inside the ghost box
        and returns the result'''
        if self.rect.bottom < self.ghostBox - 10:
            self.inBox = False
        return self.inBox

    def think(self,player,walls):
        '''This function sets the direction and next direction of the
        ghost based on the position of the player and walls'''
        if self.checkInBox():
            if self.leaving:
                self.leaveBox()
                return
            else:
                self.setDir(random.randrange(4))
                return
        else:
            if self.leaving:
                self.setDir(random.randrange(0,3,2))
                self.leaving = False
                return

        #Set the directions it cannot go    
        self.invalids = []
        self.move = True
        for offset in self.offsets:
            self.rect.centerx += offset[0]
            self.rect.centery += offset[1]
            if pygame.sprite.spritecollide(self,walls,False):
                self.invalids.append(self.offsets.index(offset))
            self.rect.centerx -= offset[0]
            self.rect.centery -= offset[1]
            
        #Choosing direction - Basic
        if self.rect.centerx > player.rect.centerx and self.left not in self.invalids:
            self.setDir(self.left)
            if self.rect.top > player.rect.top:
                self.nextDir = self.up
            elif self.rect.top < player.rect.top:
                self.nextDir = self.down
        elif self.rect.centerx < player.rect.centerx and self.right not in self.invalids:
            self.setDir(self.right)
            if self.rect.top > player.rect.top:
                self.nextDir = self.up
            elif self.rect.top < player.rect.top:
                self.nextDir = self.down
        elif self.rect.centery > player.rect.centery and self.up not in self.invalids:
            self.setDir(self.up)
            if self.rect.left > player.rect.left:
                self.nextDir = self.left
            elif self.rect.left < player.rect.left:
                self.nextDir = self.right
        elif self.rect.centery < player.rect.centery and self.down not in self.invalids:
            self.setDir(self.down)
            if self.rect.left > player.rect.left:
                self.nextDir = self.left
            elif self.rect.left < player.rect.left:
                self.nextDir = self.right
        
        #Choosing direction - 1 vertical Obstacle
        elif self.rect.centerx != player.rect.centerx\
            and self.rect.centery == player.rect.centery:
                
            if self.rect.centerx > player.rect.centerx:
                self.nextDir = self.left
            elif self.rect.centerx < player.rect.centerx:
                self.nextDir = self.right
                    
            if self.up in self.invalids:
                self.setDir(self.down)
            elif self.down in self.invalids:
                self.setDir(self.up)
            else:
                self.setDir(random.randrange(1,4,2))
                
        #Choosing direction - 1 horizontal Obstacle
        elif self.rect.centery != player.rect.centery\
              and self.rect.centerx == player.rect.centerx:
            
            if self.rect.centery > player.rect.centery:
                self.nextDir = self.up
            elif self.rect.centery < player.rect.centery:
                self.nextDir = self.down
                
            if self.right in self.invalids:
                self.setDir(self.left)
            elif self.left in self.invalids:
                self.setDir(self.right)
            else:
                self.setDir(random.randrange(0,3,2))
                
        #Choosing direction - L shaped Obstacle, up and to left of player
        elif self.rect.centerx < player.rect.centerx and \
             self.rect.centery < player.rect.centery:   
            if player.dir == player.left or player.dir == player.down:
                self.setDir(self.left)
                self.nextDir = self.up
            else:
                self.setDir(self.up)
                self.nextDir = self.left
                
        #Choosing direction - L shaped Obstacle, up and to right of player
        elif self.rect.centerx > player.rect.centerx and \
             self.rect.centery < player.rect.centery:   
            if player.dir == player.left or player.dir == player.up:
                self.setDir(self.up)
                self.nextDir = self.left
            else:
                self.setDir(self.left)
                self.nextDir = self.up
                
        #Choosing direction - L shaped Obstacle, down and to left of player
        elif self.rect.centerx < player.rect.centerx and \
             self.rect.centery > player.rect.centery:   
            if player.dir == player.left or player.dir == player.up:
                self.setDir(self.left)
                self.nextDir = self.down
            else:
                self.setDir(self.down)
                self.nextDir = self.left
                
        #Choosing direction - L shaped Obstacle, down and to right of player
        elif self.rect.centerx > player.rect.centerx and \
            self.rect.centery > player.rect.centery:   
            if player.dir == player.right or player.dir == player.up:
                self.setDir(self.right)
                self.nextDir = self.down
            else:
                self.setDir(self.down)
                self.nextDir = self.right
        else:
            self.nextDir = random.randrange(4)
            
class Pacman(Entity):
    '''This class defines the Pacman class. It inherits from the Entity class'''
    def __init__(self,x,y,screen):
        '''Initializer function for the Pacman class'''
        #Load its images
        self.images = [[pygame.image.load(r"Sprites\Pacman\right_half_open.png"),pygame.image.load(r"Sprites\Pacman\right_open.png")],\
                       [pygame.image.load(r"Sprites\Pacman\up_half_open.png"),pygame.image.load(r"Sprites\Pacman\up_open.png")],\
                       [pygame.image.load("Sprites\Pacman\left_half_open.png"),pygame.image.load("Sprites\Pacman\left_open.png")],\
                       [pygame.image.load("Sprites\Pacman\down_half_open.png"),pygame.image.load("Sprites\Pacman\down_open.png")]] 
        #Create surface
        self.image = pygame.Surface((28,28))
        self.image0 = pygame.image.load("Sprites\Pacman\mouth_closed.png")
        self.image.blit(self.image0,(2,2))
        #Call parent __init__ function
        Entity.__init__(self,"Pacman",x,y,screen)
        #Position pacman
        self.startPos = (x,y)
        self.rect.centerx = x
        self.rect.bottom = y

    def changeImage(self):
        '''This function cycles the image of the Pacman sprite, so it appears
        he is opening and closing his mouth'''
        self.image = pygame.Surface((28,28))
        if self.imageCount > 3:
            self.imageCount = 0
            
        if self.imageCount == 0:
            self.image.blit(self.image0,(2,2))
        elif self.imageCount == 1 or self.imageCount == 3:
            self.image.blit(self.images[self.dir][0],(2,2))
        elif self.imageCount == 2:
            self.image.blit(self.images[self.dir][1],(2,2))
        self.imageCount += 1

    def reset(self):
        '''This function resets the direction and positin of Pacman to the
        default'''
        self.rect.centerx, self.rect.bottom = self.startPos
        self.dir = 3
        self.nextDir = 0
        self.move = True

class scoreKeeper(pygame.sprite.Sprite):
    '''This class defines the scoreKeeper class'''
    def __init__(self,screen):
        '''Initializer function for the scoreKeeper class'''
        #Call parent __init__ class
        pygame.sprite.Sprite.__init__(self)
        #Create surface and rect object and position it on the screen
        self.image = pygame.Surface((screen.get_width(),40))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = screen.get_height() - 40
        #Load fonts and images
        self.font = pygame.font.Font("Fonts\emulogic.ttf",20)
        self.heart = pygame.image.load("Sprites\Scoreboard\heart.png")
        #Declare instance variables
        self.screen = screen
        self.lives = 3
        self.score = 0

    def playerScore(self,points):
        '''This function takes 1 integer value parameter and adds it to
        the player's score'''
        self.score += points

    def playerLoseLife(self):
        '''This function takes away 1 life from the player'''
        self.lives -= 1

    def getScore(self):
        '''This function returns the player's score'''
        return self.score
    
    def update(self):
        '''This function updates what the scoreKeeper class displays'''
        self.image.fill((0,0,0))
        self.text = self.font.render("Score: " + str(self.score),True,(255,255,255))
        self.image.blit(self.text,(0,10))
        for life in range(self.lives):
            self.image.blit(self.heart,(self.screen.get_width()-(life+1)*self.heart.get_width(),5))
