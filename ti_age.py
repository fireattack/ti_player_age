import re
import requests
from bs4 import BeautifulSoup




YEAR = 2023
def getPageFromAPI(pageName):

    # See: https://liquipedia.net/api-terms-of-use
    # time.sleep(2)
    headers = {'User-Agent': 'ti_age project', 'Accept-Encoding': 'gzip'}

    if pageName.startswith('/dota2/'):
        pageName = pageName[7:]
    pageName = pageName.replace('&amp;', '%26')
    url = f'https://liquipedia.net/dota2/api.php?action=query&prop=revisions&titles={pageName}&rvprop=content&rvparse&format=json'
    print('Getting ' + url)
    r = requests.get(url, headers=headers)
    json = r.json()
    html = list(json['query']['pages'].values())[0]["revisions"][0]['*']
    if 'redirectMsg' in html:
        pageNameNew = re.search(r'title="(.+?)"', html)
        return getPageFromAPI(pageNameNew[1])
    else:
        return BeautifulSoup(html, 'lxml')

divs = getPageFromAPI(f'The_International/{YEAR}').find_all('div', class_='teamcard')

# print all team names.
team_names = [div.select_one('center').text for div in divs]
print(f'Find {len(team_names)} teams: {", ".join(team_names)}')

for div in divs:
    team_name = div.select_one('center').text
    print('Processing ' + team_name)
    for tr in div.find_all('tr'):
        if m := re.search(r'<th>([12345])</th><td>.+<a.+</a>.+<a.+href="(.+)".+?title="(.+?)"', str(tr)):
            pos = m[1]
            name = m[3]
            bd = getPageFromAPI(m[2]).find('div', string='Born:')
            if bd:
                bday = bd.parent.find_all('div')[-1].text
            else:
                bday = 'N/A'

            record = team_name + ',' + pos + ',' + name + ',' + bday
            print(record)
            with open(f"output_{YEAR}.csv", "a", encoding='utf-8-sig') as f:
                f.write(record + '\n')
        else:
            # Not for a player. Ignore.
            pass