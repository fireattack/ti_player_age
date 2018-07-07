import re
import requests
from bs4 import BeautifulSoup

url = 'https://liquipedia.net/dota2/The_International/2018'

html = requests.get(url)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, "lxml")
divs = soup.find_all('div', class_='teamcard')

for div in divs:
    center = div.find('center')
    teamname = re.search(r'title="(.+?)"', str(center))[1]
    print(teamname)
    for tr in div.find_all('tr'):      
        string = re.search(r'<th>([12345])</th><td><a.+</a>.+<a.+href="(.+)".+?title="(.+?)"', str(tr))
        if string is not None:
            pos = string[1]
            name = string[3]
            url2 = 'https://liquipedia.net' + string[2]
            html2 = requests.get(url2)
            html2.encoding = 'utf-8'
            bd = BeautifulSoup(html2.text, "lxml").find('span', class_='bday')
            if bd is not None:
                bday = innerHTML = "".join([str(x) for x in bd.contents])
            else:
                bday = 'N/A'
            record = teamname + ',' + pos + ',' + name + ',' + bday
            print(record)
            with open("output_2018.csv", "a", encoding='utf-8-sig') as f:
                f.write(record + '\n')