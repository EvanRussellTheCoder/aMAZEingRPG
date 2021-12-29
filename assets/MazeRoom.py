from typing import List
from Event import EventType

# for testing purposes
class Mazeobject:
    def __init__(self, Dime: int):

        dimensions = Dime
        # self.arr = [[0]*dimensions]*dimensions
        self.arr = [[0, 1, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 1, 0, 1, 0],
                    [1, 1, 1, 1, 0],
                    [1, 0, 0, 0, 0]]
        for i in range(dimensions):
            print(self.arr[i])

    def getMaze(self):
        return self.arr

    def roomExists(self, x, y):
        if (x < 0 or y < 0):
            return False
        doorcheck = self.arr[y][x]
        if (self.arr[y][x] == 1):
            return True
        else:
            return False


class Room:
    def __init__(self, x, y):
        self._XPosition = x
        self._YPosition = y
        self._RoomValue = 0
        self._RoomType = "None"
        self.Doors = [False, False, False, False]
        self.visited = False

    # Setter for the doors
    def WhatDoorsExistFromThisRoomIn(self, Maze):  # pass in maze type object 2d array?
        if Maze.roomExists(self._XPosition, self._YPosition - 1):  # north

            self._Doors[0] = True
        if Maze.roomExists(self._XPosition + 1, self._YPosition):  # east

            self._Doors[1] = True
        if Maze.roomExists(self._XPosition, self._YPosition + 1):  # south

            self._Doors[2] = True
        if Maze.roomExists(self._XPosition - 1, self._YPosition):  # west

            self._Doors[3] = True

    def IveBeenHere(self):
        """Sets the VistedBefore variable to True"""
        self._VisitedBefore = True

    def getRoomType(self) -> str:
        """:returns string with the type of room"""
        return self._RoomType

    def setRoomType(self, roomtype: str):
        self._RoomType = roomtype

    def getRoomValue(self) -> int:
        """:returns integer value to determine Room event"""
        return self._RoomValue

    def theRoomValueIs(self, Value: int):
        self._RoomValue = Value

    def getDoors(self) -> List[bool]:
        """:returns List of 4 bools [North, East, South, West]"""
        return self._Doors

    def setDoors(self, newdoors):
        self._Doors = newdoors

    def getCoordinates(self) -> [int, int]:
        return [self._XPosition, self._YPosition]

    def haveIBeenHere(self) -> bool:
        return self._VisitedBefore

