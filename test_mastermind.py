from game import GameManager
from AI import AI

PLAYER_COLORS = ["red", "yellow", "green", "blue",
                 "black", "white", "blank"]
GAME = GameManager(PLAYER_COLORS)
GAME_AI = AI(PLAYER_COLORS)

''' Score system testing '''


def test_score_different_colors():
    code = ["blue", "purple", "blank", "black"]

    answer = ["black", "white", "red", "yellow"]
    score = GameManager.check_answer(answer, code)
    assert score.count("white") == 1
    assert score.count("black") == 0

    answer = ["blank", "purple", "white", "blue"]
    score = GameManager.check_answer(answer, code)
    assert score.count("white") == 2
    assert score.count("black") == 1


def test_score_dublicates_less():
    code = ["red", "red", "yellow", "red"]

    answer = ["red", "white", "red", "yellow"]
    score = GameManager.check_answer(answer, code)
    assert score.count("white") == 2
    assert score.count("black") == 1

    answer = ["red", "yellow", "white", "yellow"]
    score = GameManager.check_answer(answer, code)
    assert score.count("white") == 1
    assert score.count("black") == 1


def test_score_dublicates_more():
    code = ["purple", "red", "yellow", "red"]

    answer = ["red", "red", "red", "yellow"]
    score = GameManager.check_answer(answer, code)
    assert score.count("white") == 2
    assert score.count("black") == 1

    answer = ["purple", "red", "red", "red"]
    score = GameManager.check_answer(answer, code)
    assert score.count("white") == 0
    assert score.count("black") == 3


''' AI desision testing '''


def test_can_be_solution():
    code = ["purple", "red", "yellow", "red"]
    GAME.set_code(code)
    answer1 = ["blue", "blank", "green", "black"]  # no such colors
    answer2 = ["red", "red", "red", "red"]  # deffinetly 2 red colors
    answer3 = ["red", "yellow", "red", "yellow"]  # 1 yellow, but not there
    score1 = GameManager.check_answer(answer1, code)  # 0b, 0w
    score2 = GameManager.check_answer(answer2, code)  # 2b, 0w
    score3 = GameManager.check_answer(answer3, code)  # 2b, 1w

    current_answer1 = ["white", "red", "yellow", "red"]
    current_answer2 = ["purple", "red", "yellow", "red"]

    GAME_AI.store_answer(answer1)
    GAME_AI.store_answer(answer2)
    GAME_AI.store_answer(answer3)

    GAME_AI.store_score(score1)
    GAME_AI.store_score(score2)
    GAME_AI.store_score(score3)

    assert GAME_AI.check_if_can_be_solution(
        answer1, score1, current_answer1) == True
    assert GAME_AI.check_if_can_be_solution(
        answer2, score2, current_answer1) == True
    assert GAME_AI.check_if_can_be_solution(
        answer3, score3, current_answer1) == True
    assert GAME_AI.check_if_can_be_solution(
        answer1, score1, current_answer2) == True
    assert GAME_AI.check_if_can_be_solution(
        answer2, score2, current_answer2) == True
    assert GAME_AI.check_if_can_be_solution(
        answer3, score3, current_answer2) == True


def test_cannot_be_solution():
    code = ["purple", "red", "yellow", "red"]
    GAME.set_code(code)
    answer1 = ["blue", "blank", "green", "black"]  # no such colors
    answer2 = ["red", "red", "red", "red"]  # deffinetly 2 red colors
    answer3 = ["red", "yellow", "red", "yellow"]  # 1 yellow, but not there
    score1 = GameManager.check_answer(answer1, code)  # 0b, 0w
    score2 = GameManager.check_answer(answer2, code)  # 2b, 0w
    score3 = GameManager.check_answer(answer3, code)  # 0b, 3w

    # No for 1, because there is no blue!
    # No for 2, because must be 2 red!
    # No for 3, because yellow is in wrong place!
    current_answer1 = ["blue", "blank", "blank", "yellow"]
    # Yes for 1
    # Yes for 2
    # No for 3, because this is the same colors, but score says that there are only 3 jf them
    current_answer2 = ["yellow", "red", "yellow", "red"]
    # Yes for 1
    # Yes for 2
    # No for 3, because yellow is in wrong place!
    current_answer3 = ["red", "yellow", "red", "purple"]

    GAME_AI.store_answer(answer1)
    GAME_AI.store_answer(answer2)
    GAME_AI.store_answer(answer3)

    GAME_AI.store_score(score1)
    GAME_AI.store_score(score2)
    GAME_AI.store_score(score3)

    assert GAME_AI.check_if_can_be_solution(
        answer1, score1, current_answer1) == False
    assert GAME_AI.check_if_can_be_solution(
        answer2, score2, current_answer1) == False
    assert GAME_AI.check_if_can_be_solution(
        answer3, score3, current_answer1) == False
    assert GAME_AI.check_if_can_be_solution(
        answer1, score1, current_answer2) == True
    assert GAME_AI.check_if_can_be_solution(
        answer2, score2, current_answer2) == True
    assert GAME_AI.check_if_can_be_solution(
        answer3, score3, current_answer2) == False
    assert GAME_AI.check_if_can_be_solution(
        answer1, score1, current_answer3) == True
    assert GAME_AI.check_if_can_be_solution(
        answer2, score2, current_answer3) == True
    assert GAME_AI.check_if_can_be_solution(
        answer3, score3, current_answer3) == False
