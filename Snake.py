import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox 

class cube(object):
    rows = 30
    width = 600
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color 

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, window, eyes=False):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(window, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(window, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(window, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1 
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1 
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0 
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0 
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else: 
                if c.dirnx == -1 and c.pos[0] <= 0: 
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: 
                    c.pos = (0, c.pos[1])
                elif c.dirny == -1 and c.pos[1] <= 0: 
                    c.pos = (c.pos[0], c.rows - 1)
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: 
                    c.pos = (c.pos[0], 0)
                else: 
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    
    def addCube(self):
        end = self.body[-1]             # Last element of 'body' list 
        dx, dy = end.dirnx, end.dirny   # Setting dx, dy as last coords of snake 
        if dx == 1 and dy == 0:
            self.body.append(cube((end.pos[0]-1, end.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((end.pos[0]+1, end.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((end.pos[0], end.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((end.pos[0], end.pos[1]+1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, window):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(window, True)
            else:
                c.draw(window)

def draw_grid(width, rows, window):
    size_btwn = width // rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + size_btwn
        y = y + size_btwn

        pygame.draw.line(window, (255,255,255), (x, 0), (x, width))
        pygame.draw.line(window, (255,255,255), (0, y), (width, y))

def redraw_window(window):
    global rows, width, new_snake, snack
    window.fill((0,0,0))
    new_snake.draw(window)
    snack.draw(window)
    draw_grid(width, rows, window)
    pygame.display.update()

def random_snack(rows, sprite):
    positions = sprite.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    
    return(x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, new_snake, snack
    width = 600     # Setting the width of screen
    rows = 30       # Setting the number of boxes per rows and columns 
    window = pygame.display.set_mode((width, width))    # Setting up game window
    new_snake = snake((255, 0, 0), (10, 10))            # Generate new Snake at position (10, 10)
    snack = cube(random_snack(rows, new_snake), color=(0,255,0))    # Random snack position 
    clock = pygame.time.Clock()   
    running = True

    while running:
        pygame.time.delay(50)
        clock.tick(10)
        new_snake.move()
        if new_snake.body[0].pos == snack.pos:  # If Snake head touches snack 
            new_snake.addCube()                 # Add one cube to Snake
            snack = cube(random_snack(rows, new_snake), color=(0,255,0))   # Generate a snack in a random box

        for x in range(len(new_snake.body)):    # Checks whether or not Snake touches any part of its body 
            if new_snake.body[x].pos in list( map(lambda z:z.pos, new_snake.body[x+1:])):
                print(f'Score: {len(new_snake.body)}')      # Print out score when lose
                message_box("You lost, please try again!") 
                new_snake.reset((10, 10))                   # Respawn Snake at position (10, 10)
                break
        redraw_window(window)                               # Redraw window after Snake eat snack or reload game
    pass

main()      # Starting the game 