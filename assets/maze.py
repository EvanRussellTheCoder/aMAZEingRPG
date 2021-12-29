from MazeRoom import Room
from random import choice


# made by James Nelson after 20 hours of trying to get it working
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_cells = [Room(wid, hig) for hig in range(height) for wid in range(width)]  # make a bunch of rooms
        self.stack = []

    def checkNeighbors(self, room):
        neighbors = []
        top = self.check_room(room.getCoordinates()[0], room.getCoordinates()[1] - 1)
        right = self.check_room(room.getCoordinates()[0] + 1, room.getCoordinates()[1])
        bottom = self.check_room(room.getCoordinates()[0], room.getCoordinates()[1] + 1)
        left = self.check_room(room.getCoordinates()[0] - 1, room.getCoordinates()[1])
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        # print(neighbors)
        return choice(neighbors) if neighbors else False

    def check_room(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return self.grid_cells[x + y * self.width]

    def makedoor(self, current, next):
        dx = current.getCoordinates()[0] - next.getCoordinates()[0]
        if dx == 1:
            current.Doors[3] = True
            next.Doors[1] = True
        if dx == -1:
            current.Doors[1] = True
            next.Doors[3] = True
        dy = current.getCoordinates()[1] - next.getCoordinates()[1]
        if dy == 1:
            current.Doors[0] = True
            next.Doors[2] = True
        if dy == -1:
            current.Doors[2] = True
            next.Doors[0] = True

    def randomGenerate(self):

        current_room = self.grid_cells[0]  # RANDOM NUMBER WORKS TOO
        # print(current_room)
        generating = self.width * self.height * 2  # iterates over the whole maze twice
        for i in range(2 * len(self.grid_cells)):

            current_room.visited = True

            next_room = self.checkNeighbors(current_room)
            if next_room:
                next_room.visited = True
                self.stack.append(current_room)
                self.makedoor(current_room, next_room)
                current_room = next_room
            elif self.stack:
                current_room = self.stack.pop()

