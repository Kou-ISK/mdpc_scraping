import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json


def parse_data():
    game_datas = []
    for data in datas:
        division = data[1]
        card = data[2]
        result = data[6]
        memo = data[7]

        print(result)

        if not result or result.strip() == "":
            break
        else:
            teams = parse_card_to_teams(card)
            scores = parse_result_to_scores(result)

            if len(scores) < 2:  # スコアの解析に失敗した場合
                print(f"Invalid score format for game {card}")
                continue

            team1, team2 = teams[0], teams[1]
            score1, score2 = int(scores[0]), int(scores[1])

            # 勝敗をカウント
            if score1 > score2:
                division_team_wins[division][team1] += 1
            elif score2 > score1:
                division_team_wins[division][team2] += 1

            # 得失点差を更新
            division_team_goal_difference[division][team1] += (score1 - score2)
            division_team_goal_difference[division][team2] += (score2 - score1)

            print({
                "div": division, "team1": team1, "team2": team2,
                "score1": score1, "score2": score2
            })
            game_data = {
                "div": division, "team1": team1, "team2": team2,
                "score1": score1, "score2": score2
            }
            game_datas.append(game_data)
    return game_datas


def parse_card_to_teams(card):
    print("=============")
    card.strip()
    teams = card.split(" vs ")
    for team in teams:
        team.strip()
    return teams


def parse_result_to_scores(result):
    scores = []
    result.strip()
    if "-" in result:
        scores = result.split("-")
    if "ー" in result:
        scores = result.split("ー")
    return scores


def determine_champion():
    champions = {}
    for division, teams in division_team_wins.items():
        # 勝利数の多い順にチームをソート
        sorted_teams = sorted(teams.items(), key=lambda item: (
            item[1], division_team_goal_difference[division][item[0]]), reverse=True)
        champion_team = sorted_teams[0][0]
        champions[division] = champion_team
        print(f"Division{division}")
        print(f"Champion: {champion_team} with {sorted_teams[0][1]} wins")
    return champions


COMPETETION_NUM = 72
URL = f"http://www.mdpc.jp/game/league{COMPETETION_NUM}/schedule.html"

res = requests.get(url=URL)
res.encoding = "utf-8"
html = res.text

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")
rows = table.find_all("tr")


# 勝敗カウントを保持するための辞書
division_team_wins = defaultdict(lambda: defaultdict(int))
# 得失点差を保持するための辞書
division_team_goal_difference = defaultdict(lambda: defaultdict(int))

datas = []
for row in rows:
    data = []
    for cell in row.findAll(['td', 'th']):
        data.append(cell.get_text())
    datas.append(data)
datas.pop(0)
game_datas = parse_data()

# JSON形式でファイルに出力
output_file = "../fe/src/game_datas_output.json"  # 出力先のファイル名を指定
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(game_datas, f, ensure_ascii=False)

print(f"データが {output_file} に保存されました。")

# 優勝チームを判定
champions = determine_champion()
