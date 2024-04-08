# 爬取所有100个页面的内容
import csv
import requests
from bs4 import BeautifulSoup

# 1.设置浏览器代理，构造字典
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}

# 2.创建并打开文件夹，写入内容

fp = open("./豆瓣top100.csv", 'w', encoding='utf8', newline='')
writer = csv.writer(fp)
writer.writerow(('排名', '名称', '链接', '评分'))

# 3.循环所有页面
for page in range(0, 100, 25):
    print("正在获取第%s页" % page)
    url = 'https://movie.douban.com/top250?start=%s&filter=' % page
    # 4.请求源代码，向服务器发出请求
    response = requests.get(url=url, headers=headers).text
    # # 5.看做筛子筛取数据
    # html_etree = etree.HTML(reponse)
    #
    # # 6.过滤
    # li = html_etree.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li')
    # for item in li:
    #     rank = item.xpath('./div/div[1]/em/text()')[0]  # 电影排名
    #
    #     name = item.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0]  # 电影名字
    #
    #     dy_url = item.xpath('./div/div[2]/div[1]/a/@href')[0]  # 电影链接
    #
    #     rating_num = item.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0]  # 电影分数（如9.0分）
    #
    #     writer.writerow((rank, name, dy_url, rating_num))  # 写入文件
    soup = BeautifulSoup(response, 'html.parser')
    movie_items = soup.find_all('div', class_='item')    # 找到所有电影条目所在的元素
    for item in movie_items:
        rank = item.find('em').get_text()  # 电影排名
        name = item.find('span', class_='title').get_text()   # 电影名字
        dy_url = item.find('a')['href']   # 电影链接
        rating_num = item.find('span', class_='rating_num').get_text()    # 电影评分
        writer.writerow((rank, name, dy_url, rating_num))    # 写入CSV文件

fp.close()
