import math
import random
import datetime
import csv

# 定数定義
RANGE = [0, 9]
MAX_GUESS = 10
SCREEN_WIDTH = 100
LINE = 20
DATA_LENGH = [23, 20, 13, 13, 13, 15]
NAME_LENGH = 20

DEFAULT_SETTING = [0, 9, 10, 20]

MAX_DIGIT = RANGE[1] - RANGE[0] + 1
LINE_DIGIT = math.ceil(math.log10(MAX_GUESS+1))

class Trial:
    def __init__(self, n, digit):
        self.line = n+1
        self.hit = 0
        self.blow = 0
        self.digit = digit
        self.isInput = False
        self.isMatched = False
        self.guessList = [0] * digit

    def addHitAndBlow (self, hit, blow):
        self.hit += hit
        self.blow += blow
    
    def InputAndCheck (self, answer):
        self.guessList = getPlayerInput(self.digit)
        self.isInput = True
        for i in range(self.digit):
            if self.guessList[i] in answer:
                self.blow += 1
            if self.guessList[i] == answer[i]:
                self.blow -= 1
                self.hit += 1
        self.isMatched = True if self.hit == self.digit else False

   
    def show (self):
        if self.isInput:
            spaceN = math.ceil(math.log10(self.line+1))
            for i in range(LINE_DIGIT - spaceN):
                print(" ", end='')
            print(f"{self.line}", end='')
            print(f"\t", end='')
            for i in range(self.digit):
                print(self.guessList[i], end=' ')
            print(f"\t\t {self.hit}\t {self.blow}")
    


def showFrame (digit):
    newLine(LINE)
    print(f"\t", end='')
    for i in range(digit):
        print(" ",end=' ')
    print(f"\t\tHit\tBlow")
    print("-" * SCREEN_WIDTH)

def getPlayerInput(digit):
    while True:
        print()
        playerInput = input("enter the numbers: ")

        try:
            if len(playerInput) != digit:
                printError()
                continue

            playerInputList = []
            isExistSame = False
            for number in playerInput:
                if not int(number) in playerInputList:
                    playerInputList.append(int(number))
                else:
                    print("同じ数字は2回以上使えません。もう一度入力してください。")
                    isExistSame = True
                    break
            if not isExistSame:
                return  playerInputList

        except:
            printError()
            continue

def getYesNoInput(text, error):
    x = None
    while True:
        x = input(f"{text}")
        if x == 'y':
            x = True
            break
        elif x == 'n':
            x = False
            break
        else:
            printError()
            print(f"{error}")
    return x



def printError ():
    print("*" * SCREEN_WIDTH)
    print("入力エラー: 正しい形式で入力してください。")
    print("*" * SCREEN_WIDTH)

def printCostomError(text):
    print('*' * SCREEN_WIDTH)
    print(f"入力エラー: {text}")
    print('*' * SCREEN_WIDTH)

def newLine(n):
    for i in range(n):
        print()



def hitAndBlow(digit, Result):

    answer = [None] * digit
    for i in range(digit):
        while True:
            randNum = random.randint(RANGE[0], RANGE[1])
            if randNum in answer:
                continue
            answer[i] = randNum
            break
    print(answer)



    rounds = []
    for i in range(MAX_GUESS):
        rounds.append(Trial(i, digit))

    count = 0

    newLine(LINE)
    while True:
        count += 1
        print()
        print("=" * SCREEN_WIDTH)
        print(f"桁数: {digit}")
        print()
        print(f"{count}回目: ")
        rounds[count-1].InputAndCheck(answer)
        
        showFrame(digit)
        for i in range(MAX_GUESS):
            rounds[i].show()
        print()

        if rounds[count-1].isMatched:
            print("matched!")
            Result["correct"] += 1
            break


        if count >= MAX_GUESS:
            print("Game Over")
            break
    
    return count

