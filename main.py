import math
import random
import time
import datetime
import csv

# 定数定義
RANGE = [0, 9]
MAX_GUESS = 10
SCREEN_WIDTH = 135
LINE = 20
DATA_LENGH = [23, 20, 13, 13, 13, 15, 19, 19]
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
        # self.guessList = getPlayerInput(self.digit)
        self.isInput = True
        for i in range(self.digit):
            if self.guessList[i] == answer[i]:
                self.hit += 1
            elif self.guessList[i] in answer:
                self.blow += 1
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
    print("桁数")
    print(f" {digit}\t", end='')
    for i in range(digit):
        print(" ",end=' ')
    print(f"\t\tHit\tBlow")
    print("-" * SCREEN_WIDTH)

# y/n の入力をTrue/Falseに変換する関数
def getYesNoInput(text, error):
    x = None
    while True:
        try:
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
        except:
            printError()
            newLine(2)
            continue
    return x

# エラー表示
def printError(text = "正しい形式で入力してください。"):
    newLine(LINE)
    print('*' * SCREEN_WIDTH)
    print(f"入力エラー: {text}")
    print('*' * SCREEN_WIDTH)

# 引数の分だけ改行する
def newLine(n):
    for i in range(n):
        print()

# ヒットアンドブローの処理
def hitAndBlow(digit, Result):
    clear = False

    # 答えの数列を生成
    answer = [None] * digit
    for i in range(digit):
        while True:
            randNum = random.randint(RANGE[0], RANGE[1])
            if randNum in answer:
                continue
            answer[i] = randNum
            break

    # インスタンス作成
    rounds = []
    for i in range(MAX_GUESS):
        rounds.append(Trial(i, digit))

    count = 0

    newLine(LINE)
    while True:
        count += 1

        while True:

            # Hit, Blow数を表示
            if not count == 1:
                print()
                showFrame(digit)
                for i in range(MAX_GUESS):
                    rounds[i].show()

            print()
            try:
                print()
                print("=" * SCREEN_WIDTH)
                print(f"{count}回目: ")

                availableNumbers = []
                for i in range(RANGE[0], RANGE[1]+1):
                    availableNumbers.append(i)

                print()
                playerInput = input("enter the numbers: ")

                isInclude = True

                for i in range(len(playerInput)):
                    if not int(playerInput[i]) in availableNumbers:
                        isInclude = False
                        break
                    
                if not isInclude:
                    printError(f"{RANGE[0]}から{RANGE[1]}までの数字のみ使用可能です。")
                    continue

                if len(playerInput) != digit:
                    printError(f"{digit}桁の数字を入力してください。")
                    continue

                playerInputList = []
                isExistSame = False
                for number in playerInput:
                    if not int(number) in playerInputList:
                        playerInputList.append(int(number))
                    else:
                        isExistSame = True
                        break
                if isExistSame:
                    printError("同じ数字は2回以上使えません。もう一度入力してください。")
                    continue
                
                break

            except:
                printError()
                continue

        rounds[count-1].guessList = playerInputList

        rounds[count-1].InputAndCheck(answer)
        
        if rounds[count-1].isMatched:
            clear = True
            print()
            print("matched!")
            Result["correct"] += 1
            break

        if count >= MAX_GUESS:
            clear = False
            print()
            print("Game Over")
            break

        newLine(LINE)
    
    return count, clear

# ゲーム結果をcsvに保存
def record(Result):
    dt_now = datetime.datetime.now()
    name = None
    
    print()
    while True:
        try:
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
        except:
            printError()
            newLine(2)
            continue

    with open('HitAndBlow.csv', mode='a') as f:
        f.write(f"{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}, {name}, {Result["play"]}, {Result["correct"]}, {Result["guess"]}, {Result["average"]}, {Result["time"]}, {Result["averageTime"]}\n")
    
    print()
    print("結果を記録しました。")


