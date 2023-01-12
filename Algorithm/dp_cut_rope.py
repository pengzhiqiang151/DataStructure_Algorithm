def find_max(n):
    """
    自上而下考虑问题:
    此问题为 n 长度的绳子，切割成若干段的 乘机最大化 问题       注：最优化问题
    第一刀: 第一段长度为 i ，第二段长度为 n-i , 则有 max f(n) = max f(i) * max f(n-i)   注: 整体问题的最优解依赖子问题的最优解

    循环从下而上求解整体问题的最优解
    n: 绳子长度
    """
    best_result = {1: 1, 2: 1, 3: 2}  # 1 只是为了后面计算方便
    for i in range(4, n + 1):
        # 自下而上查找最优解
        val_max = 0
        for first_data in range(1, i // 2 + 1):
            second_data = i - first_data
            data1 = first_data if first_data > best_result[first_data] else best_result[first_data]  # 不分和切分选最大
            data2 = second_data if second_data > best_result[second_data] else best_result[second_data]  # 不分和切分选最大
            res_mul = data2 * data1
            if res_mul > val_max:
                val_max = res_mul
        best_result[i] = val_max
        print(best_result)


find_max(10)
