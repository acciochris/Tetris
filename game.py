from asynctk import *
import random
import time
import sys
import collections
import asyncio
import itertools

colors = ["red","green","blue","yellow"]
current_blocks = [None,None]
LEFT = 0
RIGHT = 1
Block = collections.namedtuple("Block","shape color")

class Blocks:
    def __init__(self):
        self.blocks = [[[1, 1, 1, 1]], \
            [[1, 1, 1], [0, 0, 1]], \
            [[1, 1, 1], [1]], \
            [[1, 1], [0, 1, 1]], \
            [[0, 1, 1], [1, 1]], \
            [[1, 1], [1, 1]], \
            [[1, 1, 1], [0, 1]]]
    def pick(self):
        block = self.blocks[random.randrange(len(self.blocks))]
        return block

class Game:
    def __init__(self,blocks):
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
        self.blocks = blocks
        # bind start and stop
        self.tk.bind("<Return>",self.start)
        self.tk.bind("<Escape>",self.stop)

    def start(self,evt):
        self.running = True

    def stop(self,evt):
        self.running = False

class Player:
    window = None
    offset = ((530,110),(775,110))
    def __init__(self,name):
        self.bind_keys = (("<w>","<a>","<s>","<d>"), \
        ("<KeyPress-Up>","<KeyPress-Left>","<KeyPress-Down>","<KeyPress-Right>"))
        self.funcs = (self.rotate,self.move_left,self.drop_to_bottom,self.move_right)
        self.offset = ((530,110),(775,110))
        self.name = name
        self.lines = 0
        self.keys = self.bind_keys[self.window]
        for key, func in zip(self.keys,self.funcs):
            canvas.bind_all(key,func)
    async def play(self):
        for color in itertools.cycle(colors):
            shape = game.blocks.pick()
            global current_blocks
            current_blocks[self.window] = Block(shape,color)
            ids = await self.show_next_block()
            await asyncio.sleep(5)
            game.canvas.delete(*ids)
    def move_left(self,evt):
        pass
    def move_right(self,evt):
        pass
    def rotate(self,evt):
        pass
    def drop_to_bottom(self,evt):
        pass
    async def show_next_block(self):
        ids = []
        for a in range(len(current_blocks[self.window].shape)):
            for b in range(len(current_blocks[self.window].shape[a])):
                if current_blocks[self.window].shape[a][b] == 1:
                    x1 = self.offset[self.window][0] + b*45
                    y1 = self.offset[self.window][1] + a*45
                    x2 = x1 + 45
                    y2 = y1 + 45
                    #print(x1,x2,y1,y2)
                    id = await canvas.create_rectangle(x1,y1,x2,y2,fill=current_blocks[self.window].color)
                    ids.append(id)
        return ids

    def drop(self):
        pass

class Player1(Player):
    window = LEFT

class Player2(Player):
    window = RIGHT

def clear_full_row():
    pass

async def draw_windows():
    # main windows
    await canvas.create_rectangle(50,50,500,950)
    await canvas.create_rectangle(1000,50,1450,950)
    # next blocks
    await canvas.create_rectangle(515,50,740,275)
    await canvas.create_rectangle(760,50,985,275)
    # line windows
    await canvas.create_rectangle(515,300,740,450)
    await canvas.create_rectangle(760,300,985,450)

async def update():
    while True:
        game.tk.update_idletasks()
        game.tk.update()
        await asyncio.sleep(0.01)

if __name__ =="__main__":
    if len(sys.argv) != 3:
        print("Usage:python game.py player1_name player2_name")
        sys.exit(1)
    blocks = Blocks()
    g = Game(blocks)
    game = g
    canvas = g.canvas
    name1 = sys.argv[1]
    name2 = sys.argv[2]
    player1 = Player1(name1)
    player2 = Player2(name2)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(draw_windows())
    loop.create_task(player1.play())
    loop.create_task(player2.play())
    loop.create_task(update())
    loop.run_forever()

#a = Blocks("blocks.dat")
#print(a.blocks)
#for i in range(10):
#    print(a.pick())