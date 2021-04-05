# coding=utf-8
import arrow
import requests
import json
import os
import pickle
import MySQLdb
import time
import html


class WeatherRepoter(object):
    """
    获取天气预报
    :param str location: 地区
    ```location``` 地区参数可以为整形也可以为字符串
    """

    def __init__(self, location):
        self.cur_url = self.cururlmaker(location)
        self.headers = self.header_maker(location)
        self.current = None  # 当前天气字典
        self.get_data()

    def get_data(self):
        """
        获取日历数据以及实时数据
        访问地址时，需要带上时间参数以及Referer的headers
        """
        # 生成时间参数
        params = {'_': arrow.get().timestamp() * 1000}

        # 获取实时数据
        resp = requests.get(self.cur_url, headers=self.headers, params=params)

        self.current = self.parse(resp.content)

    def cururlmaker(self, location):
        """当前天气URL"""
        return f"http://d1.weather.com.cn/sk_2d/{location}.html"

    def parse(self, data):
        data = data.decode("utf-8").split('=')[1]
        # 转换小于号 <
        data = html.unescape(data)
        data = json.loads(data)
        info = []
        for k, v in data.items():
            info.append(v)
        return info

    def header_maker(self, location):
        """生成合法headers"""
        return {"Referer": f"http://www.weather.com.cn/weather40dn/{location}.shtml",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"}


with open('city_code_list.pickle', 'rb') as f:
    city_list = pickle.load(f)

for id in city_list:

    db = MySQLdb.connect(host="", user="", password="", port=3306, database="star_charge_app", charset='utf8')

    cursor = db.cursor()
    try:
        wr = WeatherRepoter(id)
        wr.current.pop(9)
        cursor.execute(
            "INSERT INTO weather(nameen,cityname,city,temp,tempf,WD,wde,WS,wse,"
            "time,weather,weathere,weathercode,qy,njd,sd,rain,rain24h,aqi,limitnumber,aqi_pm25,date) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            wr.current)
        db.commit()
    except Exception as e:
        print('a', str(e))
