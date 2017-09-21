from random import randint #For the spice of randomness
from time import strftime #For Date
from string import rstrip #For String Stripping
add_library('minim') #Imports Sound Library 
minim = Minim(this)
class Score():
    #Accepts list of name date points and saves in score object.
    def __init__(self, listerine):
        #Breaks up list elements and saves as object attributes for management later in Scoreboard() class
        self.name, self.date, self.points = listerine[0], listerine[1],int(listerine[2].rstrip('\n'))            
class Scoreboard():
    """Scoreboard object that holds score objects in dictionary and handles sorting."""
    def __init__(self):
        self.order = []
        self.scores = {}
    def add_score(self, score):
        """Adds score object to Scoreboard dictionary"""
        #Check if score already in dictionary
        if self.scores.has_key(score.points):
            #Score already in dict. Add to list
            self.scores[score.points].append(score)
        else:
            #Score not in dict. Create point key and list pair.
            self.scores[score.points] = [score]
    def sortPoints(self):
        """Sorts Scoreboard by player points and writes updated board to file"""
        msg = "Name\tDate\tPoints\n"
        print "By Points"
        self.order = []
        #Fill up list with all points
        for z in self.scores:
            self.order.append(z)
        #Sort recursively
        mergeSort(self.order)
        
        #Loop through sorted list and organize the associated objects in the table
        for a in self.order[::-1]:
            for b in self.scores:
                if b == a:
                    for c in self.scores[b]:
                        msg = msg + str(c.name) + "\t" + str(c.date) + "\t" + str(c.points) + "\n"
        #Export newly sorted table to file
        with open("data.tsv", "r+") as x:
            x.write(msg)

    def sortPlayers(self):
        """Sorts Scoreboard by Player Name (alphabetially) and writes updated board to file"""
        msg = "Name\tDate\tPoints\n"
        print "By Player"
        self.order = []
        printed = []
        #Loop through dictionary of objects and pull out all names. Put names in list for sorting.
        for a in self.scores:
            for b in self.scores[a]:
                self.order.append(b.name.lower())
        #Sort list of names and loop through it
        for a in mergeSort(self.order):
            for b in self.scores:
                for c in self.scores[b]:
                    #If already added to file, dont repeat. Else, append the object attributes associated with the names in alpha order.
                    if c.name.lower() == a and (c.name, c.date, c.points) not in printed:
                        msg = msg + str(c.name) + "\t" + str(c.date) + "\t" + str(c.points) + "\n"
                        printed.append((c.name, c.date, c.points))
        #Export sorted table to file
        with open("data.tsv", "r+") as x:
            x.write(msg)
        print 11111
    def sortDate(self):
        """Sort table by date of score (Most recent first)"""
        msg = "Name\tDate\tPoints\n"
        printed = []
        print "By Date"
        self.order = []
        #Loop through objects and pull all dates out and throw into list for sorting
        for a in self.scores:
            for b in self.scores[a]:
                self.order.append(b.date)
        #Sort list
        mergeSort(self.order)
        print self.order
        #Loop through ordered dates by most recent first
        for a in self.order[::-1]:
            for b in self.scores:
                for c in self.scores[b]:
                    #If score hasn't already been appended to table
                    if c.date == a and (c.name, c.date, c.points) not in printed:
                        #Add objects to table in order
                        msg = msg + str(c.name) + "\t" + str(c.date) + "\t" + str(c.points) + "\n"
                        printed.append((c.name, c.date, c.points))
        #Export sorted dates to file
        with open("data.tsv", "r+") as x:
            x.write(msg)
        
        print 22222

class Driver:
#Manages the driver/player data and controls
  def __init__(self):
    self.powerupcounter = 0
    self.name = "" #name for highscore logging purposes
    self.level = 1 #level is used to choose how frequently to generate traffic
    self.score = 0 #score based on checkpoints reached
    self.time_remaining = 30 #time limit to reach checkpoint
    self.dist_remaining = 2000 #distance required to travel to reach checkpoint
    self.pos = 0 #which lane the car is on
    self.x = 420
    self.y = 450
    self.jump = False #is the car currently jumping?
    self.upvel = 0 #up velocity
    self.justjumped = False #did we just jump in the last frame?
  def showcar(self): #display the car on the screen
    image(playercar,self.x,self.y,175,130) 
  def Jump(self): #function to make the car jump
    global jumpsound
    if self.y <= 450: #if the car is higher than its normal y position
        if self.jump == True: #if we are jumping
            if self.justjumped == True: #if we just jumped
                self.upvel = 20 #set the up velocity to 20 pixels per frame
                self.justjumped = False   
            self.y -= self.upvel #decrease the y value by the velocity
            self.upvel -= 1 # decrease the velocity
    else:
        self.jump = False
        self.y = 450 #lock back on to original y position
        jumpsound.close()
        jumpsound = minim.loadSnippet("jump.wav")
  def reset(self): #reset function for game over situation
      self.level = 1
      self.score = 0
      self.dist_remaining = 2000
      self.pos = 0
      self.name = ""          
       