def game():

    newLine(LINE)
    while True:
        try:
            digit = input(f"桁数を入力してください(1〜{MAX_DIGIT}): ")
            if 1 <= int(digit) <= MAX_DIGIT:
                digit = int(digit)
                break
            else:
                printError(f"1〜{MAX_DIGIT}の範囲で入力してください。")
                continue
        except:
            printError()
            print()
            continue

    ResultKeys = ["play", "correct", "guess", "average", "time", "averageTime"]
    ResultValues = [0, 0, '-', '-', '-', '-']

    Result = dict(zip(ResultKeys, ResultValues))

    while True:

        print()

        Result["play"] += 1

        startTime = time.time()
        guess, clear = hitAndBlow(digit, Result)
        endTime = time.time()

        if clear:
            if Result["guess"] == '-':
                Result["guess"] = 0
            if Result["time"] == '-':
                Result["time"] = 0
            Result["guess"] += guess
            playTime = int((endTime - startTime) * 10) / 10
            Result["time"] += playTime
            Result["average"] = int((Result["guess"] / Result["correct"]) * 10) / 10
            Result["averageTime"] = int((Result["time"] / Result["correct"]) * 10) / 10
            print(f"タイム: {playTime}")
        else:
            print()

        print()
        print("=" * SCREEN_WIDTH)
        print("=" * SCREEN_WIDTH)
        print()
        
        again = getYesNoInput("もう一度プレイしますか？ (y/n): ", '')
        if not again:
            break
    
    return Result

def mainScreen():
    newLine(2)
    print("#" * SCREEN_WIDTH)
    side = (SCREEN_WIDTH - 12) / 2
    print(' ' * int(side), end='') 
    print("Hit And Blow")
    print("#" * SCREEN_WIDTH)
    newLine(2)
    print('-' * SCREEN_WIDTH)

def showHistory():
    newLine(LINE)
    while True:
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
        print(' ' * (DATA_LENGH[5]-12), end='')
        print("合計クリアタイム", end='')
        print(' ' * (DATA_LENGH[6]-16), end='')
        print("平均タイム", end='')
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
        try:
            input("Enterを押して戻る...")
            break
        except:
            printError()
            newLine(2)
            continue

# 設定メニュー
def settings():
    newLine(LINE)

    while True:
        print('=' * SCREEN_WIDTH)
        print()
        print("設定項目")
        print(f"\t1: 数字の下限 (デフォルト: 0,  現在値: {RANGE[0]})")
        print(f"\t2: 数字の上限 (デフォルト: 9,  現在値: {RANGE[1]})")
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
                    printError()
                    continue
            newLine(LINE)
        except:
            printError()

# 設定画面
def settingScreen(target, requirements):
    print('=' * SCREEN_WIDTH)
    newLine(3)
    print(f"{target}")
    print()
    print(f"\t{requirements}")
    newLine(3)
    print('=' * SCREEN_WIDTH)
    print()

# 設定画面1
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
                printError(f"0 から {RANGE[1]-1} の数字を入力してください。")
        except:
            printError()

# 設定画面2
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
                printError(f"{RANGE[0]+1} から 9 の数字を入力してください。")
        except:
            printError()

# 設定画面3
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
                printError("1以上の整数を入力してください。")
        except:
            printError()

# 設定画面4
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
                printError("最大20文字までです。")
            else:
                printError("1以上の整数を入力してください。")
        except:
            printError()

# デフォルト
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

# ルール表示
def rule():
    newLine(LINE)
    while True:
        print('*' * SCREEN_WIDTH)
        print()
        print("Hit and Blow")
        print()
        print(f"\tコンピュータが用意した数列をプレイヤーが推理していくゲーム")
        print()
        print(f"\t数字と場所が合っていたら、\tHit  +1")
        print(f"\t数字のみが合っていたら、\tBlow +1")
        print()
        print('*' * SCREEN_WIDTH)
        print()
        print("Enterを押して戻る...")
        try:
            input()
        except:
            newLine(LINE)
            printError()
            continue
        break

# メイン関数
def main():
    try:
        with open('HitAndBlow.csv') as f:
            pass
    except:
        with open('HitAndBlow.csv', mode='w') as f:
            pass
    while True:
        mainScreen()
        print("Enterキーを押してください...")
        try:
            input()
        except:
            printError()
            continue
        newLine(LINE)

        wantEnd = False
        
        while True:
            mainScreen()
            print("ゲームスタート: g, 戦歴を見る: h, 設定: s, ゲームルールを確認: r, ゲームを終了する: E")
            try:
                mode = input()
            except:
                printError()
                continue
            match mode:
                case 'g':
                    break
                case 'h':
                    showHistory()
                    newLine(LINE)
                case 's':
                    settings()
                    newLine(LINE)
                case 'r':
                    rule()
                    newLine(LINE)
                case 'E':
                    wantEnd = True
                    break
                case _:
                    printError()
        
        if wantEnd:
            newLine(LINE)
            mainScreen()
            print("おしまい")
            break

        Result = game()
        print()
        isRecord = getYesNoInput("結果を記録しますか？ (y/n)", '')
        if isRecord:
            record(Result)

        newLine(LINE)



main()