def record(Result):
    dt_now = datetime.datetime.now()
    name = None
    
    print()
    while True:
        name = input("記録する名前を入力してください。: ")
        if len(name) > NAME_LENGH:
            print(f"名前の文字数は {NAME_LENGH} 文字までです。")
            print()
            print("もう一度", end='')
            continue
        isOk = getYesNoInput(f"{name} でよろしいですか？ (y/n): ", '')
        if isOk:
            break
        else:
            print()
            print("もう一度", end='')

    with open('HitAndBlow.csv', mode='a') as f:
        f.write(f"{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}, {name}, {Result["play"]}, {Result["correct"]}, {Result["guess"]}, {Result["average"]}\n")
    
    print()
    print("結果を記録しました。")


def game():

    while True:
        print()
        digit = input(f"桁数を入力してください(1〜{MAX_DIGIT}): ")
        try:
            if digit.isdigit() and 1 <= int(digit) <= MAX_DIGIT:
                digit = int(digit)
                break
            else:
                print("*" * SCREEN_WIDTH)
                print(f"入力エラー: 入力は半角数字で1〜{MAX_DIGIT}の範囲で入力してください。")
                print("*" * SCREEN_WIDTH)
                continue
        except:
            print("*" * SCREEN_WIDTH)
            print(f"入力エラー: 入力は半角数字で1〜{MAX_DIGIT}の範囲で入力してください。")
            print("*" * SCREEN_WIDTH)
            continue


    ResultKeys = ["play", "correct", "guess", "average"]
    ResultValues = [0, 0, 0, 0]

    Result = dict(zip(ResultKeys, ResultValues))

    while True:
        Result["play"] += 1
        Result["guess"] += hitAndBlow(digit, Result)
        Result["average"] = Result["guess"] / Result["play"]

        print()
        print("=" * SCREEN_WIDTH)
        print("=" * SCREEN_WIDTH)
        print()
        
        again = getYesNoInput("もう一度プレイしますか？ (y/n): ", '')
        if not again:
            break
    
    return Result

def mainScreen():
    print()
    print()
    print("#" * SCREEN_WIDTH)
    side = (SCREEN_WIDTH - 12) / 2
    print(' ' * int(side), end='') 
    print("Hit And Blow")
    print("#" * SCREEN_WIDTH)
    print()
    print()
    print('-' * SCREEN_WIDTH)

def showHistory():
    newLine(LINE)
    print("日時", end='')
    print(' ' * (DATA_LENGH[0]), end='')
    print("名前", end='')
    print(' ' * (DATA_LENGH[1]-4), end='')
    print("プレイ回数", end='')
    print(' ' * (DATA_LENGH[2]-10), end='')
    print("当てた回数", end='')
    print(' ' * (DATA_LENGH[3]-10), end='')
    print("総予想回数", end='')
    print(' ' * (DATA_LENGH[4]-10), end='')
    print("平均予想回数", end='')
    print()
    print('-' * SCREEN_WIDTH)
    with open('HitAndBlow.csv') as f:
        reader = csv.reader(f)
        for data in reader:
            for i in range(len(data)):
                print(f"{data[i]}", end='')
                space = DATA_LENGH[i] - len(data[i])
                print(' ' * space, end='')
            print()
    print()
    input("Enterを押して戻る...")

def settings():
    newLine(LINE)

    while True:
        print('=' * SCREEN_WIDTH)
        print()
        print("設定項目")
        print(f"\t1: 数字の下限 (デフォルト: 0, 現在値: {RANGE[0]})")
        print(f"\t2: 数字の上限 (デフォルト: 9, 現在値: {RANGE[1]})")
        print(f"\t3: 予想可能数 (デフォルト: 10, 現在値: {MAX_GUESS})")
        print(f"\t4: 名前文字数 (デフォルト: 20, 現在値: {NAME_LENGH})")
        print(f"\t5: 戻る")
        print(f"\t6: デフォルトに戻す")
        print()
        print('=' * SCREEN_WIDTH)
        print("設定する項目の数字を入力してください。(1,2,3,4,5,6)")

        try:
            s = int(input())
            match s:
                case 1:
                    setting1()
                case 2:
                    setting2()
                case 3:
                    setting3()
                case 4:
                    setting4()
                case 5:
                    break
                case 6:
                    setDefault()
                case _:
                    newLine(LINE)
                    printError()
                    continue
            newLine(LINE)
        except:
            newLine(LINE)
            printError()

