#!/usr/bin/python
# -*-coding:utf-8-*-
# Author zhl

import importlib, sys

importlib.reload(sys)

import MySQLdb.cursors

import datetime
from mailer import Mailer
from mailer import Message
from jinja2 import Environment, PackageLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from time import sleep


def fetch_result():
    today = datetime.datetime.today()
    seven_day_ago = today - datetime.timedelta(days=7)

    today_str = today.strftime('%Y-%m-%d')
    seven_day_ago_str = seven_day_ago.strftime('%Y-%m-%d')
    db = MySQLdb.connect(host='127.0.0.1', port='3306', user='root', password='root', db='test', charset='utf8',
                         cursorclass=MySQLdb.DictCursor)
    cursor = db.cursor()
    sql = "SELECT * FROM test.test WHERE start_time < '{today}' and start_time >= '{seven_day_ago}'".format(
        today=today_str, seven_day_ago=seven_day_ago_str)
    cursor.execute(sql)
    resullts = cursor.fetchall()
    db.close()
    return resullts


def screen_shot(event_id):
    # driver = webdriver.PhantomJS(executable_path="G:\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disables-gpu')
    driver = webdriver.Chrome(executable_path="G:\\chromedriver.exe", chrome_options=chrome_options)

    driver.set_page_load_timeout(20)
    driver.set_window_size('1920', '1080')

    url = 'http://www.xjfeihu.com/portal.php?mod=view&aid={}'.format(event_id)
    driver.get(url)
    sleep(5)

    img_path = 'D:\python_pro\screen_shot\image\event_{}.png'.format(event_id)
    driver.save_screenshot(img_path)

    # element = driver.find_element_by_id('main')
    # left = int(element.location['x'])
    # top = int(element.location['y'])
    # right = int(element.location['x'] + element.size['width'])
    # bottom = int(element.location['y'] + element.size['height'])
    # driver.quit()
    #
    # im = Image.open(img_path)
    # im = im.crop(left, top, right, bottom)
    # im.save(img_path)


def send_mail(results):
    env = Environment(loader=PackageLoader('jinja2', 'D:\\python_pro\\get_img\\templates'))
    template = env.get_template("D:\\python_pro\\get_img\\templates\\mail.html")

    message = Message(From='784440822@qq.com', To='zhenghl1126@126.com', charset='utf-8')
    message.Subject = 'test'
    message.Html = template.render(results=results)
    message.Body = "teetss"

    for r in results:
        message.attach("D:\\python_pro\\screen_shot\\image\\event_{}.png".format(r['id'], cid=r['id']))
        message.attach("D:\\python_pro\\screen_shot\\image\\event_{}.png".format(r['id']))

        sender = Mailer(host="smtp.qq.com", port=465, usr='784440822@qq.com', pwd='ufdvoeqqcchlbbha', use_ssl=True,
                        use_plain_auth=True)
        sender.send(message)


if __name__ == '__main__':
    data = [{'name': '我的', 'type': '测试', 'start_time': '2019.12.36', "end_time": "2019.2.3", "place": "地方",
             "description": "描述",
             "id": "5131"}]
    for row in data:
        screen_shot(row['id'])

    send_mail(data)
