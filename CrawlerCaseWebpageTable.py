import requests  
from bs4 import BeautifulSoup  
import csv  
import os


def get_player_data(url, class_name):
    response = requests.get(url)  
    html = response.content
    soup = BeautifulSoup(html, "html.parser")  
    table = soup.find('table', attrs={"class": class_name})  

    player_data_list = []
    for row in table.find_all("tr"):  
        cols = row.find_all('td')  
        if cols:  
            player_rank = cols[22].find('span').text.replace(" ", "") if cols[22].find('span') else ""
            player_name = cols[1].find('a').text if cols[1].find('a') else ""
            player_country = cols[1].find('i')['class'][-1] if cols[1].find('i') else ""

            player_data_list.append({
                '玩家': player_name,
                '国家（地区）': player_country,
                '天梯分': player_rank
            })

    return player_data_list


def write_player_data_to_csv(player_data_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:  
        writer = csv.writer(csvfile)  
        writer.writerow(['玩家', '国家（地区）', '天梯分'])  

        for player_data in player_data_list:
            writer.writerow([player_data['玩家'], player_data['国家（地区）'], player_data['天梯分']])


if __name__ == '__main__':
    curr_path = os.getcwd()
    print(curr_path)

    url = "https://arena.5eplay.com/data"
    class_name = "odd-even data-rank"

    player_data_list = get_player_data(url, class_name)
    print(player_data_list)

    write_player_data_to_csv(player_data_list, 'player_data.csv')
