import random


class GameManager:
    ''' Game class'''

    def __init__(self, colors):
        self.colors = colors
        self._code = []
        self.generate_code()

    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    def generate_code(self):
        """ Generate code on start """
        for i in range(4):
            self._code.append(random.choice(self.colors))

    def check_answer(answer, correct_code):
        score = ["blank", "blank", "blank", "blank"]
        total_guesses = 0
        color_guesses = 0
        not_total_guess_rows = []
        not_total_guess_rows2 = []
        for i in range(4):
            if correct_code[i] == answer[i]:
                total_guesses += 1
            else:
                not_total_guess_rows.append(correct_code[i])
                not_total_guess_rows2.append(i)
        for i in not_total_guess_rows2:
            if answer[i] in not_total_guess_rows:
                not_total_guess_rows.remove(answer[i])
                color_guesses += 1
        for i in range(total_guesses):
            score[i] = "black"
        for i in range(color_guesses):
            score[i + total_guesses] = "white"
        return score
