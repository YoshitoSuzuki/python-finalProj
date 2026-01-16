import math
import random

# 定数定義
# DIGIT = 3
RANGE = [0, 9]
MAX_GUESS = 10
SCREEN_WIDTH = 50

LINE_DIGIT = math.ceil(math.log10(MAX_GUESS+1))

# print(f"test: {LINE_DIGIT}")


digit = 0

while True:
    print()
    digit = input("桁数を入力してください(1〜10): ")
    try:
        if digit.isdigit and 1 <= int(digit) <= RANGE[1]-RANGE[0]+1:
            digit = int(digit)
            break
        else:
            print("*" * SCREEN_WIDTH)
            print("入力エラー: 入力は半角数字で1〜10の範囲で入力してください。")
            print("*" * SCREEN_WIDTH)
            continue
    except:
        print("*" * SCREEN_WIDTH)
        print("入力エラー: 入力は半角数字で1〜10の範囲で入力してください。")
        print("*" * SCREEN_WIDTH)
        continue

answer = [None] * digit
for i in range(digit):
    while True:
        randNum = random.randint(RANGE[0], RANGE[1])
        if randNum in answer:
            continue
        answer[i] = randNum
        break
print(answer)



class Trial:
    def __init__(self, n):
        self.line = n+1
        self.hit = 0
        self.blow = 0
        self.isInput = False
        self.isMatched = False
        self.guessList = [0] * digit

    def addHitAndBlow (self, hit, blow):
        self.hit += hit
        self.blow += blow
    
    def InputAndCheck (self):
        self.guessList = getPlayerInput()
        self.isInput = True
        for i in range(digit):
            if self.guessList[i] in answer:
                self.blow += 1
            if self.guessList[i] == answer[i]:
                self.blow -= 1
                self.hit += 1
        self.isMatched = True if self.hit == digit else False

   
    def show (self):
        if self.isInput:
            spaceN = math.ceil(math.log10(self.line+1))
            for i in range(LINE_DIGIT - spaceN):
                print(" ", end='')
            print(f"{self.line}", end='')
            print(f"\t", end='')
            for i in range(digit):
                print(self.guessList[i], end=' ')
            print(f"\t\t {self.hit}\t {self.blow}")
    


def showFrame ():
    print()
    print(f"\t", end='')
    for i in range(digit):
        print(" ",end=' ')
    print(f"\t\tHit\tBlow")
    print("-" * SCREEN_WIDTH)

def getPlayerInput():
    while True:
        print()
        playerInput = input("enter the numbers: ")

        if not playerInput.isdigit:
            printError()
            continue
            
        if len(playerInput) != digit:
            printError()
            continue

        return [int(number) for number in playerInput]

def printError ():
    print("*" * SCREEN_WIDTH)
    print("入力エラー: 正しい形式で入力してください。")
    print("*" * SCREEN_WIDTH)



def main():

    rounds = []
    for i in range(MAX_GUESS):
        rounds.append(Trial(i))


    # rounds[1].addHitAndBlow(2,1)

    count = 0

    while True:
        print()
        print("=" * SCREEN_WIDTH)
        print(f"桁数: {digit}")
        print()
        print(f"{count+1}回目: ")
        rounds[count].InputAndCheck()
        
        showFrame()
        for i in range(MAX_GUESS):
            rounds[i].show()
        print()

        if rounds[count].isMatched:
            print("matched!")
            break

        count += 1

        if count >= MAX_GUESS:
            print("game over")
            break


main()