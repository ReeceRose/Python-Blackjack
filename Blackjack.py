#-------------------------------------------------------------------------------
# Name:        Blackjack
#
# Author:      Reece
#
# Created:     16/09/2015
# Copyright:   (c) Reece 2015
#-------------------------------------------------------------------------------
from graphics import *
from Button import *
from time import sleep
from Chip import *
from tkinter.commondialog import Dialog

def main(intro, name):
    try:
        window = graphics()
        name = menu(window, intro, name)
    except GraphicsError:
        window.close()

def graphics():
    window = GraphWin("BlackJack", 800, 800)
    window.setBackground("black")
    return window

def menu(window, intro, name):
    #Initial intro. With animations
    if(intro):
        image = Image(Point(400, 400), "Images/bg.gif")
        image.draw(window)
        img = image.clone()
        img.draw(window)
        sleep(0.5)
        for i in range(25):
            img.move(0, i)
            image.move(0, i * -1)
            sleep(0.025)
        sleep(0.25)
    else:
        image = Image(Point(400, 100), "Images/bg.gif")
        img = Image(Point(400, 700), "Images/bg.gif")
        drawObject(window, image, img)
    #If the user has already played a round, skip all the intros (But draw the Blackjack logo) and get the users bet
    if(len(name) >= 1):
        balance = getProfile(name)
        undraw(img)
        game(window, name, balance)
        return name
    #User face buttons
    deal = Button(window, Point(400, 250), 150, 75, "DEAL", "dodgerblue2")
    option = Button(window, Point(400, 350), 150, 75, "OPTIONS", "dodgerblue2")
    stats = Button(window, Point(400, 450), 150, 75, "STATS", "dodgerblue2")
    quit = Button(window, Point(400, 550), 150, 75, "QUIT", "dodgerblue2")
    while(True):
        click = window.getMouse()
        if(deal.clicked(click)):
            undraw(deal, option, stats, quit)
            if(name == ""):
                #If it's the first time running, get users name to load profile
                name = getName(window)
            undraw(img)
            while(True):
                #Repeat the game until; player quits.
                game(window, name)
            break
        elif(option.clicked(click)):
            undraw(deal, option, stats, quit)
            #Option window
            options(window)
            drawObject(window, deal, option, stats, quit)
        #Load the all-time highscores
        elif(stats.clicked(click)):
            undraw(deal, option, stats, quit)
            getHighscores(window)
            drawObject(window, deal, option, stats, quit)
        #Quit the game
        elif(quit.clicked(click)):
            break
    window.close()
    return name

#Save the shoe size set by the user
def saveShoe(size):
    #If it's less than one or greater than 5. Set it to the default (5)
    if(size > 5 or size < 1):
        size = 5
    file = open("shoe size.dat", "w+")
    file.write(str(size))
    file.close()

#Load the shoe size
def getShoe():
    file = open("shoe size.dat", "w+")
    size = file.readline()
    #If the file is empty or shoe size is 0, set to the default (5)
    if(size == "" or size == "0"):
        file.write("5")
        size = 5
    file.close()
    return size

def options(window):
    box = Rectangle(Point(200, 200), Point(600, 600))
    box.setFill("white")
    box.draw(window)
    name = Text(Point(400, 375), "SHOE SIZE")
    name.draw(window)
    shoe = Entry(Point(400, 400), 15)
    shoe.draw(window)
    returnButton = Button(window, Point(400, 500), 100, 75, "RETURN", "dodgerblue2")
    while(True):
        click = window.getMouse()
        #If they want to return to the menu, and save the shoe size
        if(returnButton.clicked(click)):
            try:
                shoeSize = int(shoe.getText())
            except:
                shoeSize = 5
                shoe.setText(5)
                continue
            undraw(box, name, shoe, returnButton)
            break
    saveShoe(shoeSize)

