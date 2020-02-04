from asynctk import *
import random
import time
import sys
import collections
import asyncio
import itertools

colors = ["red","green","blue","yellow"]
current_blocks = [None,None]
current_ids = [[],[]]
LEFT = 0
RIGHT = 1
Block = collections.namedtuple("Block","shape color")
windows = [{},{}]
scores = [0,0]
done = [False,False]
text = None

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
        self.running = False
        self.blocks = blocks
        # bind start and stop
        self.tk.bind("<Return>",self.start)
        self.tk.bind("<Escape>",self.stop)

    def start(self,evt):
        global text,current_blocks,current_ids,windows,scores
        self.running = True
        self.canvas.delete(text)
        text = None

    def stop(self,evt):
        if self.running:
            self.running = False
        else:
            loop.stop()
            sys.exit(0)

class Player:
    window = None
    small_window_offset = ((530,110),(775,110))
    main_window_offset = ((50,50),(1000,50))
    score_window_offset = ((627,337),(872,337))
    def __init__(self,name):
        self.bind_keys = (("<w>","<a>","<s>","<d>"), \
        ("<KeyPress-Up>","<KeyPress-Left>","<KeyPress-Down>","<KeyPress-Right>"))
        self.funcs = (self.rotate,self.move_left,self.drop_to_bottom,self.move_right)
        self.name = name
        self.lines = 0
        self.dropping = True
        self.speed = 0.5
        self.x = 0
        self.rotate = 0
        self.fall = 0
        self.keys = self.bind_keys[self.window]
        for key, func in zip(self.keys,self.funcs):
            canvas.bind_all(key,func)

    async def play(self):
        global text
        offset = self.score_window_offset[self.window]
        global current_blocks, colors, scores, done

        await canvas.create_text(*self.score_window_offset[self.window],\
            text=self.name,font=("Calibri",35))
        self.score = await canvas.create_text(offset[0],offset[1]+75,\
            text="0",font=("Calibri",35))
        await self.show_score()
        shape = game.blocks.pick()
        next_block = Block(shape,colors[-1])
        ids = await self.show_next_block(next_block)
        while True:
            if game.running and (not done[self.window]):
                for color in itertools.cycle(colors):
                    current_blocks[self.window] = next_block
                    game.canvas.delete(*ids)
                    shape = game.blocks.pick()
                    next_block = Block(shape,color)
                    ids = await self.show_next_block(next_block)
                    await self.move()
                    windows[self.window].update(self.final_pos)
                    self.clear_full_row()
                    await self.show_score()
                    status = self.check()
                    if status:
                        canvas.delete(*ids)
                        self.lines = 0
                        done[self.window] = True
            elif done[self.window]:
                await asyncio.sleep(0.005)
            else:
                if not text:
                    text = await canvas.create_text(700,500,text="Press Enter to start\nPress Esc to exit/pause game",font=("Calibri",50))
                await asyncio.sleep(0.005)

    async def show_next_block(self,next_block):
        ids = []
        for a in range(len(next_block.shape)):
            for b in range(len(next_block.shape[a])):
                if next_block.shape[a][b]:
                    x1 = self.small_window_offset[self.window][0] + b*45
                    y1 = self.small_window_offset[self.window][1] + a*45
                    x2 = x1 + 45
                    y2 = y1 + 45
                    id = await canvas.create_rectangle(x1,y1,x2,y2,fill=next_block.color)
                    ids.append(id)
        return ids

    async def move(self):
        self.final_pos = {}
        global current_ids, current_blocks
        raw_ids = []
        ids = []
        tmp_ids = []
        # draw the block
        current_ids[self.window] = []
        if game.running and (not done[self.window]):
            for a in range(len(current_blocks[self.window].shape)):
                for b in range(len(current_blocks[self.window].shape[a])):
                    if current_blocks[self.window].shape[a][b]:
                        x = 3
                        y = 0
                        x1 = self.main_window_offset[self.window][0] + b*45 + x*45
                        y1 = self.main_window_offset[self.window][1] + a*45 + y*45
                        x2 = x1 + 45
                        y2 = y1 + 45
                        id = (await canvas.create_rectangle(x1,y1,x2,y2,fill=current_blocks[self.window].color), \
                            (b+x,a+y))
                        current_ids[self.window].append(id)
        self.dropping = True
        self.speed = 0.5
        while self.dropping:
            if self.x == 1:
                self.x = 0
                for id, (x,y) in current_ids[self.window]:
                    if (x + 1 > 9) or windows[self.window].get((x+1,y)):
                        break
                else:
                    tmp_ids = []
                    for id, (x,y) in current_ids[self.window]:
                        canvas.move(id,45,0)
                        tmp_ids.append((id,(x+1,y)))
                    current_ids[self.window] = tmp_ids
            if self.x == -1:
                self.x = 0
                for id, (x,y) in current_ids[self.window]:
                    if x - 1 < 0 or windows[self.window].get((x-1,y)):
                        break
                else:
                    tmp_ids = []
                    for id, (x,y) in current_ids[self.window]:
                        canvas.move(id,-45,0)
                        tmp_ids.append((id,(x-1,y)))
                    current_ids[self.window] = tmp_ids

            if self.fall == 1:
                self.fall = 0
                # fall quickly (sleep for 0.005s)
                self.speed = 0.001
            
            if self.rotate == 1:
                self.rotate = 0
                ref = current_ids[self.window][0][1]
                
                # Calculate the new position based on the reference point
                x_dist = -ref[1]-1-ref[0]
                y_dist = ref[0]-ref[1]
                # Recalculate all points to real position
                raw_ids = []
                for id, (x,y) in current_ids[self.window]:
                    # clockwise rotation
                    new_x = -y-1-x_dist
                    new_y = x-y_dist
                    raw_ids.append((id,(new_x,new_y)))
                # check if it is out of boundary
                ids = [id for id, (x,y) in raw_ids]
                xs = [x for id, (x,y) in raw_ids]
                ys = [y for id, (x,y) in raw_ids]
                if min(xs) < 0:
                    xs = [x-min(xs) for x in xs]
                if max(xs) > 9:
                    xs = [x-max(xs)+9 for x in xs]
                if min(ys) < 0:
                    ys = [y-min(ys) for y in ys]
                if max(xs) > 19:
                    ys = [y-max(ys)+19 for y in ys]
                # Detect if current block collides with other blocks
                for id, x, y in zip(ids,xs,ys):
                    if windows[self.window].get((x,y)):
                        break
                else:
                    tmp_ids = []
                    for id, x, y in zip(ids,xs,ys):
                        canvas.moveto(id,\
                            self.main_window_offset[self.window][0]+x*45,\
                            self.main_window_offset[self.window][1]+y*45)
                        tmp_ids.append((id,(x,y)))
                    current_ids[self.window] = tmp_ids
            await asyncio.sleep(0.005)

    async def drop(self):
        global current_ids, windows
        while True:
            if game.running and current_ids[self.window] and self.dropping:
                await asyncio.sleep(self.speed)
                for id, (x,y) in current_ids[self.window]:
                    # await asyncio.sleep(0.01)
                    # check if hit bottom
                    if windows[self.window].get((x,y+1)) or y == 19:
                        self.dropping = False
                        self.final_pos = {(x,y):id for (id, (x,y)) in current_ids[self.window]}
                        break
                else:
                    # drop one step
                    for id, (x,y) in current_ids[self.window]:
                        canvas.move(id,0,45)
                    current_ids[self.window] = [(id,(x,y+1)) for (id,(x,y)) in current_ids[self.window]]
            else:
                await asyncio.sleep(0.01)

    def move_left(self,evt):
        self.x = -1

    def move_right(self,evt):
        self.x = 1

    def rotate(self,evt):
        self.rotate = 1

    def drop_to_bottom(self,evt):
        self.fall = 1

    def clear_full_row(self):
        global windows, scores
        deleted_lines = []
        xy = windows[self.window].keys()
        y_values = [y for (x,y) in xy]
        counter = collections.Counter(y_values)
        tmp_window = {}
        # collect all lines that need to be deleted
        for line in counter.keys():
            if counter[line] == 10:
                deleted_lines.append(line)
        deleted_lines = sorted(deleted_lines)
        length = len(deleted_lines)
        self.lines += int(length*(length+1)/2)
        scores[self.window] = self.lines
        for line in deleted_lines:
            tmp_window = {}
            for (x,y),id in windows[self.window].items():
                # Delete the line
                if y == line:
                    canvas.delete(id)
                # Move the lines above down
                elif y < line:
                    canvas.move(id,0,45)
                    tmp_window[(x,y+1)] = id
                # Do nothing for lines below
                else:
                    tmp_window[(x,y)] = id
            windows[self.window] = tmp_window
    
    async def show_score(self):
        canvas.delete(self.score)
        offset = self.score_window_offset[self.window]
        self.score = await canvas.create_text(offset[0],offset[1]+75,\
            text=str(self.lines),font=("Calibri",35))
    
    def check(self):
        for x, y in windows[self.window].keys():
            if y == 0:
                return True
        return False

class Player1(Player):
    window = LEFT

class Player2(Player):
    window = RIGHT

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

async def decide_winner():
    global text, done
    while True:
        if all(done):
            msg = "{} has won!"
            if scores[0] == scores[1]:
                winner = "Nobody"
            else:
                winner = player1.name if scores[0] > scores[1] else player2.name
            text = await canvas.create_text(700,500,text=msg.format(winner),font=("Calibri",50))
            game.running = False
            await asyncio.sleep(3)
            loop.stop()
            sys.exit(0)

        await asyncio.sleep(0.005)

if __name__ =="__main__":
    if len(sys.argv) != 3:
        print("Usage:python game.py player1_name player2_name")
        sys.exit(1)
    blocks = Blocks()
    game = Game(blocks)
    canvas = game.canvas
    name1 = sys.argv[1]
    name2 = sys.argv[2]
    player1 = Player1(name1)
    player2 = Player2(name2)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(draw_windows())
    loop.create_task(player1.play())
    loop.create_task(player2.play())
    loop.create_task(player1.drop())
    loop.create_task(player2.drop())
    loop.create_task(update())
    loop.create_task(decide_winner())
    loop.run_forever()
