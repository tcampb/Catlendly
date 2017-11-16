import os, sys, random, time
import pygame
from pygame.locals import *
pygame.font.init()


def load_image(file_name):
    image = pygame.image.load(file_name)
    image = image.convert()
    print dir(image)
    return image

def load_fonts(text, size, color):
    font = pygame.font.Font("PressStart2P-Regular.ttf", size)
    space_font = font.render(text, 1, color)
    return space_font


class PyMain(object):

    def __init__(self, width=1439, height=899):
        pygame.init()
        #set window size
        self.width  = width
        self.height = height
        #This function will create a display surface; it will initialize a window or screen for display
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.caption = pygame.display.set_caption("Catlendly")
        self.level = "Intro"
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.stage_background = load_image("catlendly_background.png")
        self.lives = 9

    def MainLoop(self):
        y = 0
        self.time_hit = 0
        self.load_intro_sprites()
        pygame.display.update()
        #Main game loop
        while 1:
            rel_y = y % self.stage_background.get_rect().height
            if self.level == "Intro":
                self.star_sprites.draw(self.screen)
                pygame.display.update()
                self.star_sprites.clear(self.screen, self.background)
                self.star_sprites.empty()
                self.update_intro_background()
            elif self.level == "Character_selection":
                pygame.display.update()
            elif self.level == "Stage_one":

                self.screen.blit(self.stage_background, (20, (rel_y - self.stage_background.get_rect().height)))
                self.load_asteroids()
                if pygame.sprite.spritecollide(self.ship, self.asteroid_sprites, False):
                    self.ship.image = load_image("ship_explosion.png")
                    if self.ship.is_alive:
                        self.lives -= 1
                        self.time_hit = time.time()
                    self.ship.is_alive = False
                if int(self.time_hit + 3) == int(time.time()):
                    self.ship_sprites.empty()
                    self.level = "Stage_one"
                    self.Stage_one(True)
                self.asteroid_sprites.draw(self.screen)
                self.update_asteroids()
                self.ship_sprites.draw(self.screen)
                pygame.display.update()
                y += 1
                if rel_y < 899:
                    self.screen.blit(self.stage_background, (20, rel_y))
            
            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "escape":
                        sys.exit()
                if self.level == "Stage_one":
                    if event.type == pygame.KEYDOWN and self.ship.is_alive:
                            #pygame.draw.rect(pygame.display.get_surface(), (0,0,0), self.ship.rect.copy())
                            self.ship.move(event.key, self.screen_rect)
                elif self.level == "Intro":
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:               
                            self.level = "Character_selection"
                            self.Character_Selection()
                elif self.level == "Character_selection":
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] in range(150, 380) and mouse[1] in range(700, 768):
                        image_group = pygame.sprite.Group(Static_Image('button_success.png', (150, 700, 250, 68)))
                        image_group.draw(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.level = "Stage_one"
                            self.character = "Ship1.png"
                            self.Stage_one(False)
                    elif mouse[0] in range(580, 810) and mouse[1] in range(700, 768):
                        image_group = pygame.sprite.Group(Static_Image('button_success.png', (580, 700, 250, 68)))
                        image_group.draw(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.level = "Stage_one"
                            self.character = "Ship2.png"
                            self.Stage_one(False)
                    elif mouse[0] in range(1010, 1260) and mouse[1] in range(700, 768):
                        image_group = pygame.sprite.Group(Static_Image('button_success.png', (1010, 700, 250, 68)))
                        image_group.draw(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.level = "Stage_one"
                            self.character = "Ship3.png"
                            self.Stage_one(False)
                    else:
                        image_group = pygame.sprite.Group(Static_Image('button_inactive.png', (150, 700, 250, 68)), 
                                                          Static_Image('button_inactive.png', (580, 700, 250, 68)),
                                                          Static_Image('button_inactive.png', (1010, 700, 250, 68)))
                        image_group.draw(self.screen)

    
    def Character_Selection(self):
        #Clear previous surface
        self.screen.fill((0,0,0))
        self.star_sprites.clear(self.screen, self.background)
        self.star_sprites.empty()
        #Load text font and images
        font_choose_pilot = load_fonts("Choose your pilot: ", 50, (255, 255, 255))
        text_name_gotham = load_fonts("Name: Gotham", 30, (255, 255, 255))
        text_name_oakley = load_fonts("Name: Oakley", 30,(255, 255, 255))
        text_name_eva = load_fonts("Name: Eva", 30,(255, 255, 255))
        text_lives = load_fonts("Lives: 9", 30,(255, 255, 255))
        text_ship = load_fonts("Ship: ", 30,(255, 255, 255))
        #Add text to screen 
        self.screen.blit(font_choose_pilot, [25, 25])
        self.screen.blit(text_name_gotham, [95, 470])
        self.screen.blit(text_name_oakley, [525, 470])
        self.screen.blit(text_name_eva, [955, 470])
        self.screen.blit(text_lives, [95, 530])
        self.screen.blit(text_lives, [525, 530])
        self.screen.blit(text_lives, [955, 530])
        self.screen.blit(text_ship, [95, 580])
        self.screen.blit(text_ship, [525, 580])
        self.screen.blit(text_ship, [955, 580])
        #Create Static_Image objects
        static_image_group = pygame.sprite.Group(Static_Image('Cat1.png', (105, 175, 144, 119)),
                                                 Static_Image('Cat2.png', (535, 175, 144, 119)),
                                                 Static_Image('Cat3.png', (965, 175, 144, 119)),
                                                 Static_Image('button_inactive.png', (150, 700, 250, 68)),
                                                 Static_Image('button_inactive.png', (580, 700, 250, 68)),
                                                 Static_Image('button_inactive.png', (1010, 700, 250, 68)),
                                                 Static_Image('Ship1.png', (285, 580, 75, 73)),
                                                 Static_Image('Ship2.png', (710, 580, 75, 73)),
                                                 Static_Image('Ship3.png', (1135, 580, 75, 73))
                                                 )
        #Draw static_image_group to screen
        static_image_group.draw(self.screen)
        pygame.display.update()

    def Stage_one(self, reset): 

        if reset:
            self.ship_sprites = self.LoadSprites(self.character)
            self.ship_sprites.draw(self.screen)
            self.asteroid_sprites.empty()
        else:
            self.screen.fill((0,0,0))
            self.star_sprites.clear(self.screen, self.background)
            self.star_sprites.empty()
            self.ship_sprites = self.LoadSprites(self.character)
            self.ship_sprites.draw(self.screen)
            self.asteroid_sprites = pygame.sprite.Group()
            #pygame.display.update()

                
       
             
    def LoadSprites(self, character):
        #sprite - base class for visible game objects
        self.ship = Ship(character)
        #A container class to hold and manage multiple sprite objects
        #Pass newly created ship object to Group as an arguement
        self.ship_sprites = pygame.sprite.Group(self.ship)
        return self.ship_sprites

    def load_intro_sprites(self):

        font_Catlendly_header = load_fonts("Catlendly", 95, (42, 247, 44))
        font_press_to_start = load_fonts("Press Enter to Start", 30, (255, 255, 255))
        rfont_Catlendly_header = self.screen.blit(font_Catlendly_header, [290, 145])
        rfont_press_to_start = self.screen.blit(font_press_to_start, [415, 375])
        rfont_press_to_start.width = 250
        rfont_press_to_start.width = 60

        nNumHorizontal = int(self.width/50)
        nNumVertical = int(self.height/50)
        self.star_sprites = pygame.sprite.Group()
        
        for i in range(nNumHorizontal * 2): 
            x = random.randint(0, nNumHorizontal) * 50
            y = random.randint(0, nNumVertical) * 50
            if x not in range(290, 1135) or y not in range(145, 420):
                self.star_sprites.add(Stars(pygame.Rect(x, y, 50, 50), (255,255,255)))
               

        return rfont_Catlendly_header, rfont_press_to_start

    def update_intro_background(self):
        colors = [(0, 0, 255), (255, 255, 255), (255, 0, 0)]
        nNumHorizontal = int(self.width/50)
        nNumVertical = int(self.height/50)
        self.star_sprites = pygame.sprite.Group()
        time.sleep(0.75)

        for i in range(nNumHorizontal * 2): 
            x = random.randint(0, nNumHorizontal) * 50
            y = random.randint(0, nNumVertical) * 50
            if x not in range(290, 1135) or y not in range(145, 420):
                self.star_sprites.add(Stars(pygame.Rect(x, y, 50, 50), random.choice(colors)))

    def load_asteroids(self):
        asteroid_image_array = ["asteroid1.png", "asteroid2.png", "asteroid3.png", "asteroid4.png"]
        if random.randint(0, 10) == 0:
            self.asteroid_sprites.add(Asteroid(random.choice(asteroid_image_array),
                                               random.randint(20, self.width)))
        
          
      
    def update_asteroids(self):
        for sprite in self.asteroid_sprites.sprites():
            sprite.move(self.screen_rect)
            self.asteroid_sprites.add(sprite)




class Ship(pygame.sprite.Sprite):

    def __init__(self, character):
        #Create sprite object
        pygame.sprite.Sprite.__init__(self)
        #Surface is the pygame object for representing images 
        self.image = load_image(character)
        #pygame.Rect - object for storting rectangular coordinates 
        self.rect = self.image.get_rect()
        self.rect.top = 800
        self.rect.left = 685
        self.x_dist  = 45
        self.y_dist  = 45
        self.is_alive = True

    def move(self, key, screen_rect):
        xMove = 0
        yMove = 0
        
    
        if (key == pygame.K_RIGHT):
            xMove = self.x_dist
        elif (key == pygame.K_LEFT):
            xMove = -self.x_dist
        elif (key == pygame.K_DOWN):
            yMove = self.y_dist
        elif (key == pygame.K_UP):
            yMove = -self.y_dist


        self.rect.move_ip(xMove, yMove)
        self.rect.clamp_ip(screen_rect)
        
        
class Asteroid(pygame.sprite.Sprite):

    def __init__(self, image_file, x_axis):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_file)
        self.rect = Rect(x_axis, 0, 35, 32)

    def move(self, screen_rect):

        self.rect.move_ip(0, 10)
        

class Stars(pygame.sprite.Sprite):
    
    def __init__(self, rect, color):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,3))
        self.image = self.image.convert()
        self.image.fill(color)
        self.rect = rect
       

class Static_Image(pygame.sprite.Sprite):

    def __init__(self, file_name, rect):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(file_name)
        self.rect = pygame.Rect(rect)


    
#Only run if module is not being imported
if __name__ == "__main__":
    #Create PyMain object
    MainWindow = PyMain()
    #Call PyMain method to start game
    #MainWindow.MainLoop()
    MainWindow.MainLoop()
   