class Prop:
  #Creates prop instances and manages their main properties (cacti and checkpoint flags)
  def __init__(self,pos,type):
      self.id = type #cactus or flag?
      self.divisor = 500
      self.x = 500 
      self.anglemultiplier = tan(radians(30)) #the slope of its movement (the m in y = mx+b)
      self.sizey = 0 
      self.sizex = self.sizey * 1.3
      self.pos = pos #coming from right of road or left?
      self.const = 0 #b value in y = mx+b
      if self.pos == (-1): self.const = 438.68 
      if self.pos == 1: self.const = -138.68
      self.y = 150
  def show(self): #displays the prop on the screen
      if self.pos == (-1): #depending on which side of the road it's coming from, the equation is different.
          self.y = ((-1) * self.x * self.anglemultiplier) + self.const
      if self.pos == 1:
          self.y = (self.x * self.anglemultiplier) + self.const
      if self.id == 0: #displays the object based on its ID
          self.sizex = self.sizey
          image(cactus,self.x,self.y,self.sizex,self.sizey)
      elif self.id == 1:
          self.sizex = self.sizey*2
          image(flag,self.x,self.y,self.sizex,self.sizey)          
              
class AI:
  #creates instances of traffic cars (AI) and stores their basic data
  def __init__(self,pos,ID):
    #nearly all values are the same in purpose as the prop class data
    self.id = ID
    self.divisor = 500
    self.x = 500
    self.anglemultiplier = tan(radians(50))
    self.sizey = 0
    self.sizex = self.sizey * 1.3
    self.pos = pos
    self.const = 0
    if self.pos == (-1): self.const = 745.9
    if self.pos == 1: self.const = -445.9
    self.y = 150
    if self.pos == 0: #if the car is coming down the middle
        self.y = 150    
  def showcar(self): #displays the car on the screen
    self.sizex = self.sizey * 1.3
    if self.pos == (-1):
        self.y = ((-1) * self.x * self.anglemultiplier) + self.const
    if self.pos == 1:
        self.y = (self.x * self.anglemultiplier) + self.const
    if self.id == 0:
        image(AIcar,self.x,self.y,self.sizex,self.sizey)
    if self.id == 1:
        image(orb,self.x,self.y,self.sizex,self.sizey)
 
