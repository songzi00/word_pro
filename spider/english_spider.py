import requests,random,re
from bs4 import BeautifulSoup
import pymysql

# 设置数据库
connect = pymysql.connect(
        host = '127.0.0.1',
        db = 'Book',   #数据名称
        port = 3306,
        user = 'root',
        passwd = '20001124',    #数据库密码
        charset = 'utf8',
        )
cursor = connect.cursor()






url_list = ['http://en-brief.xiao84.com/meiwen/p{}.html'.format(i) for i in range(1,10)]


def book_detail(detail_url):
    detail_url_list = []
    res = requests.get(detail_url)
    res = res.content.decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')
    detail_list = soup.select('.title > a')
    for detail in detail_list:
        detail_url_list.append(detail['href'])

    return detail_url_list


def book_data(url,type):
    res = requests.get(url)
    res = res.content.decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')

    title = soup.select('.title > h1')[0].get_text()

    title = re.sub('[\u4e00-\u9fa5]','',title) #去除中文字符

    content = soup.select('.content')[0].get_text()
    content = re.sub(r'[\u4e00-\u9fa5。，；\n\r\t]','',content)

    try:
        sql = 'insert into myapp_book(types,title,content) VALUES (%s,%s,%s)'

        cursor.execute(sql, (
            type,title,content))
        connect.commit()
        print('--------------{}数据已存入mysql--------------------'.format(type))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    types = ['英语美文', '英语小短文', '英语散文', '英语演讲', '英语阅读']
    for url in url_list:
        for u in book_detail(url):
            try:
                book_data(u,random.choice(types))
            except:
                pass




