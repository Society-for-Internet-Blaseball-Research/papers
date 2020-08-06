# MIT License
# Copyright (c) 2020 iliana etaoin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv
import gzip
import json
import sys

GAMES = {}
STARTED = []

COMPLETED = []
NEW_RULES_COMPLETED = []

SHAMED = []
NEW_RULES_SHAMED = []

END = {}
NEW_RULES_END = {}


def is_game_over(away, home, inning, top):
    if inning >= 8:
        if top and home > away:
            return True
        if not top and home != away:
            return True
    return False


def is_shame(away, home, inning, top):
    return inning >= 8 and not top and home > away


def process_game_event(game):
    if game["gameComplete"] and game["_id"] in STARTED and game["_id"] not in COMPLETED:
        # print(GAMES[game["_id"]]["last"])
        # print(game)
        # print(f"failed assumption -- we thought {game['_id']} didn't end!")
        # sys.exit(0)
        for list in [COMPLETED, SHAMED, NEW_RULES_SHAMED]:
            if game["_id"] in list:
                list.remove(game["_id"])
    if (
        game["_id"] in COMPLETED
        and not game["gameComplete"]
        and GAMES[game["_id"]]["last"] != game
    ):
        print(GAMES[game["_id"]]["last"])
        print(game)
        print(f"failed assumption -- we thought {game['_id']} ended early!")
        sys.exit(0)

    if game["gameComplete"] or not game["gameStart"]:
        return

    entry = GAMES.get(game["_id"])
    if entry is None:
        if game["lastUpdate"] == "Play ball!":
            STARTED.append(game["_id"])
            GAMES[game["_id"]] = {
                "awaySteals": 0,
                "homeSteals": 0,
                "last": None,
            }
        return

    if game != entry["last"]:
        if any(
            game["lastUpdate"].endswith(x)
            for x in ["steals second base!", "steals third base!", "steals home!"]
        ):
            if game["topOfInning"]:
                entry["awaySteals"] += 1
            else:
                entry["homeSteals"] += 1

    # detect end of half inning if halfInningOuts resets
    if entry["last"] and game["halfInningOuts"] < entry["last"]["halfInningOuts"]:
        if is_game_over(
            game["awayScore"],
            game["homeScore"],
            entry["last"]["inning"],
            entry["last"]["topOfInning"],
        ):
            COMPLETED.append(game["_id"])
            END[game["_id"]] = (
                game["awayScore"],
                game["homeScore"],
                entry["last"]["inning"],
                entry["last"]["topOfInning"],
            )
            if is_shame(
                game["awayScore"],
                game["homeScore"],
                entry["last"]["inning"],
                entry["last"]["topOfInning"],
            ):
                assert game["shame"]
                SHAMED.append(game["_id"])
            else:
                assert not game["shame"]

        if (
            is_game_over(
                game["awayScore"] + (entry["awaySteals"] * 0.1),
                game["homeScore"] + (entry["homeSteals"] * 0.1),
                entry["last"]["inning"],
                entry["last"]["topOfInning"],
            )
            and game["_id"] not in NEW_RULES_COMPLETED
        ):
            NEW_RULES_COMPLETED.append(game["_id"])
            NEW_RULES_END[game["_id"]] = (
                game["awayScore"] + (entry["awaySteals"] * 0.1),
                game["homeScore"] + (entry["homeSteals"] * 0.1),
                entry["last"]["inning"],
                entry["last"]["topOfInning"],
            )
            if is_shame(
                game["awayScore"] + (entry["awaySteals"] * 0.1),
                game["homeScore"] + (entry["homeSteals"] * 0.1),
                entry["last"]["inning"],
                entry["last"]["topOfInning"],
            ):
                NEW_RULES_SHAMED.append(game["_id"])

    # ok all done
    GAMES[game["_id"]]["last"] = game


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        with gzip.open(filename) as f:
            for line in f:
                schedule = json.loads(line)["schedule"]
                for game in schedule:
                    process_game_event(game)
    print(f"games tabulated: {len(COMPLETED)}")
    print(f"games with shame (original rules): {len(SHAMED)}")
    print(f"games with shame (blaserunning rules): {len(NEW_RULES_SHAMED)}")

    report = []

    i = 0
    for id in SHAMED:
        if id not in NEW_RULES_SHAMED:
            i += 1
            report.append(id)
    print(f"games going from shame to not shame: {i}")

    i = 0
    for id in NEW_RULES_SHAMED:
        if id not in SHAMED:
            i += 1
            report.append(id)
    print(f"games going from not shame to shame: {i}")

    def top_word(top):
        return "Top" if top else "Bot"

    rows = []
    for id in report:
        entry = GAMES[id]
        last = entry["last"]
        (away, home, inning, top) = END[id]
        (away_new, home_new, inning_new, top_new) = NEW_RULES_END[id]
        rows.append(
            {
                "Season": last["season"] + 1,
                "Day": last["day"] + 1,
                "Away": last["awayTeamNickname"],
                "Home": last["homeTeamNickname"],
                "Inning Orig": f"{top_word(top)} {inning + 1}",
                "Away Orig": float(away),
                "Home Orig": float(home),
                "Shame Orig": is_shame(away, home, inning, top),
                "Inning New": f"{top_word(top_new)} {inning_new + 1}",
                "Away New": away_new,
                "Home New": home_new,
                "Shame New": is_shame(away_new, home_new, inning_new, top_new),
                "Result Flipped": (
                    (away > home and away_new < home_new)
                    or (away < home and away_new > home_new)
                ),
            }
        )

    rows = sorted(rows, key=lambda row: row["Day"])
    rows = sorted(rows, key=lambda row: row["Season"])

    writer = csv.DictWriter(sys.stdout, rows[0].keys())
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