class AIgroup:
  #Class that manages props and cars in traffic.
  def __init__(self):
    self.cars = []
    self.props = []
    self.flagexists = False #boolean to keep track of whether the flag is visible or not
  def spawncar(self,pos,ID): #adds a car object into the list of cars
    self.cars.append(AI(pos,ID))
  def spawnprop(self,pos): #adds a prop object into the list of props
    self.props.append(Prop(pos,0))
  def spawnflag(self,pos): #spawns a prop with the ID of a flag
    self.props.append(Prop(pos,1))
    self.flagexists = True
  def simulate(self,speed): #this method simulates the movement of props and cars based on the player's speed and pseudo 3d rules
    imageMode(CENTER)
    for i in range(len(self.cars)-1,-1,-1): #loops through the list of cars backwards (so that nearer cars are displayed before the farther cars)
        temp = (speed * self.cars[i].y/self.cars[i].divisor) #temp is the speed of the AI cars (in pixels per frame)
        if speed == 0: #If the player stops
            temp = -0.5 #AI cars move forwards 
        if self.cars[i].divisor > 20: #divisor of each car decreases (causing speed to increase as they get closer)
            if self.cars[i].y > 275: #if the cars are very close
                self.cars[i].divisor -= (2.5 * speed) #the speed increases even more
            else:
                self.cars[i].divisor -= (1.8 * speed) #otherwise they are accelerating at a lesser rate
        if self.cars[i].pos == (-1): #if the car is on the left lane
            self.cars[i].x -= temp #make the x variable go left by the speed
        if self.cars[i].pos == 1:
            self.cars[i].x += temp #make the x variable go right by the speed
        if self.cars[i].pos == 0:
            self.cars[i].y += temp #make the y variable go down by the speed (no angle - going straight down)
        self.cars[i].sizey = ((self.cars[i].y-150)/2.8) #increase size depending on how far down the y variable of the car is
        self.cars[i].showcar() #show the car using its built in display method
    for i in range(len(self.props)-1,-1,-1): #loops through all the props
        #from here it is very similar to the car movement, but at different angles and speeds
        temp1 = abs((speed * self.props[i].y/self.props[i].divisor))
        if self.props[i].divisor > 10:
            self.props[i].divisor -= (4 * speed)
        if self.props[i].pos == (-1):
            self.props[i].x -= temp1
        if self.props[i].pos == 1:
            self.props[i].x += temp1
        if self.props[i].id == 0:
            self.props[i].sizey = ((self.props[i].y-150)/2)
        if self.props[i].id == 1:
            self.props[i].sizey = ((self.props[i].y-150)/1)            
        self.props[i].show()
    
    #the following code loops through cars and props, checks if they are out of the screen, and pops them if they are    
    n = 0
    while n < (len(self.cars)):
        if self.cars[n].y > 750 or self.cars[n].y < 150:
            self.cars.pop(n)
            n -= 1
        n += 1
    n = 0
    while n < (len(self.props)):
        if self.props[n].y > 750 or self.props[n].y < 150:
            if self.props[n].id == 1:
                self.flagexists = False
            self.props.pop(n)
            n -= 1
        n += 1
  
  def checkcollision(self,playerY,playerpos): #method that checks if we have collided with one of the cars
    for i in self.cars:
        if (i.y >= 450 and i.y <= 550) and i.pos == playerpos: #if they are within the same Y value AND they are in the same lane
            if playerY >= 350: #if the car is on the ground (not jumping)
                return i.id #we collided, return what we collided into
  def pushback(self): #this is the resultant movement in the cars after a collision
    amount = 15
    for i in self.cars:
        if i.pos == (-1):
            i.x += amount
        if i.pos == 1:
            i.x -= amount
        if i.pos == 0:
            i.y -= amount    
    
class Lane: #this class handles the lanes on the road and their movement/size
  def __init__(self):
    self.speed = 1 #speed of the lane
    self.acc = 1 #acceleration of the lane
    self.x = 0 #start of lane's x
    self.y = 0 #start of lane's y
    self.yinc = 0 #end of lane's y (tail)
    self.xinc = 0 #end of lane's x
  def display(self): #show 2 lane lines
    stroke(255)
    strokeWeight(self.y/50)
    line(500+self.x,150 + self.y,500 + self.x+ self.xinc,150 + self.y + self.yinc)
    line(500-self.x,150 + self.y,500 - self.x - self.xinc,150 + self.y + self.yinc)
    self.acc += 0.1
  def move(self): #move the 2 lane lines based on their speed and acceleration
    self.x += 1.2*self.speed*self.acc
    self.xinc += 0.4*self.speed*self.acc
    self.y += 3*self.speed*self.acc
    self.yinc += 1*self.speed*self.acc
class Road: #class that manages the lanes on the road
  def __init__(self):
    self.items = [] #stores lane pairs
  def simulate(self):
    if len(self.items) == 0 or self.items[-1].y >= 50:
        temp = Lane() #creates a new lane pair if the previous pair is a certain distance away
        self.items.append(temp) #puts the lane into the lane list
    if self.items[0].y >= 1500: #if the lane has left the screen
        self.items.pop(0) #remove it
    for i in self.items:
        i.display() #show the lanes
        i.move() #simulate lane movement
  def changespeed(self,speed): #changes the speed of the lanes based on the player's speed
    for i in self.items:
        i.speed = speed    
             
