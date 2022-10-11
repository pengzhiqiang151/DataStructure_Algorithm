"""
求 a 和 b 两个整数的最大公约数
辗转相除法
更相减损术
"""


def max_divisor(a, b):
    """
    辗转相除法
    """
    max_num = a if a > b else b  # 取最大最小值，可以不必要写这么麻烦（嘿哈）
    min_num = a if a <= b else b
    remainder = max_num % min_num
    if remainder == 0:  # 终止，较小数即为所求最大公约数
        return min_num
    return max_divisor(min_num, remainder)  # 需要理解该处为啥要加return(若只有if后的，则仅返回到倒数第二层)


def max_divisor_decrease(a, b):
    """
    更相减损术
    """
    if a == b:
        return a
    max_num = max(a, b)
    min_num = min(a, b)
    c = max_num - min_num
    return max_divisor_decrease(min_num, c)


if __name__ == '__main__':
    result = max_divisor_decrease(25, 10)
    print('最大公约数:', result)
