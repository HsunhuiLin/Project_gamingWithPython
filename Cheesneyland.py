import pygame, random, math, re, nltk
from pygame.locals import *
from sys import exit
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize 

pygame.init()

# Linguistic part of the game
'''Input corpus from nltk.data, we picked bryant-stories from the corpus "gutenberg".
   Then tokenized them and add the part of speech on each word.'''
sample = gutenberg.raw("bryant-stories.txt")
words = word_tokenize(sample)
tokens_pos = nltk.pos_tag(words)
 
'''Because we only want 5 main pos in this game: verb, noun, adjective, adverb, and preposition,
   we filter the words with the pos we want into a list called "filtered" '''
filtered = [] 
for i in range(len(words)):     #keep only verbs, nouns, adjectives, adverbs and prepositions
    if re.search("[\!\?\*\_\"\'\-\.\,\:\``]", tokens_pos[i][0]):    #clean out unwanted symbols in the text
        pass
    else:
        if tokens_pos[i][1] == "VB":
            filtered.append(tokens_pos[i])
        elif tokens_pos[i][1] == "NN":
            filtered.append(tokens_pos[i])
        elif tokens_pos[i][1] == "JJ":
            filtered.append(tokens_pos[i])
        elif tokens_pos[i][1] == "IN":
            filtered.append(tokens_pos[i])
        elif tokens_pos[i][1] == "RB":
            filtered.append(tokens_pos[i])

'''Pops is the word that is going to randomly pop up in the main game,
   for the player to distinguish their part of speech.'''
pops = random.choice(filtered)  

# Screen setup
screen = pygame.display.set_mode((800,500),0,32)
pygame.display.set_caption("On the Way to Cheesneyland!")
icon = pygame.image.load("full-of-cheese.jpg")
pygame.display.set_icon(icon)

# Menu & intro images
Menu = pygame.image.load('cheese_castle.jpg').convert()
background1 = pygame.image.load('back1.jpg').convert()
RatImg = pygame.image.load('hungryrat.png').convert_alpha()
CheeseImg = pygame.image.load('cheese1.png').convert_alpha()

# Main game images
background2 = pygame.image.load('kitchen.png').convert()
mouse_kitchen = pygame.image.load('mouse_room.png').convert_alpha()
katze = pygame.image.load('cat.png').convert_alpha()
losing = pygame.image.load('lose2.png').convert_alpha()
cheesneyland = pygame.image.load('cheesesuite.jpg').convert_alpha()
winner = pygame.image.load('winning.png').convert_alpha()

# Background Music
pygame.mixer.music.load('Bubble-Gum-Puzzler.mp3')   #specify the name of music
pygame.mixer.music.play(-1)                         #music loop
pygame.mixer.music.set_volume(0.2)                  #lower volume


# Tagger Buttons
'''Create a list for the taggers, which we place as 5 buttons on the main game for players to click on.
   We have 5 taggers/pos, each tagger set is a triple that contains xy position and the pos that shows up in the button.
   gap and radius to define the distance for each button circle. Distance = two radius + the gap inbetween.
   first one is placed in (startx, starty), the rest plus up the distance 4 more times to create the five buttons.'''
taggers = []
show_tags = ['ADJ','ADV','VERB','NOUN','PREP']
gap = 50
radius = 50
startx,starty = 100,80
for i in range(5):
    x = startx + (radius*2 + gap)*(i %5)
    y = starty
    taggers.append([x,y,show_tags[i]])

# Define colours
White = (255,255,255)
Blue = (0,0,255)
LightBlue = (66, 200, 245)
Red = (255,0,0)
Yellow = (255,255,0)
LightYellow = (230, 219, 106)

# Define global variables
Letter_Font = pygame.font.SysFont('comicsans',40)
move_x, move_y = 0, 0
speed = 0.1
pos_x, pos_y = 50, 50
wd_x, wd_y = 300, 100
running = True
play_sound_effect = True #set to control sound effect

# Display messages on screen
def display_message(message, font, color, size, y):
    Font = pygame.font.SysFont(font, size)
    text = Font.render(message, 1, color)
    screen.blit(text, (400 - text.get_width()/2, y))
    

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 80, self.y + 40, 60, 100)
    def draw(self,screen):
        self.hitbox = (self.x + 80, self.y + 40, 60, 100)

