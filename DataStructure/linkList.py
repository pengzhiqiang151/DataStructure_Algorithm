"""
链表及其基本操作: 增、删、改、查
"""


class Node:
    """
    创建链表中的一个节点
    """
    def __init__(self, data):
        self.data = data
        self.next = None  # 存储下一个节点对象


class LinkedList:
    """
    创建链表
    """
    def __init__(self):
        self.size = 0  # 记录链表大小
        self.head = None  # 头指针: 指向头节点(Node对象)
        self.last = None  # 尾指针: 指向尾节点(Node对象)

    def get(self, index) -> Node:
        """按照索引返回链表某个节点"""
        if index < 0 or index >= self.size:
            raise Exception("超出链表节点范围！")
        p = self.head
        for i in range(index):
            p = p.next
        return p

    def insert(self, data, index):
        """链表基本操作: 增"""
        if index < 0 or index > self.size:
            raise Exception("超出链表节点范围！")
        node = Node(data)  # 创建节点
        if self.size == 0:
            # 空链表
            self.head = node
            self.last = node
        elif index == 0:
            # 插入头部
            node.next = self.head
            self.head = node
        elif self.size == index:
            # 插入尾部
            self.last.next = node       # 尾部节点指向当前节点
            self.last = node            # 使尾部指针指向最后一个节点
        else:
            # 插入中间
            prev_node = self.get(index - 1)
            node.next = prev_node.next
            prev_node.next = node
        self.size += 1

    def remove(self, index):
        if index < 0 or index >= self.size:
            raise Exception("超出链表节点范围！")
        # 暂存被删除的节点，用于返回
        if index == 0:
            # 删除头节点
            removed_node = self.head
            self.head = self.head.next
            if self.size == 1:
                self.last == Node
        elif index == self.size - 1:
            # 删除尾节点
            prev_node = self.get(index - 1)
            removed_node = prev_node.next
            prev_node.next = None
            self.last = prev_node
        else:
            # 删除中间节点
            prev_node = self.get(index - 1)
            next_node = prev_node.next.next
            removed_node = prev_node.next
            prev_node.next = next_node
        self.size -= 1
        return removed_node

    def output(self):
        p = self.head
        while p is not None:
            print(p.data)
            p = p.next


linkedList = LinkedList()
linkedList.insert(3, 0)
linkedList.insert(4, 0)
linkedList.insert(9, 2)
linkedList.insert(5, 3)
linkedList.insert(6, 1)
linkedList.remove(0)
linkedList.output()
