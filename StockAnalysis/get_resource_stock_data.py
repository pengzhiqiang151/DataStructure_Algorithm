import datetime

from bs4 import BeautifulSoup
import re
import requests


def str_to_time(param):
    if len(param) != 8:
        raise ValueError("param: {} is not correct".format(param))
    return param[:4] + '-' + param[4:6] + '-' + param[6:]


def code_to_stock_name(param):
    if param == '01':
        return '主板A'
    elif param == '02':
        return "主板B"
    elif param == '03':
        return "科创板"
    elif param == '11':
        return "股票回购"
    elif param == '17':
        return "股票"
    else:
        raise ValueError(f'code {param} is out of limit')


def str_to_float(param: str) -> str:
    try:
        float(param)
        return param
    except ValueError:
        return '-1'
    except Exception as e:
        raise Exception(f"function is_float error: {e}")


class Crawler:
    def __init__(self, time_type="All"):
        self.time_type = time_type
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
        }
        self.url = ""
        self.param = None

    def _fetch_url(self):
        html_file = requests.get(self.url, headers=self.headers, params=self.param)
        obj_soup = BeautifulSoup(html_file.text, "lxml")  # actually not to be used
        text_data = obj_soup.body.text
        return text_data

    def parse_url_data(self):
        pass


class MSNCrawler(Crawler):
    time_type_list = ['All', '1Y', '3Y', '5Y', '1M', '3M', '1D', '5D']

    def __init__(self, time_type="All"):
        if time_type not in self.time_type_list:
            raise ValueError(f"{time_type} not in {self.time_type_list}")
        Crawler.__init__(self, time_type)
        # https://www.msn.cn/zh-cn/money/chart?id=adfh77&timeFrame=1D&chartType=line&projection=false
        if time_type == '1D':
            self.url = "https://assets.msn.cn/service/Finance/QuoteSummary?" \
                       "apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&" \
                       "activityId=ADBC7810-1FD6-4FBD-8F17-6A2F3F156D87&" \
                       "ocid=finance-utils-peregrine&cm=zh-cn&it=edgeid&" \
                       "scn=APP_ANON&ids=adfh77&intents=Charts&type=1D1M&" \
                       "wrapodata=false"
        else:
            self.url = "https://assets.msn.cn/service/Finance/QuoteSummary?" \
                       "apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&" \
                       "activityId=F0A06A2D-CED9-47B6-93A7-C30193D0A2AE&" \
                       "ocid=finance-utils-peregrine&cm=zh-cn&it=edgeid&" \
                       "scn=APP_ANON&ids=adfh77&intents=Charts&wrapodata=false"
            self.param = {
                "type": time_type  # time: 'All', '1Y', '3Y', '5Y', '1M', '3M', '5D'
            }

    def parse_url_data(self):
        # extract prices
        text_data = self._fetch_url()
        print(text_data)
        open_prices_list = list(
            map(float, re.findall('"openPrices":\\[(.*?)],', text_data, re.S)[0].split(',')))
        prices_list = list(map(float, re.findall('"prices":\\[(.*?)],', text_data, re.S)[0].split(',')))
        high_prices_list = list(
            map(float, re.findall('"pricesHigh":\\[(.*?)],', text_data, re.S)[0].split(',')))
        low_prices_list = list(map(float, re.findall('"pricesLow":\\[(.*?)],', text_data, re.S)[0].split(',')))
        timestamps = re.findall('"timeStamps":\\[(.*?)],', text_data, re.S)[0]
        timestamps_list = timestamps.replace('T', ' ').replace('Z', '').replace('"', '').split(',')
        local_time_list, time_format = [], "%Y-%m-%d %H:%M:%S"
        for timestamp in timestamps_list:  # add 8 hours difference (UTC + 8 hours)
            local_time_list.append(
                str(datetime.datetime.strptime(timestamp, time_format) + datetime.timedelta(hours=8)))

        assert len(open_prices_list) == len(prices_list) == len(high_prices_list) == len(low_prices_list) == len(
            local_time_list)
        print("the number of collecting stock transaction data from URL is: {}.".format(len(local_time_list)))

        return low_prices_list, high_prices_list, open_prices_list, prices_list, local_time_list


class SSECrawler(Crawler):
    time_type_list = ['TODAY']

    def __init__(self, time_type="TODAY"):
        if time_type not in self.time_type_list:
            raise ValueError(f"{time_type} not in {self.time_type_list}")
        Crawler.__init__(self, time_type)
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'connection': 'keep-alive',
            'host': 'query.sse.com.cn',
            'referer': 'https://www.sse.com.cn/',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        }
        self.url = "https://query.sse.com.cn/commonQuery.do?" \
                   "jsonCallBack=jsonpCallback52237648&" \
                   "sqlId=COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C&" \
                   "PRODUCT_CODE=01%2C02%2C03%2C11%2C17&type=inParams&" \
                   "SEARCH_DATE=&_=1728655793860"
        self.param = None

    def parse_url_data(self):
        total_value_list = []
        trade_vol_list = []
        avg_pe_rate_list = []
        total_to_rate_list = []
        trade_amt_list = []
        trade_num_list = []
        nego_value_list = []
        nego_to_rate_list = []
        time_list = []
        list_num_list = []
        stock_name_list = []
        temp_result = re.findall('"result":\\[(.*?)]', self._fetch_url(), re.S)[0]
        result_list = re.findall("{(.*?)}", temp_result, re.S)
        for result in result_list:
            total_value_list.append(str_to_float(re.findall('TOTAL_VALUE":"(.*?)",', result, re.S)[0]))
            trade_vol_list.append(str_to_float(re.findall('TRADE_VOL":"(.*?)",', result, re.S)[0]))
            avg_pe_rate_list.append(str_to_float(re.findall('AVG_PE_RATE":"(.*?)",', result, re.S)[0]))
            total_to_rate_list.append(str_to_float(re.findall('TOTAL_TO_RATE":"(.*?)",', result, re.S)[0]))
            trade_amt_list.append(str_to_float(re.findall('TRADE_AMT":"(.*?)",', result, re.S)[0]))
            trade_num_list.append(str_to_float(re.findall('TRADE_NUM":"(.*?)",', result, re.S)[0]))
            nego_value_list.append(str_to_float(re.findall('NEGO_VALUE":"(.*?)",', result, re.S)[0]))
            nego_to_rate_list.append(str_to_float(re.findall('NEGO_TO_RATE":"(.*?)",', result, re.S)[0]))
            time_list.append(str_to_time(re.findall('TRADE_DATE":"(.*?)",', result, re.S)[0]))
            list_num_list.append(str_to_float(re.findall('LIST_NUM":"(.*?)",', result, re.S)[0]))
            stock_name_list.append(code_to_stock_name(re.findall('PRODUCT_CODE":"(.*?)"', result, re.S)[0]))
        return (list_num_list, total_value_list, nego_value_list, trade_amt_list, trade_vol_list, avg_pe_rate_list,
                total_to_rate_list, nego_to_rate_list, stock_name_list, time_list)


def get_url_data(time_type="All"):  # 类似于简单工厂模式
    if time_type in MSNCrawler.time_type_list:
        crawler = MSNCrawler(time_type)
    else:
        crawler = SSECrawler(time_type)
    return crawler.parse_url_data()


if __name__ == "__main__":
    url_result = get_url_data('TODAY')
    print(len(url_result), *url_result, sep='\n')
