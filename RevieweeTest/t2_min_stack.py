"""
该实现代码借用了python的高级数据结构：列表，使得实现尤为简单。
"""


class MinStack:
    def __init__(self):
        self.main_stack = []
        self.min_stack = []

    def push(self, num):
        """
        入栈：将数据元素填入主栈中，同时小数据保存到小栈当中
        """
        self.main_stack.append(num)
        # 空栈
        if len(self.min_stack) == 0:
            self.min_stack.append(num)
            return
        # 非空栈，当前元素与最小栈中最后一个元素比较
        if num <= self.min_stack[-1]:  # 防止栈中有相同数据时，出栈时导致最小数据错误
            self.min_stack.append(num)

    def pop(self):
        """
        出栈：将主栈中最后一个元素弹出，小栈中元素与此相等时也弹出
        """
        pop_data = self.main_stack.pop(-1)
        if pop_data == self.min_stack[-1]:
            self.min_stack.pop(-1)
        return pop_data

    def get_min(self):
        """
        获取最小元素：返回当前主栈中元素最小值
        """
        if len(self.main_stack) > 0:
            return self.min_stack[-1]


if __name__ == '__main__':
    data_stack = MinStack()
    data_stack.push(9)
    data_stack.push(8)
    data_stack.push(7)
    data_stack.push(10)

    print('最小元素:', data_stack.get_min())

    print('弹出的元素:', data_stack.pop())
    print('弹出的元素:', data_stack.pop())
