"""
计数排序
"""
import random


def sort_count(nums: list):
    # 首先创建全零的数组用于计数
    list_sort = [0] * (max(nums) + 1)
    for i in nums:
        list_sort[i] += 1
    # 根据计数结果用于展开成排序后结果
    result = []
    for index, item in enumerate(list_sort):
        if item > 0:
            result.extend([index] * item)
    return result


if __name__ == '__main__':
    data = list(range(10)) + list(range(5, 9))
    random.shuffle(data)
    print('原始列表：', data)

    res = sort_count(data)
    print('排序后的列表: ', res)
