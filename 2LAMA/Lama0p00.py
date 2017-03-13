#LAMA0p00#

################################################################################
import tkinter
import random
import time

TILES = 5
WIDTH = 50 # 1 tile is 50 pixels high and wide
RANDSTEPS=25


window = tkinter.Tk()
canvas = tkinter.Canvas(window, height=TILES*WIDTH, width=TILES*WIDTH,bg='green')
canvas.pack()

lightMatrix = [[0 for i in range(TILES)] for j in range(TILES)]
tileIdMatrix = [[0 for i in range(TILES)] for j in range(TILES)]
print(lightMatrix)

def createTiles():
    for ix in range(TILES):
        for iy in range(TILES):
            tileIdMatrix[ix][iy]=canvas.create_rectangle(ix*WIDTH, iy*WIDTH, (ix+1)*WIDTH, (iy+1)*WIDTH  )

def randomize():
    for i in range(RANDSTEPS):
        randIX = random.randint(0,TILES-1)
        randIY = random.randint(0,TILES-1)
        print("randomize", randIX, randIY)
        reactToClick(randIX,randIY)
        colorTiles()
        window.update()
        time.sleep(.1)
        
def colorTiles():
    for ix in range(TILES):
        for iy in range(TILES):
            fillColor = "red"
            if lightMatrix[ix][iy] is 1:
                fillColor = "green"
            canvas.itemconfig(tileIdMatrix[ix][iy], fill=fillColor  )

def switchColor(ix,iy):
    lightMatrix[ix][iy] = (lightMatrix[ix][iy]+1)%2

def reactToClick(ix, iy):
    print("react", ix, iy)
    switchColor(ix,iy)
    if ix-1>=0:
        switchColor(ix-1,iy)
    if ix+1<TILES:
        switchColor(ix+1,iy)
    if iy-1>=0:
        switchColor(ix,iy-1)
    if iy+1<TILES:
        switchColor(ix,iy+1)
    
def mouseClick(event):
    ix = event.x // WIDTH
    iy = event.y // WIDTH
    reactToClick(ix, iy)
    colorTiles()
    
createTiles()
randomize()
colorTiles()
canvas.bind('<Button>', mouseClick)
    
tkinter.mainloop()