'''Class player is the rat in the first part of the game(intro).
   We need the rat/player to move to the cheese to enter the main game.
   So their positions and sizes are used as functions,
   the hitbox is to define the range for both images to collide.'''
   
class cheese(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 45, self.y + 50, 75, 60)
    def draw(self, screen):
        self.hitbox = (self.x + 45, self.y + 50, 75, 60)

# X Y position, size(width and height) setting for rat and cheese in intro game. 
rat0 = player(0, 250,100,100)
smilecheese = cheese(450,350,100,100)

# Blitting all images and guidelines to the intro/first interactive part of the game.
def introdraw():
    screen.blit(background1,(0,0))
    cheese_font = pygame.font.SysFont('comicsans',60) 
    line = cheese_font.render("Go Get the Cheese NOW!", 1, Yellow)
    screen.blit(line,(pos_x,pos_y))
    screen.blit(RatImg, (rat0.x, rat0.y))
    screen.blit(CheeseImg, (smilecheese.x, smilecheese.y))
    display_message("Use your keyboard to move", "Comic Sans MS", White, 30, 25)

# Intro loop is the first interactive part of the game, after clicking on the "enter game" button from the menu loop.
def intro():
    global speed, move_x, move_y, pos_y, play_sound_effect
    while running:
        # Background set up
        introdraw() 

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            # The rat/player moves up&down, left&right by pressing the keyborard.
            if event.type == KEYDOWN:
                # Define the movement for pressing down different keys.
                if event.key == K_LEFT:
                    move_x -= 0.5
                elif event.key == K_RIGHT:
                    move_x += 0.5
                elif event.key == K_UP:
                    move_y -= 0.5
                elif event.key == K_DOWN:
                    move_y += 0.5
                    
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0
                elif event.key == K_RIGHT:
                    move_x = 0
                elif event.key == K_UP:
                    move_y = 0
                elif event.key == K_DOWN:
                    move_y = 0
                
        rat0.x += move_x
        rat0.y += move_y
        
        # Set screen boundaries for rat
        '''In X-axis rat can only go from 0 to 600, while in Y-axis it stay between -10 and 320.'''
        if rat0.x <= 0:
            rat0.x = 0
        elif rat0.x >= 600:
            rat0.x = 600
        if rat0.y <= -10:
            rat0.y = -10
        elif rat0.y >= 320:
            rat0.y = 320  
            
        # Call the hitbox function from class player and cheese
        rat0.draw(screen)
        smilecheese.draw(screen)
        
        '''If both hitboxes collides, and if the sentence hasn't fallen down to the ground yet, player goes to the main game loop.
           hitbox[0] = x, hitbox[1] = y, hitbox[2] = width, hitbox[3] = height.'''
        if smilecheese.hitbox[1] < rat0.hitbox[1] + rat0.hitbox[3] and rat0.hitbox[1] < smilecheese.hitbox[1] + smilecheese.hitbox[3]:
            if rat0.hitbox[0]+rat0.hitbox[2] > smilecheese.hitbox[0] and rat0.hitbox[0] < smilecheese.hitbox[0] + smilecheese.hitbox[3]:
                if pos_y < 500:
                    pos_y += 0  #the sentence stop falling.
                    pygame.mixer.Sound("mixkit-funny-squeaky-toy-hits-2813.wav").play()
                    pygame.time.delay(500)
                    main_game()
        
        # Falling effect for sentence "go get the cheese now" 
        pos_y += speed
        loseSound = pygame.mixer.Sound("mixkit-game-over-trombone-1940.wav")
        '''Once the sentence falls to the bottom, meaning the rat hasn't get to the cheese yet, the player already lost the game.
           to restart playing, just press the key R.'''
        if pos_y > 500:
            move_x, move_y = 0, 0
            text = Letter_Font.render("YOU LOSE ALREADY! Press R to restart.", 1, White)
            screen.blit(text, ((800/2 - text.get_width()/2), (500/2 - text.get_height()/2)))
            
            # Condition for controlling sound effect to play once only
            if play_sound_effect:
                play_sound_effect = False   #reset value
                loseSound.play(0)           #play only once
                loseSound.fadeout(2500)
            
            # Restart intro by pressing R. Reset variables.
            if event.type == pygame.KEYUP:
                if event.key == K_r:
                    loseSound.stop()
                    play_sound_effect = True
                    pos_y = 0
                    rat0.x, rat0.y = 0, 250

        pygame.display.update()

