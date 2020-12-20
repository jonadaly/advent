import requests
import os
import time
import json
from datetime import datetime
from matplotlib import pyplot as plt

LEADER_BOARD_CODE = "91857"
LEADER_BOARD_URL = "https://adventofcode.com/2018/leaderboard/private/view/"
SESSION_COOKIE = '53616c7465645f5fd0ef0552afc7a20461143c377db6adf58c36ceef070dbc47f928a2738de414f874eb0baec4e7f348'

if not os.path.exists("leader_board_" + LEADER_BOARD_CODE + ".json") or os.path.getmtime(
        "leader_board_" + LEADER_BOARD_CODE + ".json") < (int(time.time()) - 60 * 30):
    jar = requests.cookies.RequestsCookieJar()
    jar.set('session', SESSION_COOKIE)
    response = requests.get(LEADER_BOARD_URL + LEADER_BOARD_CODE + ".json", cookies=jar)
    _json = response.json()
    with open("leader_board_" + LEADER_BOARD_CODE + ".json", "w") as fd:
        json.dump(_json, fd, indent=4, separators=(",", ": "), sort_keys=True)

with open("leader_board_" + LEADER_BOARD_CODE + ".json", "r") as fd:
    board = json.load(fd)
history = {}
for member_id, member_details in board["members"].items():
    for day, level_details in member_details["completion_day_level"].items():
        history[level_details['1']['get_star_ts']] = (member_details["name"], day, '1')
        if '2' in level_details:
            history[level_details['2']['get_star_ts']] = (member_details["name"], day, '2')
history = {key: history[key] for key in sorted(history)}

people = list(set([h[0] for h in history.values()]))
dayScores = {str(x): {str(z): [y for y in range(1, len(people) + 1)] for z in range(1, 3)} for x in range(1, 26)}
scores = {p: {
    "x": [0],
    "star_y": [0],
    "points_y": [0]
} for p in people}
for ts, event in history.items():
    event_date = datetime.fromtimestamp(int(ts))
    print(event_date.strftime("%Y-%b-%d %H:%M:%S") + " - " + event[0] + " completed Day " + event[1] + " part " + event[
        2])
    scores[event[0]]["x"].append((int(ts) - 1543622400)/(60*60*24))
    scores[event[0]]["star_y"].append(scores[event[0]]["star_y"][-1] + 1)
    scores[event[0]]["points_y"].append(
        scores[event[0]]["points_y"][-1] + (dayScores[event[1]][event[2]].pop() if event[1] != '6' else 0))

for p, s in scores.items():
    plt.plot(s["x"], s["points_y"], label=p)
plt.legend()
plt.show()