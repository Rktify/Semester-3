import pygame
from tkinter import messagebox, Tk
import sys
import tracemalloc
import time

width, height = 600, 600
columns, rows = 30, 30
window = pygame.display.set_mode((width, height))

pixelwidth = width // columns
pixelheight = height // rows

grid = []
queue = []
pathing = []

class Box:
    def __init__ (self, i, j):
        self.x = i
        self.y = j
        self.obstacle = False
        self.start = False
        self.end = False
        self.obstaclestatus = False
        self.next = False
        self.visited = False
        self.neighbours = []
        self.path = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * pixelwidth, self.y * pixelheight, pixelwidth - 2, pixelheight - 2))
    
    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)
    
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()


def main():
    global elapsed, memory
    search = False
    endboxstatus = False
    startboxstatus = False
    searching = True
    endzone = None
    finish = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                i = x // pixelwidth
                j = y // pixelheight
                if event.buttons[0] and not grid[i][j].obstaclestatus and not startboxstatus:
                    start_box = grid[i][j]
                    start_box.start = True
                    startboxstatus = True
                    grid[i][j].visited = True
                    queue.append(grid[i][j])
                if event.buttons[0] and endboxstatus and startboxstatus and not finish:
                    grid[i][j].obstacle = True
                    grid[i][j].obstaclestatus = True
                if event.buttons[2] and not endboxstatus and not grid[i][j].obstaclestatus:
                    endzone = grid[i][j]
                    endzone.end = True           
                    endboxstatus = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and searching and not finish:
                    for i in range(columns):
                        for j in range(rows):
                            box = grid[i][j]
                            if box.obstacle:
                                box.obstacle = False
                                box.obstaclestatus = False
                if event.key == pygame.K_SPACE and endboxstatus and not finish:
                    for i in range(columns):
                        for j in range(rows):
                            box = grid[i][j]
                            if box.end:
                                box.end = False
                                endboxstatus = False
                if event.key == pygame.K_r:
                    for i in range(columns):
                        for j in range(rows):
                            box = grid[i][j]
                            box.obstacle = False
                            box.obstaclestatus = False
                            box.end = False
                            box.next = False
                            box.visited = False
                            box.start = False
                            box.path = None
                            endboxstatus = False
                            startboxstatus = False
                            finish = False
                            searching = True
                            search = False
                            queue.clear()
                            pathing.clear()
                            
                
                if event.key == pygame.K_LCTRL:
                    if event.key == pygame.K_w:
                        pygame.quit()
                        sys.exit()
                            
            if event.type == pygame.KEYDOWN and endboxstatus:
                if event.key == pygame.K_RETURN:
                    timestart = time.time()
                    search = True 
        if search:
            tracemalloc.start()
            if len(queue) > 0 and searching:
                currentpixel = queue.pop(0)
                currentpixel.visited = True
                if currentpixel == endzone:
                    searching = False
                    finish = True
                    while currentpixel.path != start_box:
                        pathing.append(currentpixel.path)
                        currentpixel = currentpixel.path
                        
                else:
                    for i in currentpixel.neighbours:
                        if not i.next and not i.obstacle:
                            i.next = True
                            i.path = currentpixel
                            queue.append(i)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("pls", "NO PATH!!!!!!!!!!!!")
                    searching = False
                    finish = True
        
        if finish:
            search = False
            timeend = time.time()
            elapsed = timeend - timestart
            currentmemory, memorypeak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            queue.clear()
            Tk().wm_withdraw()
            messagebox.showinfo("Time and memory", f"Time: %.2fs  | Memory: {memorypeak} bytes" % elapsed)

            finish = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (221, 221, 221))
                if box.next:
                    box.draw(window, (0, 0, 255))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box.start and not box.end:
                    box.draw(window, (0, 200, 200))
                if box.obstacle and not box.start and not box.end:
                    box.draw(window, (255, 255, 0))
                if box in pathing:
                    box.draw(window, (0, 0, 0))
                if box.end and not box.start:
                    box.draw(window, (255, 0, 0))
        
        pygame.display.flip()
        pygame.display.set_caption("Dijkstra Algorithm Visualization")
        

main()





#add the path itself T..T
#add a reset with the same map
#add the runtime
#maybe add more messageboxes if error or how to

#MAKE MORE ALGORITHMS

#Find bugs