'''Class Rat and Cat in the main game have the same purpose as class player and cheese in intro.
   we need to define their movement with their positions and the point to collide with each other.''' 
class Rat(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 90, self.y + 10, 60, 40)
    def draw(self,screen):
        self.hitbox = (self.x + 90, self.y + 10, 60, 40)
        
class Cat(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 100, self.y + 80, 100, 100)
    def draw(self,screen):
        self.hitbox = (self.x + 100, self.y + 80, 100, 100)

rat = Rat(150,300,200,130)
cat = Cat(-50,250,200,130)

# Blitting all images, falling words, pos buttons, and instruction on the main game.  
def maindraw():
    global wd_x, wd_y
    screen.blit(background2,(0,0))
    screen.blit(mouse_kitchen,(rat.x,rat.y))
    screen.blit(katze,(cat.x,cat.y))
    text = Letter_Font.render(pops[0],1,Yellow)
    screen.blit(text,(wd_x,wd_y))
    display_message("Click on the correct part of speech of the falling word", "Comic Sans MS", White, 25, 430)
    
    # Draw taggers and buttons
    for tagger in taggers:
        x, y, pos = tagger
        pygame.draw.circle(screen, Red, (x,y), radius, 3)
        pygame.draw.circle(screen, Red, (x,y), radius-5, 3)
        tag = Letter_Font.render(pos, 1, Blue)
        screen.blit(tag,(x - tag.get_width()/2, y - tag.get_height()/2))
        mouse = pygame.mouse.get_pos()
        if x - radius < mouse[0] < x + radius and y - radius < mouse[1] < y + radius: #taggers respond when the mouse is over it
            pygame.draw.circle(screen, Yellow, (x,y), radius-5, 3)
            
    # Falling effect
    ''' y position of a word keeps adding up with the speed variable that we set as 0.1,
        when y is bigger than 500(falls underneath the screen), 
        the word pops up again from the top in a random x position ranging from 100 to 600 and keep falling.
        Also the cat moves one step forward to the right.'''
    wd_y += speed
    if wd_y > 500:
        wd_x = random.randrange(180,600)
        wd_y = -25
        cat.x += 30

# Function for correct answer
'''The rat moves 40 pixels to the right with a sound, and pops up another word of random choice from our corpus in a different X position. 
   Its y-axis starts back at 100'''
def correct():
    global wd_x, wd_y, pops
    rat.x += 40
    pygame.mixer.Sound("mixkit-arcade-game-jump-coin-216.wav").play()
    pops = random.choice(filtered)   #pop up another random word choice.
    wd_x = random.randrange(180,600) #in a random range between 180 and 600
    wd_y = 100

# Function for wrong answer
'''Cat goes 30 pixels forward with this function.'''    
def incorrect():
    cat.x += 30
    pygame.mixer.Sound("mixkit-angry-cartoon-kitty-meow-94.wav").play()

# Function for winning effect
'''When the player successfully wins the game, another background image is displayed with a sound effect.
   "Quit" button and "Play Again" button will be shown on the screen.'''
def win():
    global play_sound_effect
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.blit(cheesneyland,(0,0))
        screen.blit(winner,(350,250))
        display_message('Welcome to Cheesneyland!!', 'comicsans', Red, 80, 50)
        display_message('YOU CHAMP!', 'comicsans', Red, 60, 150)
        
        if play_sound_effect:   #play only once
            play_sound_effect = False
            pygame.mixer.Sound("mixkit-animated-small-group-applause-523.wav").play(0)

        pos = pygame.mouse.get_pos()
        again_Button.draw(screen, Yellow)   #display "Play Again" button
        again_Button.isOver(pos)            #check if the current mouse position is within "Play Again" button area
        
        pygame.display.update()

# Function for losing the game 
'''When the player loses, it displays another background image with a sound effect.
   "Quit" button and "Play Again" button will also be shown on the screen.'''     
def loser():
    global play_sound_effect
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        
        screen.blit(losing,(0,0))
        display_message("SORRY but YOU LOSE!", 'comicsans', Red, 80, 50)
        pygame.mixer.music.pause()  #pause background music
        
        if play_sound_effect:   #play only once
            play_sound_effect = False
            pygame.mixer.Sound("mixkit-game-over-dark-orchestra-633.wav").play(0)
        
        pos = pygame.mouse.get_pos()    #buttons same as in win function
        quit_Button.draw(screen, Red)   #display "Quit" button
        quit_Button.isOver(pos)         #check if the current mouse position is within "Quit" button area
        again_Button.draw(screen, Yellow)
        again_Button.isOver(pos)

        pygame.display.update()

