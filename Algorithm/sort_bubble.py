import numpy as np
import random


def bubble_sort(arr, data_sort, is_sort=True):
    """
    通过递归实现的冒泡排序
    arr: 待排序的list
    data_sort: 排序完成后的list

    该设计的最大问题在于需要创建一个单独的列表用于存储排序结果。
    元素有序时，依然需要用for循环去改变原来的变量。
    而在多次的递归调用中，保持和原始数据有相同的索引是较为困难的。
    """
    print('当前列表:', arr)
    if len(arr) == 1:       # 已经排序到最后一个元素
        data_sort.insert(0, arr[0])
        return arr
    # 实现一轮冒泡排序
    for i in range(len(arr)-1):
        if arr[i] > arr[i+1]:
            temp = arr[i]
            arr[i] = arr[i + 1]
            arr[i+1] = temp
            is_sort = False
    if is_sort is True:        # 剩下元素已经有序
        for i in range(len(arr)):
            data_sort.insert(0, arr[-i-1])
        return
    data_sort.insert(0, arr[-1])
    bubble_sort(arr[:-1], data_sort)


if __name__ == '__main__':
    arr = list(np.arange(-10, 10))
    data_sort = []
    random.shuffle(arr)
    # print(data)

    bubble_sort(arr, data_sort)
    print(data_sort)