#Highscore Table:             
def mainmenu():
    global name, date, points, scroll, c1, c2, c3, c4, c5, c6,y
    c = 1
    d = 1
    stroke(0)
    fill(255)
    textSize(32)
    textMode(CENTER)
    text("HighScores", 425, 40)
    #Open and read all lines in the data file
    with open("data.tsv", "r") as x:
        for a in x:
            c += 1
            d = 1
            #Print all data to screen in Name, Date, Points format
            for b in a.split("\t"):
                if d == 1:
                    text(b, d*20, c*49)
                elif d == 2:
                    text(b, d*180, c*49)
                elif d == 3:
                    text(b, d*200, c*49)
                else:
                    pass
                d += 1
    #Create sorting buttons
    stroke(255)
    fill(c1)
    rect(width-220, 100, 200, 50, 20)
    fill(c2)
    rect(width-220, 200, 200, 50, 20)
    fill(c3)
    rect(width-220, 300, 200, 50, 20)
    fill(c4)
    text("Sort Date",width-190, 105, 200, 50)
    fill(c5)
    text("Sort Pts",width-180, 205, 200, 50)
    fill(c6)
    text("Sort Name", width-195, 305, 200, 50)
    
    #If mouse over one of buttons, change mouse cursor from arrow to hand
    if ((width - 220) < mouseX < (width-20)):
        if (100 + y < mouseY < 150+ y) or (200+ y < mouseY < 250+ y) or (300+ y < mouseY < 350+ y):
            cursor(HAND)
        else:
            cursor(ARROW)
    else:
        cursor(ARROW)

def mergeSort(alist):
    """Sort recursively by splitting down list and rebuilding"""
    if len(alist)>1:
        mid = len(alist)//2
        left = alist[:mid]
        right = alist[mid:]
        #Break down the list recursively until len == 1
        mergeSort(left)
        mergeSort(right)
    
        i, j, k = 0, 0, 0
        #Build the list back up
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                alist[k]=left[i]
                i += 1
            else:
                alist[k]=right[j]
                j += 1
            k += 1
    
        while i < len(left):
            alist[k]=left[i]
            i += 1
            k += 1
    
        while j < len(right):
            alist[k]=right[j]
            j += 1
            k += 1
    return alist
         
def setup():
  frameRate(60)
  global player,playercar,AIcar,orb,cantpress,playroad,gamespeed,transition,traffic,cactus,flag,phase,timecount, board, name, date, points, y, scroll, c1, c2, c3, c4, c5, c6,mainscreenimg,salmone,enginestartup,intromusic,jumpsound,idlesound,collidesound,collideswitch,gameoversound
  size(1000,600)
  enginestartup = minim.loadFile("startup.wav")
  intromusic = minim.loadFile("bugs.mp3")
  jumpsound = minim.loadSnippet("jump.wav")
  idlesound = minim.loadFile("idle.wav")
  collidesound = minim.loadFile("hit.wav")
  collideswitch = False
  gameoversound = minim.loadSnippet("gameover.wav")
  playercar = loadImage("playercar.png")
  AIcar = loadImage("AIcar.png")
  orb = loadImage("orb.png")
  cactus = loadImage("cactoos.png")
  flag = loadImage("flag.png")
  mainscreenimg = loadImage("backy.jpg")
  salmone = loadImage("salmone.png")
  player = Driver()
  cantpress = False #manages lane switching (makes sure you cant hold the right key and just switch 2 lanes)
  playroad = Road()
  gamespeed = 0 #speed of the car
  transition = False #manages change-lane animation
  traffic = AIgroup()
  phase = 0 #variable controls what screen to display
  timecount = 0 #keeps track of seconds
  #colour variables for buttons
  c1 = 0 
  c2 = 0
  c3 = 0
  c4 = 255
  c5 = 255
  c6 = 255
  y = 0 #y variable for highscore scrolling
  board = Scoreboard()
  #Gets current date at point when called in format (YYYY/MM/DD)
  date = strftime("%Y/%m/%d")
  #Read all lines from file and throw into list
  with open('data.tsv', "r") as x:
    f = [line.split('\t') for line in x]
  #For all lines in the new list (Except the first which contains garbage):
  for scores in f[1:]:
    board.add_score(Score(scores))  #Create score object out of all data in the line. Then add that score object into the scoreboard class