def settingScreen(target, requirements):
    print('=' * SCREEN_WIDTH)
    print()
    print()
    print()
    print(f"{target}")
    print()
    print(f"\t{requirements}")
    print()
    print()
    print()
    print('=' * SCREEN_WIDTH)
    print()

def setting1():
    global MAX_DIGIT
    newLine(LINE)

    while True:
        settingScreen("数字の下限", f"数字の下限を 0 から {RANGE[1]-1} の中から選んで入力してください。")
        try:
            n = int(input())
            if 0 <= n <= RANGE[1] - 1:
                RANGE[0] = n
                MAX_DIGIT = RANGE[1] - RANGE[0] + 1
                break
            else: 
                newLine(LINE)
                printCostomError(f"0 から {RANGE[1]-1} の数字を入力してください。")
        except:
            newLine(LINE)
            printError()

def setting2():
    global MAX_DIGIT
    newLine(LINE)

    while True:
        settingScreen("数字の上限", f"数字の上限を {RANGE[0]+1} から 9 の中から選んで入力してください。")
        try:
            n = int(input())
            if RANGE[0] + 1 <= n <= 9:
                RANGE[1] = n
                MAX_DIGIT = RANGE[1] - RANGE[0] + 1
                break
            else: 
                newLine(LINE)
                printCostomError(f"{RANGE[0]+1} から 9 の数字を入力してください。")
        except:
            newLine(LINE)
            printError()

def setting3():
    global MAX_GUESS, LINE_DIGIT
    newLine(LINE)

    while True:
        settingScreen("予想可能数", "数列を予想できる回数を入力してください。")
        try:
            n = int(input())
            if 1 <= n:
                MAX_GUESS = n
                LINE_DIGIT = math.ceil(math.log10(MAX_GUESS+1))
                break
            else:
                newLine(LINE)
                printCostomError("1以上の整数を入力してください。")
        except:
            newLine(LINE)
            printError()

def setting4():
    global NAME_LENGH
    newLine(LINE)
    while True:
        settingScreen("名前文字数", "記録する時に入力する名前の最大文字数を入力してください。(最大20文字)")
        try:
            n = int(input())
            if 1 <= n <= 20:
                NAME_LENGH = n
                break
            elif n > 20:
                newLine(LINE)
                printCostomError("最大20文字までです。")
            else:
                newLine(LINE)
                printCostomError("1以上の整数を入力してください。")
        except:
            newLine(LINE)
            printError()

def setDefault():
    isOk = getYesNoInput("全ての設定をリセットしますか？ (y/n)", '')
    if isOk:
        global MAX_GUESS, NAME_LENGH, MAX_DIGIT, LINE_DIGIT
        RANGE[0] = DEFAULT_SETTING[0]
        RANGE[1] = DEFAULT_SETTING[1]
        MAX_GUESS = DEFAULT_SETTING[2]
        NAME_LENGH = DEFAULT_SETTING[3]
        MAX_DIGIT = RANGE[1] - RANGE[0] + 1
        LINE_DIGIT = math.ceil(math.log10(MAX_GUESS+1))


        

def main():
    try:
        with open('HiaAndBlow.csv') as f:
            pass
    except:
        with open('HitAndBlow.csv', mode='w') as f:
            pass
    while True:
        mainScreen()
        print("Enterキーを押してください...")
        # showHistory()
        input()
        newLine(LINE)

        wantEnd = False
        
        while True:
            mainScreen()
            print("ゲームスタート: g, 戦歴を見る: h, 設定: s, ゲームを終了する: E")
            mode = input()
            if mode == 'g':
                break
            elif mode == 'h':
                showHistory()
                newLine(LINE)
            elif mode == 's':
                settings()
                newLine(LINE)
            elif mode == 'E':
                wantEnd = True
                break
            else:
                newLine(LINE)
                printError()
        
        if wantEnd:
            newLine(LINE)
            mainScreen()
            print("おしまい")
            break

        Result = game()
        print()
        print(Result)
        isRecord = getYesNoInput("結果を記録しますか？ (y/n)", '')
        if isRecord:
            record(Result)


        newLine(LINE)






main()