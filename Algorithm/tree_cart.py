import numpy as np
import sklearn.datasets as sd
import sklearn.utils as su
import pandas as pd
from copy import deepcopy


class TreeNode:
    """类：树的节点"""

    def __init__(self, dt=None):
        self.data = dt  # 当前节点数据
        self.rule = None  # 分裂规则    （特征的索引，阈值）
        self.left = None  # 左节点的指向
        self.right = None  # 右节点的指向
        self.predict = None  # 预测结果 (叶节点)


class CartTree(object):
    """类：训练一棵树，预测树的结果"""

    def __init__(self, *, depth: int):
        self.depth = depth
        self.tree = None  # 初始化树的根节点
        self.num_leaf = 0  # 记录叶节点的个数

    @staticmethod
    def calculate_inf_gain(dt: pd.DataFrame, ind: int):
        """分类问题
        计算当前特征当前分裂节点下的信息增益
        ind 为分裂节点的行级索引"""
        df_left = dt[dt.iloc[:, 1] <= dt.iloc[ind, 1]]
        df_right = dt[dt.iloc[:, 1] > dt.iloc[ind, 1]]

        value_counts_right = df_right[0].value_counts()
        sum_right = sum(value_counts_right)
        right_pow = sum(value_counts_right.apply(lambda value: value ** 2))
        score_right = 0 if sum_right == 0 else right_pow / sum_right

        value_counts_left = df_left[0].value_counts()
        sum_left = sum(value_counts_left)
        left_pow = sum(value_counts_left.apply(lambda value: value ** 2))
        score_left = 0 if sum_left == 0 else left_pow / sum_left
        return score_left + score_right

    def find_split(self, dt: np.array):
        """寻找最优分裂节点"""
        df = pd.DataFrame(dt)
        score_best = 0  # 全局最好点的指标
        list_best = None  # 保存最好的分裂点，包含特征和具体的值
        for i in range(1, len(df.columns)):  # 遍历每一个特征
            # 将数据按照当前特征排序
            dt_temp = deepcopy(df[[0, i]]).sort_values(by=i)
            dt_temp.index = range(dt_temp.shape[0])
            # 遍历该特征的每一个分裂点计算分裂指标（分类：信息增益，回归：均方误差）
            for ind in range(dt_temp.shape[0]):
                inf_gain = self.calculate_inf_gain(dt_temp, ind)
                if inf_gain > score_best:
                    list_best = [i, dt_temp.loc[ind, i]]  # 保存此时的最优分裂点
                    score_best = inf_gain
            print(f'当前已训练 {i} 特征,', '最优特征', score_best, list_best)
        return list_best

    def train(self, dt: np.array, depth: int = 0):
        """创建树"""
        # 创建节点
        node = TreeNode()
        # 终止条件: 深度超过设定值, 样本类别为 1, 节点样本数小于阈值
        depth += 1
        print('树的深度: {}'.format(depth))
        if depth > self.depth or sum(dt[:, 0] != dt[0, 0]) == 0 or dt.shape[0] <= 10:
            node.predict = pd.DataFrame(dt[:, 0]).mode().iloc[0, 0]  # 为叶节点赋值
            self.num_leaf += 1
            print('生成第 {} 个 叶节点, 输出值 {}'.format(self.num_leaf, node.predict))
            return node
        # 寻找当前节点的分裂规则(特征、分裂值) [ind, value]   (dt[ind] ? value)
        node.rule = self.find_split(dt)
        # 递归创建左子树和右子树
        data_left = dt[dt[:, node.rule[0]] <= node.rule[1], :]
        data_right = dt[dt[:, node.rule[0]] > node.rule[1], :]
        if data_left.shape[0] == 0:  # 左节点样本数为空, 终止
            node.left = TreeNode()  # 生成左叶节点
            node.left.predict = pd.DataFrame(dt[:, 0]).mode().iloc[0, 0]  # 为叶节点赋值
            self.num_leaf += 1
            print('生成第 {} 个 叶节点, 输出值 {}'.format(self.num_leaf, node.left.predict))
            return
        if data_right.shape[0] == 0:  # 右节点样本数为空, 终止
            node.right = TreeNode()  # 生成右叶节点
            node.right.predict = pd.DataFrame(dt[:, 0]).mode().iloc[0, 0]  # 为叶节点赋值
            self.num_leaf += 1
            print('生成第 {} 个 叶节点, 输出值 {}'.format(self.num_leaf, node.right.predict))
            return
        node.left = self.train(data_left, depth)
        node.right = self.train(data_right, depth)
        # 创建完成后返回当前节点
        print('完成一个节点的训练')
        return node

    def predict_sample(self, node: TreeNode, one_sample):
        """遍历决策树, 找到叶子节点"""
        # 终止条件
        if node.predict is not None:
            print('当前预测结果：{}'.format(node.predict))
            return node.predict
        # 查询左节点 (注：索引数比训练时少一个)
        if one_sample[node.rule[0]-1] <= node.rule[1]:
            return self.predict_sample(node.left, one_sample)
        # 查询右节点
        else:
            return self.predict_sample(node.right, one_sample)

    def predict(self, node: TreeNode, dt: np.array):
        result = []
        for sample in dt:
            result.append(self.predict_sample(node, sample))
        return result


if __name__ == '__main__':
    boston = sd.load_breast_cancer()
    print(type(boston))

    random_seed = 7
    x, y = su.shuffle(boston.data, boston.target, random_state=random_seed)
    data = np.hstack((y.reshape(-1, 1), x))

    model = CartTree(depth=2)
    tree_node = model.train(data)

    y_predict = model.predict(tree_node, x)

    num_acc = 0
    for i in range(len(y_predict)):
        if y_predict[i] == y[i]:
            num_acc += 1
    print('acc:', num_acc/len(y_predict))

