import pandas as pd
import requests
from bs4 import BeautifulSoup

stats = []
for idx in range(38200, 55200):
    try:
        url = f'https://austinssc.leaguelab.com/league/{idx}/standings'
        response = requests.get(url, allow_redirects=False)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
        league_info = soup.find('h1', class_="leagueTitle")
        field_name = str.split(league_info.text, '(')[-1][0:-1]
        day_of_week = str.split(league_info.text, ' ')[0]
        sport = str.split(league_info.text, ' ')[1]
        if sport != 'Kickball':
            continue
        wlds = soup.find_all('td', class_="wld")
        points_allowed = soup.find_all('td', class_="lastColumn")
        total_points_allowed = 0
        num_teams = 0
        games_per_team = 0
        for wld in wlds[:3]:
            games_per_team += int(str.strip(wld.text))
        for pa in points_allowed:
            total_points_allowed += int(str.strip(pa.text))
            num_teams += 1

        stats.append({
            'field_name': field_name,
            'day_of_week': day_of_week,
            'sport': sport,
            'games_per_team': games_per_team,
            'num_teams': num_teams,
            'total_points_allowed': total_points_allowed,
            'url': url
        })

        pd.DataFrame(stats).to_csv('scraped_kickball_scores_url.csv', index=False)

    except Exception as e:
        print(e)

