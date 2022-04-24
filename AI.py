import random
from game import GameManager


class AI:
    def __init__(self, colors):
        # store history of game to help decide next move based on past results
        self.answers_history = []
        self.scores_history = []
        self.colors = colors
        # create all possible answers
        self.possibilities = [[col1, col2, col3, col4]
                              for col1 in colors
                              for col2 in colors
                              for col3 in colors
                              for col4 in colors]
        # shuffle possibilities to check more colors in the first move
        random.shuffle(self.possibilities)

    def get_possibilities(self):
        return self.possibilities

    def decide_answer(self):
        ''' Decide answer based on previous answers and scores '''
        answer = ["blank", "blank", "blank", "blank"]
        if (len(self.answers_history) == 0):  # if this is the first move
            answer = self.random_answer()
            self.answers_history.append(answer)
            return answer
        new_possibilities = self.possibilities[:]
        # check all combinations that are possible
        for combination in self.possibilities:
            passed = True
            row = 0
            for prev_answer in self.answers_history:
                # check if combinations is relatively to another answer and score
                can_be_solution = self.check_if_can_be_solution(
                    prev_answer, self.scores_history[row], combination)
                if (can_be_solution == False):
                    passed = False
                    # remove invalid possibility
                    new_possibilities.remove(combination)
                    break
                row += 1
            if passed:  # if combination is possible after analizing all answer history
                answer = combination
                break
        self.possibilities = new_possibilities[:]
        self.answers_history.append(answer)
        return answer

    def clear_history(self):
        """ remember answer to help AI find the best possible solution """
        self.answers_history = []
        self.possibilities = [[col1, col2, col3, col4]
                              for col1 in self.colors
                              for col2 in self.colors
                              for col3 in self.colors
                              for col4 in self.colors]

    def store_score(self, score):
        # store score to scores_history
        self.scores_history.append(score)

    def store_answer(self, answer):
        # store answer to answers_history
        self.answers_history.append(answer)

    def check_if_can_be_solution(self, combination, score, answer):
        # check if the answer is possible based on other answer and score
        temp_score = GameManager.check_answer(answer, combination)
        if (temp_score.count("black") == score.count("black")):
            if (temp_score.count("white") == score.count("white")):
                return True
        return False

    def random_answer(self):
        # 4 random colors
        answer = []
        for i in range(4):
            answer.append(random.choice(self.colors))
        return answer
