import pandas as pd
import requests
from bs4 import BeautifulSoup

stats = []
valid_league_ids = [41652, 41653, 41751, 42206, 42207, 42230, 42231, 42232, 42288, 42731,
                    42732, 42734, 42735, 43448, 43456, 43693, 43695, 43968, 44388, 44389,
                    44390, 44391, 44524, 44525, 44526, 44778]

for idx in valid_league_ids:
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
        total_games = 0
        for wld in wlds:
            total_games += int(str.split(str.strip(wld.text), ' ')[0])
        total_games = total_games/2
        for pa in points_allowed:
            total_points_allowed += int(str.strip(pa.text))
            num_teams += 1

        stats.append({
            'field_name': field_name,
            'day_of_week': day_of_week,
            'sport': sport,
            'total_games': total_games,
            'num_teams': num_teams,
            'total_points_allowed': total_points_allowed,
            'url': url
        })

        pd.DataFrame(stats).to_csv('scraped_kickball_scores_tot_games.csv', index=False)

    except Exception as e:
        print(e)

