from pprint import pprint
import random
import math
import sys


TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value: dict) -> dict:
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game() -> list:
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()
pprint(game_stamps)


def get_score(game_stamps: list, offset: int) -> tuple:
    '''
        Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
        Please pay attention to that for some offsets the game_stamps list may not contain scores.
    '''
    # simple binary search without recursion
    def search_offset(game_stamps: list, offset: int, start: int, end: int) -> int | None:
        mid = len(game_stamps)//2
        end = end - 1
        while game_stamps[mid]["offset"] != offset and start <= end:
            if offset > game_stamps[mid]["offset"]:
                start = mid + 1
            else:
                end = mid - 1
            mid = (start + end) // 2
        if start > end:
            return None
        else:
            return mid
    # Checking that all parameters take satisfactory values
    if isinstance(game_stamps, list) and isinstance(offset, int) and game_stamps:
        index_state = search_offset(game_stamps, offset, 0, len(game_stamps))
        if index_state != None:
            home, away = game_stamps[index_state]['score']['home'], game_stamps[index_state]['score']['away']
            return home, away
        else:
            return None
    elif not isinstance(game_stamps, list) or not game_stamps:
        raise ValueError("Game_stamps is not a list, or list is empty")
    elif not isinstance(offset, int):
        raise ValueError("offset not int")


