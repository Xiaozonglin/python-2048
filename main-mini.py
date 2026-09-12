import os
from random import randint, random
from collections import deque

class Play:
    # 存储每一格的数字
    data = []

    def __init__(self) -> None:
        # 初始化
        for _ in range(16):
            self.data.append(0)

    def printTheData(self) -> None:
        # 将当前情况打印到控制台
        for i in range(4):
            print("\t\t".join(map(str, self.data[4 * i:4 * i + 4])))

    def get_vacent_index(self) -> list[int]:
        # 获取当前没有数字的索引
        result = []
        for index, i in enumerate(self.data):
            if i == 0:
                result.append(index)
        return result

    def get_valid_number_dict(self) -> dict[int, int]:
        # 获取当前所有数字的位置与值
        result = dict()
        for index, i in enumerate(self.data):
            if i != 0:
                result[index] = i
        return result

    def random_new_number(self) -> None:
        # 随机选择一个添加数字
        vacent = self.get_vacent_index()
        if len(vacent) == 0:
            return
        random_index = randint(0, len(vacent) - 1)
        if random() > 0.6:
            random_number = 4
        else:
            random_number = 2
        self.data[vacent[random_index]] = random_number

    def get_score(self) -> int:
        result = 0
        for i in self.data:
            result += i
        return result

    def operate(self, op: str, isTest: bool = False) -> bool:
        # 进行操作，上下左右，返回操作是否有效
        match op:
            case 'w': opn = 1
            case 's': opn = -1
            case 'a': opn = 2
            case 'd': opn = -2
            case _: return False

        nums = self.get_valid_number_dict()

        def check_and_update(isReverse: bool = False, isVertical: bool = False) -> bool:
            if isReverse:
                column_from = 3
                column_to = -1
                column_step = -1
            else:
                column_from = 0
                column_to = 4
                column_step = 1

            isUpdated = False
            for row in range(0, 4):
                deq = deque()
                for i in range(column_from, column_to, column_step):
                    if isVertical:
                        index = row * 4 + i
                    else:
                        index = i * 4 + row
                    if index not in nums:
                        continue
                    if len(deq) == 0:
                        # 入栈
                        deq.append(nums[index])
                        if i != column_from:
                            # 发生平移
                            isUpdated = True
                    elif deq[-1] == nums[index]:
                        deq.pop()
                        deq.append(nums[index] * 2)
                        isUpdated = True
                    else:
                        if i != 3 - len(deq) if isReverse else len(deq):
                            # 发生平移
                            isUpdated = True
                        deq.append(nums[index])

                if isTest == True:
                    # 如果是test就不修改
                    continue
                # 依次出队，覆盖原本列
                for i in range(column_from, column_to, column_step):
                    if isVertical:
                        index = row * 4 + i
                    else:
                        index = i * 4 + row
                    if len(deq) == 0:
                        self.data[index] = 0
                    else:
                        self.data[index] = deq.popleft()
            return isUpdated

        if opn == 1:
            # 对每一列进行检查，双端队列，没漏洞，又优雅，thanks @copperkoi
            return check_and_update()
        elif opn == -1:
            return check_and_update(isReverse=True)
        elif opn == 2:
            # 对每一行进行检查
            return check_and_update(isVertical=True)
        else:
            # 对每一行进行检查
            return check_and_update(isReverse=True, isVertical=True)

    def is_game_continuable(self) -> bool:
        if self.get_vacent_index() is not None or self.operate('w', True) or self.operate('s', True) or self.operate('a', True) or self.operate('d', True):
            return True
        return False

game = Play()

import signal
import sys

def signal_handler(signal, frame):
    print("\n退出游戏")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# 上下左右键
from pynput.keyboard import Key, Listener
import os

def on_press(key):
    match key:
        case Key.up: op = 'w'
        case Key.down: op = 's'
        case Key.left: op = 'a'
        case Key.right: op = 'd'
        case Key.esc: return False
        case _: return

    os.system("cls" if os.name == "nt" else "clear")
    if game.operate(op):
        if game.is_game_continuable():
            game.random_new_number()
    game.printTheData()
    print(f"当前 {game.get_score()} 分")

os.system("cls" if os.name == "nt" else "clear")
game.random_new_number()
game.printTheData()
print(f"当前 {game.get_score()} 分")
with Listener(on_press=on_press) as listener:
    listener.join()