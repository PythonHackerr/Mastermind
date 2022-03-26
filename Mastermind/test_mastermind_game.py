from mastermind import MastermindGame

PLAYER_COLORS = ["red", "yellow", "green", "blue",
                 "black", "white", "blank"]
GAME = MastermindGame(PLAYER_COLORS)


''' Score system testing '''


def test_score_different_colors():
    code = ["blue", "purple", "blank", "black"]
    GAME.set_code(code)

    answer = ["black", "white", "red", "yellow"]
    score = GAME.check_answer(answer, code)
    assert score.count("white") == 1
    assert score.count("black") == 0

    answer = ["blank", "purple", "white", "blue"]
    score = GAME.check_answer(answer, code)
    assert score.count("white") == 2
    assert score.count("black") == 1


def test_score_dublicates_less():
    code = ["red", "red", "yellow", "red"]
    GAME.set_code(code)

    answer = ["red", "white", "red", "yellow"]
    score = GAME.check_answer(answer, code)
    assert score.count("white") == 2
    assert score.count("black") == 1

    answer = ["red", "yellow", "white", "yellow"]
    score = GAME.check_answer(answer, code)
    assert score.count("white") == 1
    assert score.count("black") == 1


def test_score_dublicates_more():
    code = ["purple", "red", "yellow", "red"]
    GAME.set_code(code)

    answer = ["red", "red", "red", "yellow"]
    score = GAME.check_answer(answer, code)
    assert score.count("white") == 2
    assert score.count("black") == 1

    answer = ["purple", "red", "red", "red"]
    score = GAME.check_answer(answer, code)
    assert score.count("white") == 0
    assert score.count("black") == 3


''' AI scoring system testing '''


def test_calculate_score_blacks():
    code = ["green", "white", "purple", "white"]
    GAME.set_code(code)

    answer1 = ["white", "white", "white", "red"]
    answer2 = ["purple", "blank", "white", "green"]

    assert GAME.black_scores(answer1, GAME.get_code()) == 1
    assert GAME.black_scores(answer2, GAME.get_code()) == 0


def test_calculate_score_whites():
    code = ["green", "white", "purple", "white"]
    GAME.set_code(code)

    answer1 = ["white", "white", "white", "red"]
    answer2 = ["purple", "red", "yellow", "red"]

    assert GAME.white_scores(answer1, GAME.get_code()) == 2
    assert GAME.white_scores(answer2, GAME.get_code()) == 1


def test_can_be_solution():
    code = ["purple", "red", "yellow", "red"]
    GAME.set_code(code)
    answer1 = ["blue", "blank", "green", "black"]  # no such colors
    answer2 = ["red", "red", "red", "red"]  # deffinetly 2 red colors
    answer3 = ["red", "yellow", "red", "yellow"]  # 1 yellow, but not there

    # YES!
    current_answer1 = ["white", "red", "yellow", "red"]
    # Deffinetly YES!
    current_answer2 = ["purple", "red", "yellow", "red"]

    GAME.store_answer(answer1)
    GAME.store_answer(answer2)
    GAME.store_answer(answer3)

    assert GAME.can_be_solution(current_answer1) == True
    assert GAME.can_be_solution(current_answer2) == True


def test_cannot_be_solution():
    code = ["purple", "red", "yellow", "red"]
    GAME.set_code(code)
    answer1 = ["blue", "blank", "green", "black"]  # no such colors
    answer2 = ["red", "red", "red", "red"]  # deffinetly 2 red colors
    answer3 = ["red", "yellow", "red", "yellow"]  # 1 yellow, but not there

    # NO! Must be no blanks and 2 reds
    current_answer1 = ["red", "blank", "yellow", "blank"]
    # NO! Must be yellow
    current_answer2 = ["red", "red", "purple", "purple"]
    # NO! There are no score "black" in last answer, so yellow can't be there again
    current_answer3 = ["red", "yellow", "red", "purple"]

    GAME.store_answer(answer1)
    GAME.store_answer(answer2)
    GAME.store_answer(answer3)

    assert GAME.can_be_solution(current_answer1) == False
    assert GAME.can_be_solution(current_answer2) == False
    assert GAME.can_be_solution(current_answer3) == False


# Everything else l tested via pygame display window, because
# it is realy more efficient and faster. Please understand :)
