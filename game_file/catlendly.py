import os, sys, random, time, string, pickle
import pygame
from pygame.locals import *
pygame.font.init()


def load_image(file_name):
    image = pygame.image.load(file_name)
    image = image.convert()
    return image

def load_fonts(text, size, color):
    font = pygame.font.Font("../assets/PressStart2P-Regular.ttf", size)
    space_font = font.render(text, 1, color)
    return space_font


class PyMain(object):
    score_array = [0,0,0]
    player_names = ["$$$","###","***"]
    player_scores = {"$$$":0, "###":0, "***":0}
    total = {
         3: (570, 600),
         4: (570, 650),
         5: (570, 700),
         6: (570, 900)
    }
    players_total = total[len(player_scores.keys())]


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
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.game_screen = pygame.Surface((1439, 844)).convert()
        self.game_screen_rect = self.game_screen.get_rect()
        self.stage_background = load_image("../assets/catlendly_background.png")
        self.lives = 3
        self.health_bar_surface = load_image("../assets/health_bar_100.png")
        self.score = 0

    def MainLoop(self):

        first_initial = "-"
        middle_initial = "-"
        last_initial = "-"
        full_initials = first_initial + middle_initial + last_initial
        y = 0
        self.time_hit = 0
        self.load_intro_sprites()
        #Main game loop
        while self.level != "restart":
            rel_y = y % self.stage_background.get_rect().height
            if self.level == "Intro":
                self.screen.blit(self.font_top_scores, [550, 500])
                self.screen.blit(self.font_score_one, [575, 600])
                self.screen.blit(self.font_score_two, [575, 650])
                self.screen.blit(self.font_score_three, [575, 700])
                self.screen.blit(self.score_cover, PyMain.players_total)
                self.star_sprites.draw(self.screen) 
                pygame.display.update()
                self.star_sprites.clear(self.screen, self.background)
                self.star_sprites.empty()
                self.update_star_sprites()
            elif self.level == "Character_selection":
                pygame.display.update()
            elif self.level == "Stage_one":
                self.screen.blit(self.stage_background, (0, (rel_y - self.stage_background.get_rect().height)))
                self.load_asteroids()
                if pygame.sprite.spritecollide(self.ship, self.asteroid_sprites, False):
                    self.ship.image = load_image("../assets/ship_explosion.png")
                    if self.ship.is_alive:
                        self.lives -= 1
                        self.time_hit = time.time()
                        self.health_bar_surface = load_image({
                            "0": "../assets/health_bar_0.png",
                            "1": "../assets/health_bar_33.png",
                            "2": "../assets/health_bar_67.png",
                            "3": "../assets/health_bar_33.png",
                            "4": "../assets/health_bar_45.png",
                            "5": "../assets/health_bar_56.png",
                            "6": "../assets/health_bar_67.png",
                            "7": "../assets/health_bar_78.png",
                            "8": "../assets/health_bar_89.png"
                }[str(self.lives)])
                    self.ship.is_alive = False
                if int(self.time_hit + 1.5) == int(time.time()):
                    self.ship_sprites.empty()
                    self.Stage_one(True)
                self.asteroid_sprites.draw(self.screen)
                self.move_asteroids()
                self.screen.blit(self.health_bar_surface, [215, 855])
                self.font_score = load_fonts("Score: %d" % self.score, 20, (255, 255, 255))
                self.screen.blit(self.font_score, [1180, 870])
                self.ship_sprites.draw(self.screen)
                pygame.display.update()
                if self.ship.is_alive:
                    self.score += 1 
                y += 1
                if rel_y < 899:
                    self.screen.blit(self.stage_background, (0, rel_y))
            elif self.level == "Game_Over":
                #Reset initials when user uses backspace
                pygame.draw.rect(self.screen, (0,0,0), (500, 500, 400, 200))
                self.font_player_initials = load_fonts("%s%s%s" % (first_initial, middle_initial, last_initial), 90, (255, 255, 255))
                self.screen.blit(self.font_player_initials, [550, 550])
                pygame.display.update()

            
            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "escape":
                        sys.exit()
                if self.level == "Stage_one":
                    if event.type == pygame.KEYDOWN and self.ship.is_alive:
                            self.ship.move(event.key, self.game_screen_rect)
                elif self.level == "Intro":
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:               
                            self.level = "Character_selection"
                            self.Character_Selection()
                elif self.level == "Character_selection":
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] in range(150, 380) and mouse[1] in range(700, 768):
                        image_group = pygame.sprite.Group(Static_Image('../assets/button_success.png', (150, 700, 250, 68)))
                        image_group.draw(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.level = "Stage_one"
                            self.character = "../assets/Ship1.png"
                            self.Stage_one(False)
                    elif mouse[0] in range(580, 810) and mouse[1] in range(700, 768):
                        image_group = pygame.sprite.Group(Static_Image('../assets/button_success.png', (580, 700, 250, 68)))
                        image_group.draw(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.level = "Stage_one"
                            self.character = "../assets/Ship2.png"
                            self.Stage_one(False)
                    elif mouse[0] in range(1010, 1260) and mouse[1] in range(700, 768):
                        image_group = pygame.sprite.Group(Static_Image('../assets/button_success.png', (1010, 700, 250, 68)))
                        image_group.draw(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.level = "Stage_one"
                            self.character = "../assets/Ship3.png"
                            self.Stage_one(False)
                    else:
                        image_group = pygame.sprite.Group(Static_Image('../assets/button_inactive.png', (150, 700, 250, 68)), 
                                                          Static_Image('../assets/button_inactive.png', (580, 700, 250, 68)),
                                                          Static_Image('../assets/button_inactive.png', (1010, 700, 250, 68)))
                        image_group.draw(self.screen)
                elif self.level == "Game_Over":
                    if event.type == pygame.KEYDOWN:
                        key = pygame.key.name(event.key)
                    
                        if key == "backspace" or key == "delete":
                            
                            if last_initial != "-":
                                last_initial = "-"
                            elif middle_initial != "-":
                                middle_initial = "-"
                            elif first_initial != "-":
                                first_initial = "-"

                        if key in string.ascii_letters:
                            if first_initial == "-":
                                first_initial = pygame.key.name(event.key).upper()
                            elif middle_initial == "-":
                                middle_initial = pygame.key.name(event.key).upper()
                            elif last_initial == "-":
                                last_initial = pygame.key.name(event.key).upper()

                        elif key == "return":
                            full_initials = "%s%s%s" % (first_initial, middle_initial, last_initial)
                            PyMain.player_scores[full_initials] = self.score
                            try:
                                saved_file = open("player_scores.txt", "wb")
                                pickle.dump(PyMain.player_scores, saved_file)                  
                                saved_file.close()
                            except:
                                print "Failed to save file."
                            

                            self.level = "restart"
                        
        MainWindow = PyMain()
        MainWindow.MainLoop()

    def game_over(self):
        self.asteroid_sprites.clear(self.screen, self.background)
        self.asteroid_sprites.empty()
        self.font_gameover = load_fonts("Game Over", 95, (42, 247, 44))
        self.font_final_score = load_fonts("Score: %d" % self.score, 50, (255, 255, 255))
        self.font_enter_initials = load_fonts("Enter initials:", 50, (255, 255, 255))
        #Remove healthbar and stage score
        pygame.draw.rect(self.screen, (0,0,0), (0, 750, 1400, 200))
        #Add text
        self.screen.blit(self.font_gameover, [290, 145])
        self.screen.blit(self.font_final_score, [450, 300])
        self.screen.blit(self.font_enter_initials, [350, 400])
        

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
        static_image_group = pygame.sprite.Group(Static_Image('../assets/Cat1.png', (105, 175, 144, 119)),
                                                 Static_Image('../assets/Cat2.png', (535, 175, 144, 119)),
                                                 Static_Image('../assets/Cat3.png', (965, 175, 144, 119)),
                                                 Static_Image('../assets/button_inactive.png', (150, 700, 250, 68)),
                                                 Static_Image('../assets/button_inactive.png', (580, 700, 250, 68)),
                                                 Static_Image('../assets/button_inactive.png', (1010, 700, 250, 68)),
                                                 Static_Image('../assets/Ship1.png', (285, 580, 75, 73)),
                                                 Static_Image('../assets/Ship2.png', (710, 580, 75, 73)),
                                                 Static_Image('../assets/Ship3.png', (1135, 580, 75, 73))
                                                 )
        #Draw static_image_group to screen
        static_image_group.draw(self.screen)
        pygame.display.update()

    def Stage_one(self, reset): 

        if reset:
            if self.lives == 0:
                self.level = "Game_Over"
                self.game_over()
            else:
                self.screen.blit(self.font_score, [1180, 870])
                self.ship_sprites = self.load_ship_sprite(self.character)
                self.ship_sprites.draw(self.screen)
                self.asteroid_sprites.empty()
                self.stage_time = time.time()
           

        else:
            self.screen.fill((0,0,0))
            self.star_sprites.clear(self.screen, self.background)
            self.star_sprites.empty()
            self.stage_time = time.time()
            self.screen.blit(self.health_bar_surface, [844, 215])
            self.ship_sprites = self.load_ship_sprite(self.character)
            self.ship_sprites.draw(self.screen)
            self.asteroid_sprites = pygame.sprite.Group()
            
            pygame.display.update()

                
       
             
    def load_ship_sprite(self, character):
        
        self.ship = Ship(character)
        self.ship_sprites = pygame.sprite.Group(self.ship)
        return self.ship_sprites

    def load_intro_sprites(self):

        try:
            PyMain.score_array = []
            player_scores_file = open("player_scores.txt", "r+b")
            PyMain.player_scores = pickle.load(player_scores_file)
            player_scores_file.close()
            if len(PyMain.player_scores.keys()) < 7:
                PyMain.players_total = PyMain.total[len(PyMain.player_scores.keys())]
            else:
                PyMain.players_total = PyMain.total[6]
            score_tuple = PyMain.player_scores.items()
            PyMain.score_array = []
            for tuple_pair in score_tuple:
                PyMain.score_array.append(tuple_pair[1])

            PyMain.score_array_sorted = sorted(PyMain.score_array)
            reversed_score = PyMain.score_array_sorted[::-1]
            top_three_scores = reversed_score[0:3]
            
                

            PyMain.player_names = []
            for i in range(0,3):
                for tuple_pair in score_tuple:
                    if top_three_scores[i] in tuple_pair:
                        PyMain.player_names.append(tuple_pair[0])
        except:
            print "Unable to open file."
     

        self.score_cover = pygame.Surface((300, 300))
        self.score_cover.fill((0,0,0))
        font_Catlendly_header = load_fonts("Catlendly", 95, (42, 247, 44))
        font_press_to_start = load_fonts("Press Enter to Start", 30, (191, 0, 255))
        rfont_Catlendly_header = self.screen.blit(font_Catlendly_header, [290, 145])
        rfont_press_to_start = self.screen.blit(font_press_to_start, [415, 375])
        rfont_press_to_start.width = 250
        rfont_press_to_start.width = 60
        self.font_top_scores = load_fonts("TOP SCORES ", 30, (255, 255, 255))
        self.font_score_one = load_fonts("%s: %s" % (PyMain.player_names[0], PyMain.player_scores[PyMain.player_names[0]]), 30, (255, 255, 255))
        self.font_score_two = load_fonts("%s: %s" % (PyMain.player_names[1], PyMain.player_scores[PyMain.player_names[1]]), 30, (255, 255, 255))
        self.font_score_three = load_fonts("%s: %s" % (PyMain.player_names[2], PyMain.player_scores[PyMain.player_names[2]]), 30, (255, 255, 255))    

        nNumHorizontal = int(self.width/50)
        nNumVertical = int(self.height/50)
        self.star_sprites = pygame.sprite.Group()
        
        for i in range(nNumHorizontal * 2): 
            x = random.randint(0, nNumHorizontal) * 50
            y = random.randint(0, nNumVertical) * 50
            if x not in range(290, 1135) or y not in range(145, 420):
                self.star_sprites.add(Stars(pygame.Rect(x, y, 50, 50), (255,255,255)))
               

        return rfont_Catlendly_header, rfont_press_to_start

    def update_star_sprites(self):
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

        asteroid_image_array = ["../assets/asteroid1.png", "../assets/asteroid2.png", "../assets/asteroid3.png", "../assets/asteroid4.png"]
        if int(self.stage_time + 30) < int(time.time()):
            if random.random() < 0.3:
                self.asteroid_sprites.add(Asteroid(random.choice(asteroid_image_array),
                                                   random.randint(20, self.width)))
        elif int(self.stage_time + 15) < int(time.time()):
            if random.random() < 0.2:
                self.asteroid_sprites.add(Asteroid(random.choice(asteroid_image_array),
                                                   random.randint(20, self.width)))
        else:
            if random.random() < 0.1:
                self.asteroid_sprites.add(Asteroid(random.choice(asteroid_image_array),
                                                   random.randint(20, self.width)))
    def move_asteroids(self):

        for asteroid in self.asteroid_sprites.sprites():
            asteroid.move(self.screen_rect)
            self.asteroid_sprites.add(asteroid)


class Ship(pygame.sprite.Sprite):

    def __init__(self, character):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(character)
        self.rect = self.image.get_rect()
        self.rect.top = 770
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
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(file_name)
        self.rect = pygame.Rect(rect)

#Only run if module is not being imported
if __name__ == "__main__":
    MainWindow = PyMain()
    MainWindow.MainLoop()


    
   







