import asyncio
import time

import aiohttp
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}


async def async_craw(url, csv_writer):
    print("craw url:", url)
    async with aiohttp.ClientSession() as session:  # 使用aiohttp创建异步http客户端会话
        async with session.get(url, headers=headers) as response:  # 使用session对象发送get请求，获取请求结果
            result = await response.text()  # 异步等待返回请求结果
            soup = BeautifulSoup(result, 'html.parser')  # 解析html字符串
            movie_items = soup.find_all('div', class_='item')  # 找到所有电影条目所在的元素
            for item in movie_items:
                rank = item.find('em').get_text()  # 电影排名
                name = item.find('span', class_='title').get_text()  # 电影名字
                dy_url = item.find('a')['href']  # 电影链接
                rating_num = item.find('span', class_='rating_num').get_text()  # 电影评分
                csv_writer.writerow((rank, name, dy_url, rating_num))  # 写入CSV文件


def run1():
    """
    异步IO    优点，实时写入；缺点，排序会乱
    :return: None
    """
    fp = open("./豆瓣top100.csv", 'w', encoding='utf8', newline='')
    writer = csv.writer(fp)
    writer.writerow(('排名', '名称', '链接', '评分'))

    urls = [('https://movie.douban.com/top250?start=%s&filter=' % page) for page in range(0, 100, 25)]
    loop = asyncio.get_event_loop()  # 获取当前事件循环
    tasks = [loop.create_task(async_craw(url, writer)) for url in urls]  # 创建任务列表，调用async_craw获取爬取结果
    start = time.time()
    loop.run_until_complete(asyncio.wait(tasks))  # 运行事件循环，等待所有任务完成。 asyncio.wait等待所有任务完成
    end = time.time()
    print("run time:", end - start)
    fp.close()


if __name__ == '__main__':
    run1()
