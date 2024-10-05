import pymysql


class DataBase:
    def __init__(self, time_type='All'):
        """
        time_type: used to determine which table
        """
        kwargs = {
            "host": "localhost",
            "port": 3306,  # mysql command: show global variables like 'port';
            "user": "root",
            "passwd": "root",
            "database": "stock_a",
            "charset": "utf8"
        }
        self.table_name = "price_{}_table".format(time_type)
        self.db = pymysql.connect(**kwargs)
        self.cur = self.db.cursor()
        self.create_table_sql = ""
        self.column_names = ""

    def _create_table(self):
        self._execute(self.create_table_sql)

    def _execute(self, sql: str, data=None) -> bool:
        try:
            if not data:
                self.cur.execute(sql)
            else:
                self.cur.executemany(sql, data)
            self.db.commit()  # 提交事务
            return True
        except Exception as e:
            self.db.rollback()  # 失败，数据库回滚
            print("error: {}".format(e))
            return False

    def _get_column_num(self):
        return self.column_names.count(',') + 1

    def _fetch_rows(self, sql: str) -> tuple:
        try:
            self.cur.execute(sql)
            fetch_rows = self.cur.fetchall()
            print("succeed to get rows from db: {}".format(len(fetch_rows)))
        except Exception as e:
            fetch_rows = tuple()
            print("fail to get rows from db: {}.".format(e))
            if "doesn't exist" in str(e):
                self._create_table()
        return fetch_rows

    def __del__(self):
        try:
            self.cur.close()
            self.db.close()
        finally:
            pass

    def insert_rows(self, data):
        sql = f'insert into {self.table_name} ({self.column_names}) values (' + ('%s,' * self._get_column_num())[
                                                                                :-1] + ');'
        if self._execute(sql, data):
            print("succeed to insert rows: {}.".format(len(data)))
        else:
            print("fail to insert rows: {}.")

    def get_last_rows(self, number):
        sql = "select {} from {} order by id desc limit {};".format(self.column_names, self.table_name, number)
        return self._fetch_rows(sql)

    def get_whole_table(self) -> tuple:
        sql = "select {} from {};".format(self.column_names, self.table_name)
        return self._fetch_rows(sql)

    def get_table_name(self):
        return self.table_name

    def get_rows_where(self, condition: str, choose_obj: str = "*"):
        if not condition:
            raise ValueError("condition is empty")
        sql = "select {} from {} where {}".format(choose_obj, self.table_name, condition)
        return self._fetch_rows(sql)


class MSNStockDataBase(DataBase):
    def __init__(self, time_type='All'):
        """
        time_type: used to determine which table
        """
        time_type_list = ['All', '1Y', '3Y', '5Y', '1M', '3M', '1D', '5D']
        if time_type not in time_type_list:
            raise ValueError(f"{time_type} not in {time_type_list}")
        DataBase.__init__(self, time_type)
        self.create_table_sql = f"""
        create table {self.table_name}(
            id int primary key auto_increment,
            price_low float,
            price_high float,
            open_price float,
            price float,
            transaction_time datetime
            );
        """
        self.column_names = 'price_low,price_high,open_price,price,transaction_time'
        self.zh_column_names = "最低价,最高价,开盘价,收盘价,交易时间"


class SSEStockDataBase(DataBase):
    def __init__(self, time_type='TODAY'):
        """
        time_type: used to determine which table
        """
        time_type_list = ['TODAY']
        if time_type not in time_type_list:
            raise ValueError(f"{time_type} not in {time_type_list}")
        DataBase.__init__(self, time_type)
        self.create_table_sql = f"""
        create table {self.table_name}(
            id int primary key auto_increment,
            list_num int,
            total_value double,
            nego_value double,
            trade_amt double,
            trade_vol double,
            avg_pe_rate double,
            total_to_rate double,
            nego_to_rate double,
            stock_name char(30) not null,
            time datetime
            );
        """
        self.column_names = 'list_num,total_value,nego_value,trade_amt,trade_vol,' \
                            'avg_pe_rate,total_to_rate,nego_to_rate,stock_name,time'
        self.zh_column_names = '挂牌数,市价总值(亿元),流通市值(亿元),成交金额(亿元),成交量(亿股/亿份),' \
                               '平均市盈率(倍),换手率(%),流通换手率(%),股票类型,时间'


class StockDataBase(MSNStockDataBase, SSEStockDataBase):
    def __init__(self, time_type='All'):
        """
        time_type: used to determine which table
        """
        msn_time_type_list = ['All', '1Y', '3Y', '5Y', '1M', '3M', '1D', '5D']
        sse_time_type_list = ['TODAY']
        if time_type in msn_time_type_list:
            MSNStockDataBase.__init__(self, time_type)
        elif time_type in sse_time_type_list:
            SSEStockDataBase.__init__(self, time_type)
        else:
            raise ValueError("{} not in {}".format(time_type, msn_time_type_list + sse_time_type_list))
