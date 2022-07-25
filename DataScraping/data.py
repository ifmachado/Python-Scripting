import requests
from bs4 import BeautifulSoup
import sqlite3


# #ghibli url
# url = 'https://ghibliapi.herokuapp.com/films'
# #get page
# data = requests.get(url)
# #parse it into json
# parsed_data = data.json()
#
# for data in parsed_data:
#     print(data["title"])
#     print(data["description"])


#OTGW episodes url
url ='https://steven-universe.fandom.com/wiki/Episode_Guide#Season_1'
#get page
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

episodes = []  # a list to store episodes

div = soup.find(id ='mw-content-text')
tables = div.findChildren('table')
for table in tables:
    row = table.findChildren('tr')[0]
    if len(row.findChildren('td')) > 2:
        cell = row.findChildren('td')[3]
        for lines in cell.findChildren('a'):
            if lines.has_attr('title'):
                title = lines['title']
                episodes.append(title)

for title in episodes:
    print(title)