def draw():
  global player,playercar,AIcar,cantpress,orb,playroad,gamespeed,transition,traffic,cactus,flag,phase,timecount, board, name, date, points, y, scroll, c1, c2, c3, c4, c5, c6,mainscreenimg,salmone,enginestartup,intromusic,jumpsound,idlesound,collidesound,collideswitch,gameoversound
  if phase == 0: # if we are in start menu
      background(100)
      image(mainscreenimg,0,0,1000,600)
      image(salmone,50,500,300,75)
      textSize(50)
      fill(255)
      text("Crazy Car Jump Bonanza",70,100)
      textSize(40)
      if (mouseX >= 350 and mouseX <= 650) and (mouseY >= 150 and mouseY <= 250):
          fill(0,255,0)
      else:
          fill(0)
      text("PLAY",340,220)
      if (mouseX >= 250 and mouseX <= 650) and (mouseY >= 300 and mouseY <= 400):
            fill(0,255,0)
      else:
          fill(0)
      text("HIGHSCORES",270,370)
      if (mouseX >= 650 and mouseX <= 800) and (mouseY >= 420 and mouseY <= 550):
            fill(0,255,0)
      else:
          fill(0)
      text("QUIT",700,485)
      if ((mouseX >= 350 and mouseX <= 650) and (mouseY >= 150 and mouseY <= 250)) or ((mouseX >= 250 and mouseX <= 650) and (mouseY >= 300 and mouseY <= 400)) or ((mouseX >= 650 and mouseX <= 800) and (mouseY >= 420 and mouseY <= 550)):
        cursor(HAND)
      else:
          cursor(ARROW)
      noFill()
      stroke(0)
  if phase == 2: #if we're in the highscore table
      background(0)
      translate(0, y)
      mainmenu()
  if phase == 3: #if we get the gameover screen
      gameoversound.play()
      background(0)
      fill(255)
      textSize(50)
      text("GAME OVER",325,150)
      textSize(35)
      text("YOUR SCORE: %s" %(player.score),350,300)
      textSize(20)
      text("ENTER YOUR NAME: %s" %(player.name),50,400) 
      text("PRESS ENTER TO CONTINUE",350,550)
      textSize(10)
      text("SCORES OF 0 WILL NOT BE LOGGED",400,600)
            
  if phase == 1: #if we are in game
    cursor(ARROW)
    background(50,100,255)
    #setting design
    strokeWeight(4)
    fill(150)
    noStroke()
    triangle(500,150,0,605,1000,605)
    fill(200,250,100)
    triangle(500,150,1000,150,1000,605)
    triangle(500,150,0,150,0,605)
    if keyPressed:
        if key == " ": #space makes the car jump
            jumpsound.play()
            player.jump = True
            if player.y == 450:
                player.justjumped = True                         
        if keyCode == UP: #increase the speed of the car as long as it is under 6
            if gamespeed < 6:
                gamespeed += 0.005
        if keyCode == DOWN: #decrease the speed if it is > 0
            if gamespeed > 0.005:
                gamespeed -= 0.005
            else:
                gamespeed = 0   
        if cantpress == False: #if we have just pressed the key
            if keyCode == RIGHT:
                #switch lanes to one to the right
                if player.pos < 1:
                    player.pos += 1
                    cantpress = True #doesn't allow anymore lane switching to occur until the key has been released and pressed again
                    transition = True #activate lane switch animation
            if keyCode == LEFT:
                #switch lanes to one to the left
                if player.pos >= 0:
                    player.pos -= 1
                    cantpress = True
                    transition = True
    if transition == True:
        #animates lane switching
        if player.pos == 1:
            if player.x < 700:
                player.x += 20
            else:
                transition = False
        if player.pos == (-1):
            if player.x > 120:
                player.x -= 20
            else:
                transition = False
        if player.pos == 0:
            if player.x < 420:
                player.x += 20
            elif player.x > 420:
                player.x -= 20
            else:
                transition = False
    if player.powerupcounter > 1:
        gamespeed = 20
        player.y = 200
        player.powerupcounter -= 1
    elif player.powerupcounter == 1:
        player.y = 450
        gamespeed = 2
        player.powerupcounter -= 1
    if traffic.checkcollision(player.y,player.pos) == 0:
        collideswitch = True
        gamespeed = 0 #set speed to 0
        traffic.pushback()
    else:
        collideswitch = False
    if traffic.checkcollision(player.y,player.pos) == 1:
        player.powerupcounter = 300        
    if collideswitch == True:
        collidesound.rewind()
        collidesound.play()
    if second() == 0:
        timecount = 0
    if second() > timecount: #timecount works with second counting library to keep track of time
        timecount = second()
        #as soon as the second() function increases, decrease the remaining time
        player.time_remaining -= 1
    if player.dist_remaining <= 0: #if we reach a checkpoint
        player.level += 1
        player.score += (10000 + (100*player.time_remaining)) #give a base score of 10000 but add extra for finishing early
        player.time_remaining = 30 #reset time limit
        player.dist_remaining = 2000 + (100*((player.level)-1)) #reset distance, but increase it a little based on level
    if player.dist_remaining <= 131 and player.dist_remaining >= 0: # if we are 131 meters from the flag
        if traffic.flagexists == False:
            traffic.spawnflag(1) #show the flag
    if player.time_remaining <= 0 and player.dist_remaining > 0: #if we did not make it in time
        gamespeed = 0
        traffic.cars = []
        traffic.props = []
        phase = 3 #enter gameover phase
    temp = randint(0,50)
    #checks if the random number = 26 and spawns the prop based on whether the remaining distance is an odd or even number
    if temp == 26:
        temppos = 0
        if (int(player.dist_remaining) % 2) == 0: temppos = 1
        else: temppos = -1
        traffic.spawnprop(temppos)
    if gamespeed >= 0.3:
        #spawn cars randomly, but more frequently based on level
        temp = randint(0,int(100/player.level))
        temp1 = randint(0,1000)
        if temp == 1:
            traffic.spawncar(randint(-1,1),0)
        if temp1 == 55:
            traffic.spawncar(randint(-1,1),1)
    player.dist_remaining -= gamespeed #decrement the remaining distance
    playroad.simulate()
    playroad.changespeed(gamespeed)
    traffic.simulate(gamespeed)
    imageMode(CORNER)
    player.showcar()
    player.Jump()
    fill(0)
    textSize(20)
    text("Score: %s"%(player.score),20,30)
    text("Next Checkpoint: %s m"%(int(player.dist_remaining)),20,60)
    text("Time Left: %s s" %(player.time_remaining),20,90)
  if phase == 0 or phase == 2:
      intromusic.play()
  else:
      intromusic.pause()