# Main game loop
def main_game(): 
    global pops, wd_y
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                '''get the mouse position and when the mouse is within any of those five buttons,
                    check if the pressed button is corresponded with the pos of the assigned word.
                    if yes, call the correct() function; otherwise the incorrect() function.'''
                m_x, m_y = pygame.mouse.get_pos()
                for tagger in taggers:
                    x, y, pos = tagger
                    dis = math.sqrt((m_x - x)**2 + (m_y - y)**2) #the distance between the mouse position and one of the pos buttons.
                    if dis < radius: #within a button circle
                        if pos == 'ADJ' and pops[1] == "JJ":    #check if player choose the correct POS
                            correct()
                        elif pos == 'ADV' and pops[1] == "RB":
                            correct()
                        elif pos == 'VERB' and pops[1] == "VB":
                            correct()
                        elif pos == 'NOUN' and pops[1] == "NN":
                            correct()
                        elif pos == 'PREP' and pops[1] == "IN":
                            correct()
                        else:
                            incorrect()

        maindraw()
        rat.draw(screen)
        cat.draw(screen)
        
        #when the rat gets to the right border of the screen, the player wins. Reset all variables and call the win() function.
        if rat.x >= 600:
            cat.x = -50
            rat.x = 150
            pops = random.choice(filtered)
            wd_y = 100
            win()
        
        #if the cat catches up the rat and their hitbox collides, the player lost the game. Reset variabls and call the loser() function.
        if cat.hitbox[0] + cat.hitbox[2] >= rat.hitbox[0]:
            cat.x = -50
            rat.x = 150
            pops = random.choice(filtered)
            wd_y = 100
            rat.hitbox = (rat.x + 80, rat.y + 10, 60, 40)
            cat.hitbox = (cat.x + 100, cat.y + 80, 100, 100)
            loser()
            
        pygame.display.update()

# Set up a "button" class for transitions among menu, intro and main game loops
'''Define attributes for button(s), draw the button(s) on screen and check if the mouse is on the button(s)'''
class button():
    def __init__ (self, color, x, y, width, height, text = "", action=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text    #text that display on button
        self.action = action    #what action will a button do
    
    # Call this method to draw the button with coloured outline and text on the screen 
    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (White))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    # Check the mouse position and mouse button, execute corresponding actions.
    def isOver(self, pos):
        global play_sound_effect
        click = pygame.mouse.get_pressed()  #get the state of mouse button
        
        # Condition for checking if the mouse position(pos) is over the surface of the button
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.color = LightBlue  #change button's color
            
            # When a specific button is clicked, trigger the relevant function
            if click[0] == 1 and self.action != None:
                play_sound_effect = True    #reset variable
                pygame.mixer.music.unpause()
                
                if self.action == "intro":
                    intro()      #intro function triggered
                elif self.action == "play":
                    main_game()  #main_game function triggered
                elif self.action == "quit":
                    quit()       #quit function triggered
        
        else: self.color = Blue

# Create three buttons for different purposes by the button class
start_Button = button(Blue, 300, 300, 200, 75, "Enter Game", "intro")  
again_Button = button(Blue, 80, 300, 180, 75, "Play Again", "play")
quit_Button = button(Blue, 520, 300, 180, 75, "Quit", "quit")

# Set up a menu before entering game
def menu():
    while running:
        screen.blit(Menu,(0,0))
        # Instructions
        display_message("By entering the game...", "Comic Sans MS", LightYellow, 35, 25)
        display_message("You become a mouse and ready to go on the journey towards Cheesneyland!", 'Comic Sans MS', White, 20, 100)
        display_message("To get there, you must pass through a wonderkitchen across the hole.", 'Comic Sans MS', White, 20, 130)
        display_message("But beware! There’s always a hungry cat right behind you!", 'Comic Sans MS', White, 20, 160)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        
        # Draw a "Enter Game" button on screen
        pos = pygame.mouse.get_pos()
        start_Button.draw(screen, Yellow)
        start_Button.isOver(pos)
        
        pygame.display.update()

menu()