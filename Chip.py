#-------------------------------------------------------------------------------
# Name:        Chip
# Purpose:
#
# Author:      Reece
#
# Created:     22/09/2015
#-------------------------------------------------------------------------------

from graphics import *
from random import randint
from time import sleep

class Chip:
    """A chip that is a clickable Circle object with an image overtop.
    """

    def __init__(self, win, center, r, amount, colour):
        """Creates a circular chip, eg:
            oneChip = Chip(myWin, centerPoint, radius, amount, "image location.gif")"""
        self.x, self.y = center.getX(), center.getY()
        self.r = r
        self.amount = amount

        self.circle = Circle(center, r)
        self.circle.setFill(colour)
        self.circle.setOutline("white")
        self.circle.draw(win)

        self.text = Text(center, amount)
        self.text.setSize(14)
        self.text.setStyle("bold")
        self.text.draw(win)

    def clicked(self, p):
        "Returns true if button activate and p is inside"
        return((self.x + self.r) >= p.getX() and (self.x - self.r) <= p.getX()
            and (self.y + self.r) >= p.getY() and (self.y - self.r) <= p.getY())

    def undraw(self):
        "Undraw the button and label"
        self.circle.undraw()
        self.text.undraw()

    def getAmount(self):
        return self.amount