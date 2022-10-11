"""
用栈模拟队列出队、入队操作
"""


class StackQueue:
    def __init__(self):
        self.stack1 = []                    # 用列表模拟栈
        self.stack2 = []                    # 用列表模拟栈

    def push(self, num):
        self.stack1.append(num)

    def pop(self):
        if len(self.stack2) == 0:
            if len(self.stack1) != 0:
                self.stack2 = list(reversed(self.stack1))
                self.stack1.clear()         # 易错: stack1已经存入stack2, 需要清空stack1
            else:
                print('队列已经为空')
                return
        res = self.stack2.pop(-1)
        print('{}被弹出成功'.format(res))


if __name__ == '__main__':
    data = StackQueue()
    data.push(1)
    data.push(2)
    data.push(4)
    data.push(3)

    data.pop()
    data.pop()
    data.pop()
    data.pop()
    data.pop()

    data.push(6)
    data.pop()
    data.pop()
