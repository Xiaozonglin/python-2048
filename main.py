import os
from random import randint, random
from collections import deque

class Play:
    def __init__(self) -> None:
        # 初始化，存储每一格的数字
        self.data = []
        self.score = 0
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
        if random() > 0.9:
            random_number = 4
        else:
            random_number = 2
        self.data[vacent[random_index]] = random_number

    def get_score(self) -> int:
        return self.score

    def operate(self, op: str, isTest: bool = False) -> bool:
        # 进行操作，上下左右，返回操作是否有效
        match op:
            case 'w': opn = 1
            case 's': opn = -1
            case 'a': opn = 2
            case 'd': opn = -2
            case _: return False

        nums = self.get_valid_number_dict()
        isUpdated = False

        if opn == 1:
            # 对每一列进行检查，双端队列，没漏洞，又优雅，thanks @copperkoi
            for row in range(0, 4):
                deq = deque()
                for i in range(0, 4):
                    index = i * 4 + row
                    if index not in nums:
                        continue
                    if len(deq) == 0:
                        # 入栈
                        deq.append(nums[index])
                        if i != 0:
                            # 发生平移
                            isUpdated = True
                    elif deq[-1] == nums[index]:
                        deq.pop()
                        self.score += nums[index] * 2
                        deq.append(nums[index] * 2)
                        isUpdated = True
                    else:
                        if i != len(deq):
                            # 发生平移
                            isUpdated = True
                        deq.append(nums[index])

                if isTest == True:
                    # 如果是test就不修改
                    continue
                # 依次出队，覆盖原本列
                for i in range(0, 4):
                    if len(deq) == 0:
                        self.data[i * 4 + row] = 0
                    else:
                        self.data[i * 4 + row] = deq.popleft()
                
        elif opn == -1:
            for row in range(0, 4):
                deq = deque()
                for i in range(3, -1, -1):
                    index = i * 4 + row
                    if index not in nums:
                        continue
                    if len(deq) == 0:
                        # 入栈
                        deq.append(nums[index])
                        if i != 3:
                            # 发生平移
                            isUpdated = True
                    elif deq[-1] == nums[index]:
                        deq.pop()
                        self.score += nums[index] * 2
                        deq.append(nums[index] * 2)
                        isUpdated = True
                    else:
                        if i != 3 - len(deq):
                            # 发生平移
                            isUpdated = True
                        deq.append(nums[index])
            
                if isTest == True:
                    # 如果是test就不修改
                    continue
                # 依次出队，覆盖原本列
                for i in range(3, -1, -1):
                    if len(deq) == 0:
                        self.data[i * 4 + row] = 0
                    else:
                        self.data[i * 4 + row] = deq.popleft()
            
        elif opn == 2:
            # 对每一行进行检查
            for row in range(0, 4): # 行
                deq = deque()
                for i in range(0, 4): # 列
                    index = row * 4 + i
                    if index not in nums:
                        continue
                    if len(deq) == 0:
                        # 入栈
                        deq.append(nums[index])
                        if i != 0:
                            # 发生平移
                            isUpdated = True
                    elif deq[-1] == nums[index]:
                        deq.pop()
                        self.score += nums[index] * 2
                        deq.append(nums[index] * 2)
                        isUpdated = True
                    else:
                        if i != len(deq):
                            # 发生平移
                            isUpdated = True
                        deq.append(nums[index])
            
                if isTest == True:
                    # 如果是test就不修改
                    continue
                # 依次出队，覆盖原本列
                for i in range(0, 4):
                    if len(deq) == 0:
                        self.data[row * 4 + i] = 0
                    else:
                        self.data[row * 4 + i] = deq.popleft()
            
        else:
            # 对每一行进行检查
            for row in range(0, 4): # 行
                deq = deque()
                for i in range(3, -1, -1): # 列
                    index = row * 4 + i
                    if index not in nums:
                        continue
                    if len(deq) == 0:
                        # 入栈
                        deq.append(nums[index])
                        if i != 3:
                            # 发生平移
                            isUpdated = True
                    elif deq[-1] == nums[index]:
                        deq.pop()
                        self.score += nums[index] * 2
                        deq.append(nums[index] * 2)
                        isUpdated = True
                    else:
                        if i != 3 - len(deq):
                            # 发生平移
                            isUpdated = True
                        deq.append(nums[index])
            
                if isTest == True:
                    # 如果是test就不修改
                    continue
                # 依次出队，覆盖原本列
                for i in range(3, -1, -1):
                    if len(deq) == 0:
                        self.data[row * 4 + i] = 0
                    else:
                        self.data[row * 4 + i] = deq.popleft()
            
        return isUpdated

    def is_game_continuable(self) -> bool:
        if len(self.get_vacent_index()) > 0 or self.operate('w', True) or self.operate('s', True) or self.operate('a', True) or self.operate('d', True):
            return True
        return False

game = Play()

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
        game.random_new_number()
    if not game.is_game_continuable():
        game.printTheData()
        print(f"游戏结束，本局获得 {game.get_score()} 分")
        return False
    game.printTheData()
    print(f"当前 {game.get_score()} 分")

os.system("cls" if os.name == "nt" else "clear")
game.random_new_number()
game.random_new_number()
game.printTheData()
print(f"当前 {game.get_score()} 分")
with Listener(on_press=on_press) as listener:
    listener.join()