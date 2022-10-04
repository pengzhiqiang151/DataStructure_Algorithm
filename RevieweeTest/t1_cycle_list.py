class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def is_cycle(node: Node):
    """
    判断链表是否有环：
    就像操场赛跑一样，有环问题，前进快的可以追上慢的
    :param node:
    :return:
    """
    p1 = node                   # 创建p1指针
    p2 = node                   # 创建p2指针
    while p2 is not None and p2.next is not None:
        p1 = p1.next            # p1前进一步
        p2 = p2.next.next       # p2前进二步
        if p1 is p2:     # 比较前进之后地址是否相同
            return True
    return False


def cycle_length(head: Node):
    """
    判断链表中环的长度:
    解题思路: 操场上的运动员第二次追上慢的运动员所多跑的长度
    :param head:
    :return:
    """
    p1 = head
    p2 = head
    length_cycle = 0
    while p2 is not None and p2.next is not None:       # 只有保证 p2 当前节点和下一节点非空
        p1 = p1.next
        p2 = p2.next.next
        if p1 == p2:
            break
    while p2 is not None and p2.next is not None:
        p1 = p1.next
        p2 = p2.next.next
        length_cycle += 1                               # p2每步比p1多走的距离
        if p1 is p2:
            return length_cycle


def entry_point(head: Node):
    """
    判断链表的入环节点:
    相遇后，其中一人重从起点跑，同等速度后第二次相遇的入环节点即是
    """
    p1 = head
    p2 = head
    while p2 is not None and p2.next is not None:
        p1 = p1.next
        p2 = p2.next.next
        if p1 is p2:                # 相遇
            break
    p2 = head
    while p2 is not None:
        p1 = p1.next
        p2 = p2.next
        if p1 is p2:                # 这次相遇节点即为入环节点
            return p2


if __name__ == '__main__':

    node1 = Node(5)         # 创建节点对象
    node2 = Node(5)         # 创建节点对象
    node3 = Node(7)         # 创建节点对象
    node4 = Node(2)         # 创建节点对象
    node5 = Node(6)         # 创建节点对象
    node1.next = node2      # 创建节点指向关系
    node2.next = node3      # 创建节点指向关系
    node3.next = node4      # 创建节点指向关系
    node4.next = node5      # 创建节点指向关系
    node5.next = node2      # 创建节点指向关系
    print(is_cycle(node1))

    length = cycle_length(node1)
    print('环的长度: {}'.format(length))

    entry = entry_point(head=node1)
    print('入环节点', entry)

