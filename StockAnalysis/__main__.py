import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from tabulate import tabulate

from get_resource_stock_data import get_url_data
from stock_mysql import StockDataBase


def write_to_database(stock_data: tuple, stock_database: StockDataBase, last_time: datetime.datetime):
    is_insert_rows = False
    filtered_stock_data = [[] for _ in range(len(stock_data))]
    for ind, time_transaction in enumerate(stock_data[-1]):
        if time_transaction > str(last_time):
            for i in range(len(stock_data)):
                filtered_stock_data[i].append(stock_data[i][ind])
            is_insert_rows = True
    if is_insert_rows:
        stock_database.insert_rows(list(zip(*filtered_stock_data)))
    return is_insert_rows


def plot_all_stock_data(stock_data, time_type, predict_stock=None):
    price_list, time_list = [], []
    for one_stock in stock_data:
        print(*one_stock, sep='\t\t')
        price_list.append(one_stock[-2])
        time_list.append(one_stock[-1])
    print("Total Rows: {}".format(len(time_list)), end=',\t')
    print('Total Time: {}'.format(time_type))
    if len(time_list) > 40:
        plt.plot(time_list, price_list, 'g', label='Actual Price', linewidth=1.2)
        if predict_stock is not None:
            plt.plot(time_list, predict_stock, 'r--', label='Predict Price', linewidth=1.3)
    else:
        plt.plot(time_list, price_list, 'g-v', label='Actual Price', linewidth=1.2)
        if predict_stock is not None:
            plt.plot(time_list, predict_stock, 'r--v', label='Predict Price', linewidth=1.3)
    plt.legend(loc='lower right', frameon=False, ncol=1, prop={'size': 7.5})
    plt.title('Price of A Stock', fontsize=7)
    plt.ylabel('Price', fontsize=7)
    plt.xlabel('Time: {}'.format(time_type), fontsize=7)
    if len(price_list) > 30:
        plt.xticks(time_list[::len(price_list) // 30], rotation=45, fontsize=4)
    else:
        plt.xticks(time_list[::1], rotation=45, fontsize=4)
    plt.yticks(fontsize=6)
    plt.grid(axis='y')
    # 设置图片的右边框和上边框为不显示
    ax = plt.gca()  # gca:get current axis得到当前轴
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.show()


def determine_get_url(last_time, last_second_time, time_type):
    """
    todo: 判读是否已经更新到最新
    """
    today = datetime.datetime.now()
    if time_type == "TODAY":
        return True if (today - last_time) >= datetime.timedelta(days=1) else False
    time_diff = last_time - last_second_time
    if time_diff >= datetime.timedelta(days=28):  # 采集间隔：月
        return True if (today - last_time) >= datetime.timedelta(days=28) else False
    if time_diff >= datetime.timedelta(days=1):  # 采集间隔：日
        return True if (today - last_time) >= datetime.timedelta(days=1, hours=1) and today.hour >= 16 else False
    if time_diff >= datetime.timedelta(hours=1):  # 采集间隔：小时
        return True if (today - last_time) >= datetime.timedelta(hours=1) else False
    if time_diff >= datetime.timedelta(minutes=1):  # 采集间隔：分
        return True if (today - last_time) >= datetime.timedelta(minutes=1) else False
    return False


def auto_write_to_stock(time_type="All"):
    # determine whether to collect stock from URL according to db
    need_get_latest_stock = True
    stock_database: StockDataBase = StockDataBase(time_type)

    stock_data: tuple = stock_database.get_last_rows(2)
    if stock_data:
        last_time, last_second_time = stock_data[0][-1], stock_data[1][-1]
        need_get_latest_stock = determine_get_url(last_time, last_second_time, time_type)
    else:
        last_time = datetime.datetime(year=1900, month=1, day=1)

    if need_get_latest_stock:
        # fetch all ShangHai stock data from url
        stock_data_from_url = get_url_data(time_type)

        # write to stock database with filtering old time stock data
        write_to_database(stock_data_from_url, stock_database, last_time)


def fit_model(train_x, train_y):
    reg = linear_model.LinearRegression()
    reg.fit(train_x, train_y)
    return reg


def preprocess_data(transaction_data):
    """Delete data that is too large or too small"""
    s = pd.Series(transaction_data)
    low, up = 0.002, 0.97
    # low, up = 0, 1
    val_percent = s.quantile([low, up])
    ind, train_x, train_y = 1, [], []
    for one_stock_data in s:
        if val_percent[low] <= one_stock_data <= val_percent[up]:
            train_y.append([ind, one_stock_data])
            train_x.append([ind, ind])
        ind += 1
    print("deleted months number after preprocessing stock data: {}".format(len(transaction_data) - len(train_x)))
    return np.array(train_x), np.array(train_y)


def main():
    # get all A stock transaction data from URL or DataBase
    time_type = "All"
    auto_write_to_stock(time_type)

    if time_type != "All":
        stock_data = StockDataBase(time_type).get_whole_table()
        if time_type == "TODAY":
            stock_data = StockDataBase(time_type).get_rows_where(condition="stock_name in ('主板A')")
        print('\t', *StockDataBase(time_type).zh_column_names.split(','), sep='  ')
        column_names = StockDataBase(time_type).column_names.split(',')
        table = tabulate(stock_data, headers=column_names, tablefmt="simple", numalign="left", showindex="always")
        print(table)
        return

    # read stock database
    stock_database = StockDataBase(time_type)
    stock_data = stock_database.get_whole_table()

    # data preprocessing
    transaction_data = [one_stock[-2] for one_stock in stock_data]
    train_x, train_y = preprocess_data(transaction_data)

    # Identifying Data Patterns
    reg = fit_model(train_x, train_y)

    # plot actual stock data and predicted stock data
    all_transaction_data_x = [[ind, ind] for ind in range(1, len(transaction_data) + 1)]
    predict_transaction_data = list(reg.predict(all_transaction_data_x)[:, 1])
    plot_all_stock_data(stock_data, time_type, predict_transaction_data)

    # future stock data predicted by model
    predict_x = np.array([[i, i] for i in range(len(transaction_data), len(transaction_data) + 3)])
    print("未来 {} 个月的预测值:".format(predict_x.shape[0]))
    print(reg.predict(predict_x))


if __name__ == "__main__":
    main()