def getProfile(name):
    #Try to load the profile
    #If file is empty or 0, set to default of 500
    try:
        file = open("profiles/"+name+".dat", "r")
        balance = file.readline()
        file.close()
        if(balance == "" or balance == "0"):
            file = open("profiles/"+name+".dat", "w")
            file.write("500")
            file.close()
            balance = 500
    #If file doesn't exist. Create a new file
    except IOError:
        file = open("profiles/"+name+".dat", "w+")
        file.write("500")
        file.close
        balance = 500
    return int(float(balance) // 1)

#Update the users balance
def updateProfile(name, balance):
    file = open("profiles/"+name+".dat", 'w')
    file.write(str(balance))
    file.close()

#Undraw all objects thar are passed
def undraw(*Objects):
    for i in Objects:
        i.undraw()

#Draw all objects that are passed
def drawObject(window, *Objects):
    for i in Objects:
        i.draw(window)

#Get the users name
def getName(window):
    text = Entry(Point(400, 400), 20)
    text.setFill("dodgerblue2")
    text.draw(window)
    play = Button(window, Point(400, 500), 75 ,50, "NEXT", "dodgerblue2")
    title = Text(Point(400, 375), "ENTER YOUR NAME")
    title.setFill("white")
    title.draw(window)
    while(True):
        click = window.getMouse()
        #Make sure the text isn't empty then return.
        if(play.clicked(click) and text.getText() != ""):
            undraw(text, play, title)
            return text.getText()

#Return a list of all the cards (52 * shoeSize)
def getCards():
    cards = []
    for i in range(int(getShoe())):
        for j in range(52):
            cards.append(Image(Point(780, 400), "images/"+str(j+1)+".gif"))
    return cards

#Main game function
def game(window, name):
    dealerX = 250
    userX = 250
    firstUserX = 250
    #Split variables
    secondUserX = 550
    resultTwo = False
    reasonTwo = False
    canHitTwo = True
    #Window/Game setup
    #Total hands
    hands = 1
    #Current hand
    hand = 1
    balance = getProfile(name)
    bet = getBet(window, balance)
    balance = balance - bet
    updateProfile(name, balance)
    deck = Image(Point(780, 400), "images/back.gif")
    deck.draw(window)
    cards = getCards()
    usedCards = []
    dealerText = Text(Point(400, 350), "Dealer Score\n{0}".format(0))
    dealerText.setFill("white")
    dealerText.draw(window)
    playerText = Text(Point(400, 450), "Your Score\n{0}".format(0))
    playerText.setFill("white")
    playerText.draw(window)
    card1, usedCards, uScore = getCard(cards, usedCards, 0)
    card2, usedCards, dHiddenScore = getCard(cards, usedCards, 0)
    card3, usedCards, uTwoScore = getCard(cards, usedCards, 0)
    card4, usedCards, dScore = getCard(cards, usedCards, 0)
    uScore += uTwoScore
    uScoreTwo = 0
    decks = initialDeal(window, deck, card1, card2, card3, card4)
    playerText.setText("Your Score\n{0}".format(uScore))
    dealerText.setText("Dealer Score\n{0}".format(dScore))
    hit = Button(window, Point(100, 700), 100, 75, "HIT", "dodgerblue2")
    stand = Button(window, Point(300, 700), 100, 75, "STAND", "dodgerblue2")
    split = Button(window, Point(500, 700), 100, 75, "SPLIT", "dodgerblue2")
    dd = Button(window, Point(700, 700), 100, 75, "DOUBLE\nDOWN", "dodgerblue2")
    initialResult = checkBlackjack(uScore, dScore + dHiddenScore)
    insured = False
    drawn = True

    #If somehow 2 aces equal 22, set the score to 12.
    if(uScore == 22):
        uScore == 12
    if(dScore + dHiddenScore == 22):
        if(dHiddenScore == 11):
            dScore = 1
        else:
            dHiddenScore = 1
    #If the dealer is showing an ace. Ask the user if they'd like to buy insurance
    if(dScore == 11 and uScore != 21):
        #If they want to buy insurance
        if(askyesno("Insurance", "Would you like to buy insurance?")):
            #If they don't have enough money
            if(balance < bet/2):
                showerror("Error", "Couldn't buy insurance.\nNot enough money")
            else:
                insured = True
                updateProfile(name, balance - (bet // 2))
    #If there's not an initial blackjack play the game
    if(not initialResult):
        canHit = True
        canSplit = True
        while(True):
            click = window.getMouse()
            if(hit.clicked(click)):
                #Check which hand a card should go to if they player has split
                if(hand == 1 and canHit):
                    usedCards, uScore, firstUserX = userHit(window, cards, usedCards, uScore, firstUserX)
                if(hand == 2 and canHitTwo):
                    usedCards, uScoreTwo, secondUserX = userHit(window, cards, usedCards, uScoreTwo, secondUserX)
                canSplit = False
            elif(stand.clicked(click)):
                canHit = False
                #If they haven't split, let the dealer play.
                if(hands == 1):
                    decks.undraw()
                    dealerText.setText("Dealer Score\n{0}".format(dScore + dHiddenScore))
                    usedCards, dScore, dealerX = dealerHit(dScore, dHiddenScore, cards, usedCards, dealerX, dealerText, window)
                else:
                    #Standing on their first hand
                    if(hand == 1):
                        hand = 2
                    #Standing on their second hand. Ends game
                    else:
                        hand = 3
                        canHitTwo = False
                        drawn = False
                        decks.undraw()
                        usedCards, dScore, dealerX = dealerHit(dScore, dHiddenScore, cards, usedCards, dealerX, dealerText, window)
                        break
            elif(split.clicked(click) and canSplit):
                res = checkSplit(uScore - uTwoScore, uTwoScore, usedCards)
                #If the user can split
                if(res):
                    #Checks balance
                    if(balance - bet > 0):
                        updateProfile(name, balance - bet)
                        hands = 2
                        #Move cards over and setup multiple scores
                        move(card3, 0, secondUserX - 250)
                        uScore = uScore // 2
                        uScoreTwo = uScore
                        firstUserX -= 75
                        #Add two cards. One to each hand
                        usedCards, uScore, firstUserX = userHit(window, cards, usedCards, uScore, firstUserX)
                        usedCards, uScoreTwo, secondUserX = userHit(window, cards, usedCards, uScoreTwo, secondUserX)
                    else:
                        showerror("Error", "Couldn't split.\nCouldn't match bet")
                        canSplit = False
                else:
                    canSplit = False
                    showerror("Error", "Couldn't split cards")
            elif(dd.clicked(click) and canHit):
                #Can't split
                if(balance < bet):
                    showerror("Error", "Can't double down.\nNot enough money")
                else:
                    #Add the card to the players hand and double the bet
                    usedCards, uScore, firstUserX = userHit(window, cards, usedCards, uScore, firstUserX)
                    balance = balance - bet
                    updateProfile(name, balance)
                    bet *= 2
                    canHit = False
                    canSplit = False
            if(hands == 1):
                playerText.setText("Your Score\n{0}".format(uScore))
            else:
                playerText.setText("Your Score\n{0} | {1}".format(uScore, uScoreTwo))
            #If dealer hasn't hit
            if(dScore + dHiddenScore < 17 and not canHit and not canHitTwo):
                usedCards, dScore, dealerX = dealerHit(dScore, dHiddenScore, cards, usedCards, dealerX, dealerText, window)
            #If users haven't split
            if(hands == 1):
                result, reason = checkGame(uScore, dScore + dHiddenScore, canHit)
            else:
                #Check the first hand
                if(hand == 1):
                    result, reason = checkGame(uScore, dScore + dHiddenScore, canHit)
                #Check the second hand
                else:
                    result, reason = checkGame(uTwoScore, dScore + dHiddenScore, canHit)
            #Second hand checks
            if(uScoreTwo >= 21):
                if(uScoreTwo == 21):
                    resultTwo = "WIN"
                    reasonTwo = "You hit 21!"
                else:
                    resultTwo = "LOSE"
                    reasonTwo = "You've busted"
                break
            if(result != False and reason != False):
                #Player busts/wins on the first hand, continue to next hand
                if(hands == 2 and hand == 1):
                    hand = 2
                    continue
                if(hand == 2 and hands == 2):
                    continue
                break
    #There was an inital blackjack
    else:
        result = initialResult
        reason = "BLACKJACK"
    #If the dealers card isn't visible, make it visible
    if(drawn):
        decks.undraw()
        drawn = False
    if(reason == False):
        reason = "Thanks for playing!"
    #Update dealer score
    dealerText.setText("Dealer Score\n{0}".format(dScore + dHiddenScore))
    #end the game
    if(hands == 2):
        balance = splitend(resultTwo, reasonTwo, bet, balance, name, insured)
        reason = "Thanks for playing"
    balance = end(window, result, reason, bet, balance, name, insured)
 #undraw all active cards
    for i in usedCards:
        i.undraw()
    #undaw all other active graphics objects
    undraw(deck, dealerText, playerText, hit, stand, split, dd)
    #update highscores
    updateHighscores(balance, name)

#Check if the user can split
def checkSplit(score, score2, cards):
    if(score == score2):
        return True
    return False

#Simulate the dealer hit
def dealerHit(dScore, dHScore, cards, usedCards, dealerX, dText, window):
    while((dScore + dHScore) < 17):
        card, usedCards, dScore = getCard(cards, usedCards, dScore)
        drawObject(window, card)
        moveTo(card, dealerX, 250)
        dText.setText("Dealer Score\n{0}".format(dScore + dHScore))
        dealerX += 75
    return usedCards, dScore, dealerX

#Update the highscores, checks current users schools
def updateHighscores(amount, user):
    file = open("highscores.dat", 'r')
    scores = []
    users = []
    for i in range(5):
        scores.append(file.readline())
        users.append(file.readline())
    file.close()
    file = open("highscores.dat", "w")
    userCount = 0
    for i in range(len(scores)):
        if(users[i].strip() == user):
            userCount = 1
        if(amount > int(scores[i])):
            scores[i] = str(amount) + "\n"
            users[i] = user + "\n"
            amount = 0
        if(userCount == 1):
            break
    for j in range(len(scores)):
        file.write(str(scores[j]))
        file.write(users[j])
    file.close()

#Get the highscores and display them
def getHighscores(window):
    file = open("highscores.dat", "r")
    scores = ""
    for i in range(5):
        scores += "Balance: " + file.readline() +" User: " + file.readline() + "\n"
    box = Rectangle(Point(200, 200), Point(600, 600))
    box.setFill("white")
    box.draw(window)
    text = Text(Point(400, 400), "Highscores: \n \n"+scores +"\n\nClick anywhere to return")
    text.draw(window)
    window.getMouse()
    undraw(box, text)

#returns win or lose, and the reason
def checkGame(uScore, dScore, canHit):
    if(uScore == 21):
        return "WIN", "You hit 21!"
    elif(uScore >= 21):
        return "LOSE", "You've BUSTED!"
    elif(dScore == 21):
        return "LOSE", "Dealer hit 21 :("
    elif(dScore >= 21):
        return "WIN", "Dealer busted"
    #Scores are the same and player/dealer can't hit
    elif((dScore == uScore) and dScore >= 17 and not canHit):
        return "TIE", "Pushed"
    #User score is higher than the dealers final score and the user can't hit
    elif(uScore > dScore and dScore >= 17 and not canHit):
        return "WIN", "You win"
    elif(dScore > uScore and not canHit):
        return "LOSE", "Dealer has a higher score!"
    else:
        return False, False

#Add a card to a players hand
def userHit(window, cards, used, score, x):
    card, used, score = getCard(cards, used, score)
    drawObject(window, card)
    moveTo(card, x, 550)
    return used, score, x + 75

#End the game, update the balance, return to getBet()
def end(window, result, reason, bet, balance, name, isInsured):
    box = Rectangle(Point(240, 50), Point(560, 150))
    box.setFill("white")
    box.draw(window)
    #The user wins
    if(result == "WIN"):
        balance = balance +(bet * 2)
    elif(result == "TIE"):
        #"Refund" the player
        balance = balance + bet
    elif(reason == "BLACKJACK"):
        if(result == "DEALER"):
            reason = "Dealer BLACKJACK!"
            if(isInsured):
                balance = balance + bet
        else:
            balance = balance + (bet * 2) + int(bet // 2)
    updateProfile(name, balance)
    text = Text(Point(400, 100), "{0}\nClick anywhere to return to the game menu".format(reason))
    text.draw(window)
    window.getMouse()
    undraw(box, text)
    return balance

#Update the balance (of the second hand) if the player has split
def splitend(result, reason, bet, balance, name, isInsured):
    if(result == "WIN"):
        balance = balance +(bet * 2)
    elif(result == "TIE"):
        #"Refund" the player
        balance = balance + bet
    elif(reason == "BLACKJACK"):
        if(result == "DEALER"):
            reason = "Dealer BLACKJACK!"
            if(isInsured):
                balance = balance + bet
        else:
            balance = balance + (bet * 2) + int(bet // 2)
    updateProfile(name, balance)
    return balance
#Check to see if there's a blackjack
def checkBlackjack(score, score1):
    #card, card 3 is user
    if(score == 21):
        return "USER"
    elif(score1 == 21):
        return "DEALER"
    return False

#FROM TKINTER MESSAGEDIALOG
class Message(Dialog):
    "A message box"
    command  = "tk_messageBox"
# convenience stuff
# Rename _icon and _type options to allow overriding them in options
def _show(title=None, message=None, _icon=None, _type=None, **options):
    if _icon and "icon" not in options:    options["icon"] = _icon
    if _type and "type" not in options:    options["type"] = _type
    if title:   options["title"] = title
    if message: options["message"] = message
    res = Message(**options).show()
    # In some Tcl installations, yes/no is converted into a boolean.
    if isinstance(res, bool):
        if res:
            return YES
        return NO
    # In others we get a Tcl_Obj.
    return str(res)

#Error window
def showerror(title=None, message=None, **options):
    return _show(title, message, "error", "ok", **options)
#Question window
def askyesno(title=None, message=None, **options):
    "Ask a question; return true if the answer is yes"
    s = _show(title, message, "question", "yesno", **options)
    return s == "yes"

#Deal the first 4 initial cards needed to play. 2 Each
def initialDeal(window, deck, card1, card2, card3, card4):
    drawObject(window, card1, card2, card3, card4)
    moveTo(card1, 100, 550)
    nDeck = deck.clone()
    nDeck.move(-680, -150)
    #Draw the deck so only one of the dealers cards are visible
    nDeck.draw(window)
    card2.move(-680, -150)
    moveTo(card3, 175, 550)
    moveTo(card4, 175, 250)
    return nDeck

#Get a random card
def getCard(cards, used, score):
    while(True):
        index = randint(0, len(cards) - 1)
        card = cards[index]
        #Check if the card is already being used, if so get another
        isUsed = False
        for i in used:
            if used == card:
                isUsed = True
        if(not isUsed):
            used.append(card)
            break
    #Add one to the index
    index += 1
    #Get the score of the card
    score = getScore(index % 52, score)
    return card, used, score

#Calaculate the score of a card giving it's index (0-52)
def getScore(index, score):
    #Subtract 13 (52(deck size) / 4(amount of each kind). Hearts/Spades all treated as the same.
    while(True):
        if(index <= 13):
            break
        index = index - 13
    if(index == 0):
        score += 10
    elif(index <= 9):
        score += index + 1
    elif(index >= 11):
        score += 10
    else:
        #Ace score checking
        if((score + 11) < 21):
            score += 11
        else:
            score += 1
    return score

#Move an image to a location
def moveTo(image, x, y):
    i = j = -1
    if(y > 400):
        j = 1
    #Coords of where the cards move from (Dealer deck)
    oldX = 780
    oldY = 400
    while True:
        if(x != oldX):
            image.move(i, 0)
            oldX += i
        if(y != oldY):
            image.move(0, j)
            oldY += j
        if(x == oldX and y == oldY):
            break
        sleep(0.0005)

#Move an image only on the x Axis
def move(image, x, newX):
    i = 1
    while True:
        if(newX != x):
            image.move(i, 0)
            x += i
        if(x == newX):
            break
        sleep(0.0005)

#Get the users bet
def getBet(window, balance):
    bet = 0
    buttons = []
    #Window setup
    buttons.append(Chip(window, Point(150, 700), 25, 1, "gray32"))
    buttons.append(Chip(window, Point(250, 700), 25, 5, "magenta2"))
    buttons.append(Chip(window, Point(350, 700), 25, 10, "deep sky blue"))
    buttons.append(Chip(window, Point(450, 700), 25, 20, "red2"))
    buttons.append(Chip(window, Point(550, 700), 25, 50, "green2"))
    buttons.append(Chip(window, Point(650, 700), 25, 100, "yellow2"))
    text = Entry(Point(400, 550), 20)
    text.setFill("dodgerblue2")
    text.draw(window)
    title = Text(Point(400, 525), "ENTER YOUR BET")
    title.setFill("white")
    title.draw(window)
    balanceText = Text(Point(400, 300), "Balance: {0}".format(balance - bet))
    balanceText.setFill("white")
    balanceText.draw(window)
    betChip = Button(window, Point(400, 600), 75 ,50, "BET", "dodgerblue2")
    while(True):
        click = window.getMouse()
        if(betChip.clicked(click)):
            try:
                #Try to convert the bet into an integer
                bet = int(text.getText())
            except:
                bet = 0
            if(bet != 0):
                #Players can't go over their account balance.
                if(bet > balance):
                    bet = 0
                else:
                    for i in buttons:
                        i.undraw()
                    undraw(text, title, betChip, balanceText)
                    return bet
        for i in buttons:
            if(i.clicked(click)):
                amount = eval(str(i.getAmount()))
                if(bet + amount > balance):
                    break
                #Add the amount of a chip when clicked
                bet += eval(str(i.getAmount()))
        text.setText(bet)
        #Update the text to display users balance
        balanceText.setText("Balance: {0}".format(balance - bet))
if __name__ == '__main__':
    main(True, "")