def keyReleased():
  global player,cantpress,traffic,phase,gamespeed,board,date,gameoversound
  if phase == 1:
    if key == BACKSPACE:
        gamespeed = 0
        traffic.cars = []
        traffic.props = []
        player.reset()
        phase = 0
    cantpress = False
  if phase == 2:
      if key == BACKSPACE:
          phase = 0
  if phase == 3:
      if key == BACKSPACE:
          player.name = player.name[:len(player.name)-1]
      elif key == ENTER:
        gameoversound.close()
        gameoversound = minim.loadSnippet("gameover.wav")
        if player.score > 0:
            board.add_score(Score([(player.name).rstrip("\n"),date,str(player.score)]))
        player.reset()
        phase = 0
        board.sortPlayers()
      else:
        if not(key == CODED):
            if key in "abcdefghijklmnopqrstuvwxyz1234567890~`!@#$%^&*()_+-=:\/><.,{}[][ ":
                if len(player.name) <= 14:
                    player.name += key.upper()

def mousePressed():
    global phase, c1, c2, c3, c4, c5, c6, y
    if phase == 2: #highscore table button highlighting
        if ((width - 220) < mouseX < (width-20)):
            if (100 +y < mouseY < 150 + y):
                c1 = 255
                c4 = 0
            elif (200 + y < mouseY < 250 + y):
                c2 = 255
                c5 = 0
            elif (300 + y < mouseY < 350 + y):
                c3 = 255
                c6 = 0    
def mouseReleased():
    global phase,player, c1, c2, c3, c4, c5, c6, board,y,enginestartup,idlesound
    if phase == 0: #buttons in start menu
        if (mouseX >= 350 and mouseX <= 650) and (mouseY >= 150 and mouseY <= 250):
            phase = 1
            player.time_remaining = 30
            idlesound.loop()
            enginestartup.close()
            enginestartup = minim.loadFile("startup.wav")
            enginestartup.play()
        if (mouseX >= 350 and mouseX <= 650) and (mouseY >= 300 and mouseY <= 400):
            phase = 2
        if (mouseX >= 650 and mouseX <= 750) and (mouseY >= 450 and mouseY <= 550):
            exit()
    if phase == 2: #highscore button pressing and color reset
        c1, c2, c3 = (0, 0, 0)
        c4, c5, c6 = (255, 255, 255)
     
        if ((width - 220) < mouseX < (width-20)):
                if (100+y < mouseY < 150 + y):
                    board.sortDate()
                elif (200+y < mouseY < 250 + y):
                    board.sortPoints()
    
                elif (300+y < mouseY < 350  + y):
                    board.sortPlayers()

def mouseWheel(event): #highscore scrolling
    global y,phase
    if phase == 2:
        if event.count == -1:
            y += 25
        elif event.count == 1:
            y -= 25 
 
 