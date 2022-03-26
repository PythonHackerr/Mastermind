import random


class MastermindGame:
    ''' Game class'''

    def __init__(self, colors):
        self.answers_history = []
        self.possibilities = [[col1, col2, col3, col4]
                              for col1 in colors
                              for col2 in colors
                              for col3 in colors
                              for col4 in colors]
        self.colors = colors
        self._code = ["red", "white", "red", "blank"]
        # self.generate_code()

    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code
        print(self._code)

    def generate_code(self):
        """ Generate code on start """
        for i in range(4):
            self._code.append(random.choice(self.colors))
        print(self._code)

    def update_possibilities(self):
        """ Reduce number of possibilities that remain """
        remaining_possibles = []
        for possibily in self.possibilities:
            if self.can_be_solution(possibily):
                remaining_possibles.append(possibily)
        self.possibilities = remaining_possibles

    def possibilities_remain(self):
        """ number of remaining possibilities """
        return len(self.possibilities)

    def store_answer(self, answer):
        """ remember answer to help AI find the best possible solution """
        self.answers_history.append(answer)
        self.update_possibilities()

    def clear_history(self):
        """ remember answer to help AI find the best possible solution """
        self.answers_history = []
        self.possibilities = [[col1, col2, col3, col4]
                              for col1 in self.colors
                              for col2 in self.colors
                              for col3 in self.colors
                              for col4 in self.colors]

    def can_be_solution(self, answer):
        """ Check if answer is valid depending on last actions """
        for i in range(len(self.answers_history)):
            if not(self.white_scores(self.answers_history[i], answer) == self.white_scores(self.answers_history[i], self.get_code()) and
                    self.black_scores(self.answers_history[i], answer) == self.black_scores(self.answers_history[i], self.get_code())):
                return False
        return True

    def black_scores(self, answer, code):
        """ Return number of black answers (color is guesses!)"""
        num = 0
        for i in range(4):
            if answer[i] == code[i]:
                num += 1
        return num

    def white_scores(self, answer, code):
        """ Return number of white answers (color is in code)"""
        code2 = code[:]  # new variable to not change original code
        num = 0
        for color in answer:
            if color in code2:
                num += 1
                code2.pop(code2.index(color))
        return num

    def check_answer(self, answer, correct_code):
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
        self.store_answer(answer)
        return score
