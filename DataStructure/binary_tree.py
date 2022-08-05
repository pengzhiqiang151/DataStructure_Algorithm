class TreeNode:
    """
    构建树的节点
    """
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def create_binary_tree(input_list=[]):
    """
    构建二叉树
    首先构建当前节点，其次用列表的一半数据分别构建左右节点，构建左右节点和原问题相同，故用递归
    此函数中递归的终止条件是input_list为None或为空
    或data为None
    :param input_list: 待构建树
    :return:
    """
    if input_list is None or len(input_list) == 0:
        return None
    data = input_list.pop(0)
    if data is None:
        return None
    node = TreeNode(data)
    input_list_left = input_list[:len(input_list)//2]
    input_list_right = input_list[len(input_list)//2:]
    node.left = create_binary_tree(input_list_left)         # 递归(重复执行构建左子树)
    node.right = create_binary_tree(input_list_right)       # 递归(重复执行构建右子树)
    return node


def pre_order_traversal(node):
    """
    前序遍历
    首先输出根节点，然后用递归遍历左子树和右子树（子问题和原问题相同）
    本递归的终止条件是：当前节点为None
    :param node:
    :return:
    """
    if node is None:
        return
    print(node.data)
    pre_order_traversal(node.left)      # 遍历左子树的方法和遍历别的节点方法相同，故采用了递归
    pre_order_traversal(node.right)     # 递归遍历右子树


def post_order_traversal(node):
    """
    后序遍历
    首先输出左节点，然后输出右节点(子问题和原问题相同，递归)，最后输出本节点数据
    递归终止条件是：节点为空
    :param node:
    :return:
    """
    if node is None:
        return
    post_order_traversal(node.left)
    post_order_traversal(node.right)
    print(node.data)


def mid_order_traversal(node):
    """
    中序遍历
    首先输出左节点(左节点同样为树，和原问题相同，用递归)，其次输出本节点数据，最后输出本节点数据(同左节点)
    递归终止条件是：本节点为空
    :param node:
    :return:
    """
    if node is None:
        return
    mid_order_traversal(node.left)
    print(node.data)
    mid_order_traversal(node.right)


if __name__ == '__main__':
    tree = create_binary_tree([1, 2, 3, 4, 5])
    # pre_order_traversal(tree)
    # mid_order_traversal(tree)
    post_order_traversal(tree)
    a = 1
