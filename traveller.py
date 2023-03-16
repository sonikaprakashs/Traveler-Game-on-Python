import csv
import sys
import random

f = open('road', 'w+')
f.write('X, , , , , , , , , ,1')
f.close()

f = open('health', 'w+')
f.write('100')
f.close()

f = open('inventory', 'w+')
f.write('1')
f.close()


def getPosition():
    with open('road', 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        road = []
        for line in csv_reader:
            road = line
    return road


def displayPosition(pos):
    nr = pos.copy()
    nrp = nr.index('X')
    moves = int(nr[10])
    nr[nrp] = 'X' * moves
    print('|'.join(nr[0:10]))


def movePlayer(steps):
    currentRoad = getPosition()

    multiplymove = int(currentRoad[10])

    currentPosition = currentRoad.index('X')

    newPosition = currentPosition + steps * multiplymove
    if steps != 0:
        multiplymove = 1
        currentRoad[10] = '1'

    if newPosition <= 0 and steps != 0:
        newPosition = 0
        print("Sorry: You cannot move step backward if you are position One!")

    if newPosition >= len(currentRoad) - 2:
        print('Congratulations! You made it to the end of the road. Well Done. You WIN!')
        sys.exit(0)

    currentRoad[currentPosition] = ' '
    currentRoad[newPosition] = 'X'
    # print(currentRoad)

    wtr = csv.writer(open('road', 'w'), delimiter=',', lineterminator='\n')
    wtr.writerow(currentRoad)

    print('Current Position:', newPosition + 1)
    displayPosition(currentRoad)


def Potion():
    with open('inventory', 'r') as f:
        potion1 = int(f.read())
    if potion1 <= 0:
        print("Potion is now empty and it cannot be reused.")
        updateHealth(0)
    else:
        potion1 -= 1
        updateHealth(70)
    with open('inventory', 'w') as f:
        f.write(str(potion1))
    print('Current Inventory:', potion1)


def updateHealth(healthChange):
    with open('health', 'r') as f:
        health = int(f.read())
    health += healthChange
    if health <= 0:
        print("Game Over! You have no health left.")
        sys.exit(0)
    if health > 100:
        health = 100
    with open('health', 'w') as f:
        f.write(str(health))
    print('Current health:', health)


def rollDice():
     #x = int(input('Dice input:'))
    return random.randint(1, 6)
     #return x


def MoveDouble():
    currentRoad = getPosition()
    moveMultiply = int(currentRoad[10])
    moveMultiply *= 2
    currentRoad[10] = str(moveMultiply)
    wtr = csv.writer(open('road', 'w'), delimiter=',', lineterminator='\n')
    wtr.writerow(currentRoad)
    displayPosition(currentRoad)


def getUserInputAnswer(inputQuestion):
    userInput = ""

    while userInput != 'q':
        userInput = input(f'\n{inputQuestion}\nValid inputs: r, p, q\n')
        if userInput not in ['p', 'q', 'r']:

            print("Invalid Selection: Please choose either\n r: Roll a Dice \n p: Consume a Potion \n q: Quit the Game?")

        while userInput not in ['p', 'r']:

            if userInput == 'q':
                print("Game Over: See you next time")
                sys.exit(0)

            userInput = input(f'\n{inputQuestion}\nValid inputs: r, p, q\n')

            if userInput not in ['p', 'q', 'r']:
                print("Invalid Selection: Please choose either\n r: Roll a Dice \n p: Consume a Potion \n q: Quit the Game?")

        if userInput == 'r':
            print('You chose r: Roll a Dice for your game')
            diceOutcome = rollDice()

            if diceOutcome == 1:
                print('You rolled 1 and took 10 damage.\n')
                updateHealth(-10)
                movePlayer(0)

            elif diceOutcome == 2:
                print('You rolled 2 and moved one step back.\n')
                updateHealth(0)
                movePlayer(-1)

            elif diceOutcome == 3:
                d10Roll = random.randint(1, 10)
                if d10Roll == 7:
                    print('You rolled a dice 3 and were saved and sent to the end of the path!\n')
                    updateHealth(0)
                    movePlayer(10)

                else:
                    print('You rolled a dice 3 and You prayed for salvation but nothing happened.\n')
                    updateHealth(0)
                    movePlayer(0)

            elif diceOutcome == 4:
                print('You rolled 4 and took 40 damage.\n')
                updateHealth(-40)
                movePlayer(0)

            elif diceOutcome == 5:
                print('You rolled 5 and doubled your next movement.\n')
                MoveDouble()
                print(f"Movement Multiplied")
                updateHealth(0)
                movePlayer(0)

            elif diceOutcome == 6:
                print('You rolled 6 and move a step forward\n')
                updateHealth(0)
                movePlayer(+1)

        if userInput == 'p':
            print('You chose p: Consume a potion')
            Potion()


startGame = getUserInputAnswer("What will you do, traveller? r: Roll a Dice  p: Consume a Potion  q: Quit the Game? ")
