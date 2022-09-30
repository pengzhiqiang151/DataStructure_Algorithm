def search(num, arr, start, end):
    """
    递归法（相当于该函数只实现了一次查询, 故而非常简单）
    :param num:
    :param arr:
    :param start:
    :param end:
    :return:
    """
    if start > end:
        print('not exist')
        return
    mid = (start + end) // 2
    if num == arr[mid]:
        print('index of finding value is {}'.format(mid))
    if num < arr[mid]:
        search(num, arr, start, mid - 1)    # 子问题和原问题相同，故采用递归法实现
    if num > arr[mid]:
        search(num, arr, mid + 1, end)


if __name__ == '__main__':
    res = list(range(0, 10))
    print(res)

    search(2, res, start=0, end=len(res) - 1)
