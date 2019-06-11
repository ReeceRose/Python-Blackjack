#-------------------------------------------------------------------------------
# Name:        Button
# Purpose:
#
# Author:      Reece
#
# Created:     22/09/2015
#-------------------------------------------------------------------------------

from graphics import *
from random import randint
from time import sleep

class Button:
    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it"""

    def __init__(self, win, center, width, height, label, colour):
        """Creates a rectangular button, eg:
            qb = Button(myWin, centerPoint, width, height, 'Quit'."""
        w,h = width / 2.0, height / 2.0
        x,y = center.getX(), center.getY()

        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h

        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)

        self.rect = Rectangle(p1,p2)
        self.rect.setFill(colour)
        self.rect.setOutline("black")
        self.rect.draw(win)

        self.label = Text(center, label)
        self.label.setSize(16)
        self.label.draw(win)
        self.activate()

    def clicked(self, p):
        "Returns true if button activate and p is inside"
        return(self.active and self.xmin <= p.getX() <= self.xmax
            and self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def setLabel(self, text):
        "Sets the label of the button"
        self.label.setText(text)

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill("gray90")
        self.rect.setWidth(1)
        self.active = False

    def undraw(self):
        "Undraw the button and label"
        self.rect.undraw()
        self.label.undraw()

    def draw(self, window):
        "Draw the button and label"
        self.rect.draw(window)
        self.label.draw(window)