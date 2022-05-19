import random
from bs4 import BeautifulSoup
import requests
import datetime
import random

a = int(input("請選擇要進行的功能 1.最新疫情資訊 2.事項提醒助手 3.圈圈叉叉小遊戲"))

if a == 1:
    response = requests.get("https://covid-19.nchc.org.tw/")
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find("h1", class_="country_confirmed mb-1 text-success")
    titles2 = soup.find("h1", class_="country_recovered mb-1 text-info")
    titles3 = soup.find("h1", class_="country_deaths mb-1 text-dark")
    titles4 = soup.find("h1", class_="country_deaths mb-1 text-danger")

    print("台灣累積確診", titles.text)
    print("台灣新增確診", titles2.text)
    print("累計死亡", titles3.text)
    print("台灣疫苗涵蓋率", titles4.text)

if a == 2:
    thing_list = []
    distance_month = []
    distance_day = []
    time2 = []

    while True:
        thing = input("請輸入事件")
        time1 = input('請輸入事件日期，格式 xx/xx，可按enter繼續輸入，輸入完畢請先按空格再按enter')

        time2 = time1.split('/')
        thing_month = time2[0]
        thing_day = time2[1]

        now = datetime.datetime.now()  # 現在時間函式
        distance_month = int(thing_month)-now.month
        distance_day = int(thing_day)-now.day

        print("距離", thing, "還有", distance_month, '個月', distance_day, "天")
        b = int(input("1.繼續輸入 2.結束"))
        if b == 2:
            break

if a == 3:

    def drawBoard(board):  # 打印方法
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')

    def inputPlayerLetter():  # 選擇O 或 X
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('你要選 X 還是 O?')
            letter = input().upper()  # 將輸入的轉為大寫
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

    def whoGoesFirst():  # 決定誰先 隨機亂數
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

    def playAgain():  # 再玩一次
        print('再玩一次嗎? (yes or no)')
        return input().lower().startswith('y')

    def makeMove(board, letter, move):  # 將符號放進指定的格子中
        board[move] = letter

    def isWinner(bo, le):  # 用來判斷是否獲勝
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or
                (bo[4] == le and bo[5] == le and bo[6] == le) or
                (bo[1] == le and bo[2] == le and bo[3] == le) or
                (bo[7] == le and bo[4] == le and bo[1] == le) or
                (bo[8] == le and bo[5] == le and bo[2] == le) or
                (bo[9] == le and bo[6] == le and bo[3] == le) or
                (bo[7] == le and bo[5] == le and bo[3] == le) or
                (bo[9] == le and bo[5] == le and bo[1] == le))

    def getBoardCopy(board):  # 複製一份目前局勢，給電腦模擬下一步狀況
        dupeBoard = []
        for i in board:
            dupeBoard.append(i)
        return dupeBoard

    def isSpaceFree(board, move):  # 判斷格子是否是空的
        return board[move] == ' '

    def getPlayerMove(board):  # 讓玩家輸入要填的格子
        move = ' '
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
            print('輸入你的下一步? 最下排由左到右分別是 1 2 3 以此類推')
            move = input()
        return int(move)

    def chooseRandomMoveFromList(board, movesList):
        possibleMoves = []
        for i in movesList:
            if isSpaceFree(board, i):
                possibleMoves.append(i)
        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None

    def getComputerMove(board, computerLetter):  # 讓機器判斷策略
        if computerLetter == 'X':  # 以機器角度來看 如果機器是X 代表玩家就是O
            playerLetter = 'O'
        else:
            playerLetter = 'X'

        # 以下是遊戲進行之中的狀況
        for i in range(1, 10):  # 先檢測自己下一步是否能贏
            # copy一份目前的下子画板
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):  # 若是备份的画板中内容不为空
                makeMove(copy, computerLetter, i)  # 下子
                if isWinner(copy, computerLetter):  # 如果下這個位置會贏 就回傳這個位置
                    return i

        for i in range(1, 10):  # 檢測對手下一步是否會贏，會的話把它堵住
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, playerLetter, i)
                if isWinner(copy, playerLetter):  # 如果對手下一步下這個位置會贏，就回傳這個位置
                    return i

        # 以下是一開始的狀況，由機器先攻的時候
        move = chooseRandomMoveFromList(
            board, [1, 3, 7, 9])  # 優先下角落的位置，隨意決定要下哪一個
        if move != None:
            return move

        if isSpaceFree(board, 5):  # 如果中心點是空的，先搶中心點
            return 5

        # 如果真的不行 就在剩下的格子下子
        return chooseRandomMoveFromList(board, [2, 4, 6, 8])

    def isBoardFull(board):  # 如果格子都滿了 回傳true
        for i in range(1, 10):
            if isSpaceFree(board, i):
                return False
        return True

    while True:
        theBoard = [' '] * 10  # 重置输出板
        playerLetter, computerLetter = inputPlayerLetter()  # 選雙方的旗子
        turn = whoGoesFirst()  # 決定誰先下
        print(turn + '先下')

        gameIsPlaying = True  # 遊戲開始
        while gameIsPlaying:
            if turn == 'player':  # 玩家的回合
                drawBoard(theBoard)  # 獲取下子位置
                move = getPlayerMove(theBoard)  # 下子
                makeMove(theBoard, playerLetter, move)

                if isWinner(theBoard, playerLetter):  # 判斷遊戲是否結束
                    drawBoard(theBoard)
                    print('你贏了')
                    gameIsPlaying = False  # 結束遊戲
                else:
                    if isBoardFull(theBoard):  # 檢驗格子是否已滿
                        drawBoard(theBoard)
                        print('平手')
                        break
                    else:
                        turn = 'computer'  # 如果還沒滿，換電腦下

            else:  # 電腦的回合
                move = getComputerMove(theBoard, computerLetter)
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print('你輸了')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('平手')
                        break
                    else:
                        turn = 'player'

        if not playAgain():
            break
