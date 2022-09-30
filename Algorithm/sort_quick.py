import random


def partition_v1(start_index, end_index, arr):
    """实现一次快排(直至本地握手),
    列表顺序无需返回, 但是需返回基准元素位置

    注： 仅改变左右指针与基准元素比较时的大于小于号即可实现升序降序"""
    pivot_index = start_index       # 此处不能为零, 因为并非每次其实索引都是0， 有可能是列表的后半部分
    # 循环遍历，进行交换
    while start_index != end_index:
        # 先从右节点开始查询
        while arr[end_index] > arr[pivot_index] and end_index > start_index:
            end_index -= 1
        # 再从左节点开始查询
        while arr[start_index] < arr[pivot_index] and end_index > start_index:
            start_index += 1
        # 交换数据
        temp = arr[start_index]
        arr[start_index] = arr[end_index]
        arr[end_index] = temp
    temp = arr[pivot_index]
    arr[pivot_index] = arr[start_index]
    arr[start_index] = temp
    return start_index


def quick_sort(start_index, end_index, arr):
    """
    用递归实现每部分的排序

    注: 只能先移动右指针，才能保住很面的很多问题"""
    if start_index >= end_index:
        return
        # 一次排序，得的基准位置，并使得列表在基准前后位置有序
    pivot_index = partition_v1(start_index, end_index, arr)
    # 实现基准元素前后部分的排序 (与原问题相同)
    quick_sort(start_index, pivot_index - 1, arr)
    quick_sort(pivot_index + 1, end_index, arr)


if __name__ == '__main__':
    data = list(range(10))
    random.shuffle(data)
    print('原始数据:', data)

    quick_sort(0, len(data) - 1, data)
    print('排序后的数据:', data)
