import pygame, spawnys
from math import hypot, floor
from random import choice, random
from pygame.locals import QUIT
import json as js



goalx = 25/5
goaly = 200/5


spawnx = 350/5
spawny = 200/5


agent_move_count = 250

agent_count = 500


def average(lst): 
    return sum(lst) / len(lst) 


pygame.init()
surf = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Pygame test')
clock = pygame.time.Clock()
obs = []
moves = [1,2,3,4,5]

#stuff
# 1 - left
# 2 - up
# 3 - right
# 4 - down
# 5 - pause


def value(ag):
  dist = hypot(ag.x-goalx,ag.y-goaly)
  if ag.reached_goal:
    return 10000.0/(ag.move_count*ag.move_count)
  else:
    return 1.0/(dist*dist)


  

class agent:
  def __init__(self):
    self.is_best = False
    self.x = spawnx
    self.y = spawny
    self.move_count = 0
    self.up_count = 0
    if not self.is_best:
      self.color = (0,255,0)
    else:
      self.color = (0,0,255)
    self.moves = []
    self.reached_goal = False
    self.done = False

  def init_moves(self):
    for i in range(agent_move_count):
      self.moves.append(choice(moves))

  def move(self,dir):
    x = self.x
    y = self.y
    if dir == 1 and x != 0:
      x -= 1
    elif dir == 2 and y != 0:
      y -= 1
    elif dir == 3 and x != 119:
      x += 1
    elif dir == 4 and y != 79:
      y += 1
    elif dir == 5:
      pass
    self.x = x
    self.y = y

  def mutate(self):
    mutrate = 0.1
    for i in range(len(self.moves)):
      rand = random()
      if rand < mutrate:
        self.moves[i] = choice(moves)
    

  def update(self):
    if not self.done:
      dist = hypot(self.x-goalx,self.y-goaly)
      if dist <= 5:
        self.reached_goal = True
        self.done = True
        if not self.is_best:
          self.color = (255,0,0)
    
    if self.move_count >= len(self.moves):
      self.done = True
      if not self.is_best:
        self.color = (255,0,0)
      else:
        self.color = (0,0,255)
      return
    if not self.done:
      m = self.moves[self.move_count]
      self.move(m)
      self.move_count += 1

  def draw(self):
    rect = pygame.Rect((self.x*5),(self.y*5),5,5)
    pygame.draw.rect(surf,self.color,rect)



for _ in range(0,agent_count):
  temp = agent()
  temp.init_moves()
  obs.append(temp)

def get_best_agent(agents):
    best_agent = None
    best_score = -1
    for agent in agents:
        score = value(agent)
        if score > best_score:
            best_agent = agent
            best_score = score
    return best_agent

draw_best = False

def pr_av(ob):
  temp = []
  for o in ob:
    temp.append(value(o))
  print(f"Average:    {average(temp)}")


while True:
  surf.fill((69,69,69))
  rect = pygame.Rect((goalx*5),(goaly*5),10,10)
  pygame.draw.rect(surf,(0,0,255),rect)
  t = []
  for o in obs:
    
    o.up_count += 1
    if draw_best == False:
      o.draw()
    else:
      if o.is_best == True or o.done == True:
        o.draw()

    #only update every n framse
    if o.up_count >= 1:
      o.update()
      o.up_count = 0
    if o.done == True:
      t.append(1)
    else:
      t.append(0)

  if 0 not in t:
    temp = get_best_agent(obs)
    pr_av(obs)
    print(f"Best Score: {value(temp)}")
    print(f"Best Dest Count: {temp.move_count}\n")
    obs = []
    temp.x = spawnx
    temp.y = spawny
    temp.move_count = 0
    temp.done = False
    temp.reached_goal = False
    temp.is_best = True
    temp.color = (0,0,255)
    for i in range(1, 800):
      new_agent = agent()
      new_agent.moves = temp.moves[:]  # Copy the best agent's moves
      new_agent.mutate()  # Mutate the moves
      obs.append(new_agent)
    obs.append(temp)
    ask = 50
    ass = 25

  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      spawnys.exit()
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_r:
        draw_best = not draw_best
  pygame.display.update()
  clock.tick(60)