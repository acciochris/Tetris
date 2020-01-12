from asynctk import *
import random
import time
import sys
import collections
import asyncio

colors = ["red","green","blue","yellow"]
current_block = None

class Blocks:
    def __init__(self, filename):
        with open(filename,'r') as f:
            self.data = [a.split('\n') for a in f.read().split('/')]
            self.blocks = []
            self.block = []
            for x in self.data:
                for y in x:
                    if y:
                        self.block.append(y.split())
                self.blocks.append(self.block)
                self.block = []
            self.blocks = [x for x in self.blocks if x]
    def pick(self):
        block = self.blocks[random.randrange(len(self.blocks))]
        return block

class Block:
    def __init__(self,shape,x,y,canvas,color):
        self.shape = shape
        self.x = x
        self.y = y
        self.canvas = canvas
        self.color = color
    
                    
class Game:
    def __init__(self):
        self.tk = AsyncTk()
        self.tk.title("Tetris")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = AsyncCanvas(self.tk, width=1500, height=1000, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 400
        self.canvas_width = 1500
        self.running = True
        # create windows
        # bind start and stop
        self.tk.bind("<Return>",self.start)
        self.tk.bind("<Escape>",self.stop)
        # get event loop
        #while True:
        #    self.tk.update_idletasks()
        #    self.tk.update()
    def start(self,evt):
        self.running = True
    
    def stop(self,evt):
        self.running = False


class Player:
    window = None
    def move_left(self,evt):
        pass
    def move_right(self,evt):
        pass
    def rotate_left(self,evt):
        pass
    def rotate_right(self,evt):
        pass
    def drop_to_bottom(self,evt):
        pass
    def show_next_block(self):
        pass
    def drop(self):
        pass

class Player1(Player):
    window = "left"
    def __init__(self,name,canvas):
        self.lines = 0
        self.name = name
        self.canvas = canvas
        self.canvas.bind_all("<a>",super().move_left)
        self.canvas.bind_all("<d>",super().move_right)
        self.canvas.bind_all("<q>",super().rotate_left)
        self.canvas.bind_all("<e>",super().rotate_right)
        self.canvas.bind_all("<s>",super().drop_to_bottom)

class Player2(Player):
    window = "right"
    def __init__(self,name,canvas):
        self.lines = 0
        self.name = name
        self.canvas = canvas
        self.canvas.bind_all("<1>",super().move_left)
        self.canvas.bind_all("<3>",super().move_right)
        self.canvas.bind_all("<4>",super().rotate_left)
        self.canvas.bind_all("<6>",super().rotate_right)
        self.canvas.bind_all("<2>",super().drop_to_bottom)

def clear_full_row():
    pass

async def draw_windows(game):
    await game.canvas.create_rectangle(50,50,500,950)
    await game.canvas.create_rectangle(1000,50,1450,950)
    await game.canvas.create_rectangle(515,50,740,275)
    await game.canvas.create_rectangle(760,50,985,275)
    await game.canvas.create_rectangle(515,300,740,450)
    await game.canvas.create_rectangle(760,300,985,450)

async def player1(name,game):
    player1 = Player1(player1_name,game.canvas)
    await asyncio.sleep(5)

async def player2(name,game):
    player2 = Player2(player2_name,game.canvas)
    await asyncio.sleep(5)
    loop.stop()

async def update(game):
    while True:
        game.tk.update_idletasks()
        game.tk.update()
        await asyncio.sleep(0.01)

if __name__ =="__main__":
    g = Game()
    player1_name = sys.argv[1]
    player2_name = sys.argv[2]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(draw_windows(g))
    loop.create_task(player1(player1_name,g))
    loop.create_task(player2(player2_name,g))
    loop.create_task(update(g))
    loop.run_forever()

#a = Blocks("blocks.dat")
#print(a.blocks)
#for i in range(10):
#    print(a.pick())