import re
import requests
from bs4 import BeautifulSoup

def getPageFromAPI(pageName):
    if pageName.startswith('/dota2/'):
        pageName = pageName[7:]
    url = f'https://liquipedia.net/dota2/api.php?action=query&prop=revisions&titles={pageName}&rvprop=content&rvparse&format=json'
    r = requests.get(url)
    json = r.json()
    html = list(json['query']['pages'].values())[0]["revisions"][0]['*']
    if 'redirectMsg' in html:
        pageNameNew = re.search(r'title="(.+?)"', html)
        return getPageFromAPI(pageNameNew[1])
    else:
        return BeautifulSoup(html, 'lxml')

divs = getPageFromAPI('The_International/2018').find_all('div', class_='teamcard')

for div in divs:
    center = div.find('center')
    teamname = re.search(r'title="(.+?)"', str(center))[1]
    print(teamname)
    for tr in div.find_all('tr'):
        string = re.search(
            r'<th>([12345])</th><td><a.+</a>.+<a.+href="(.+)".+?title="(.+?)"', str(tr))
        if string is not None:
            pos = string[1]
            name = string[3]
            bd = getPageFromAPI(string[2]).find('span', class_='bday')
            if bd is not None:
                bday = innerHTML = "".join([str(x) for x in bd.contents])
            else:
                bday = 'N/A'
            record = teamname + ',' + pos + ',' + name + ',' + bday
            print(record)
            with open("output_2018.csv", "a", encoding='utf-8-sig') as f:
                f.write(record + '\n')