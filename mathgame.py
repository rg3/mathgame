#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 Ricardo Garcia <r@rg3.name>
# SPDX-License-Identifier: MIT

import os
import random
import sys

class ScreenClearer(object):
    def __init__(self):
        self.cmd = 'cls' if os.name == 'nt' else 'clear'

    def clear(self):
        os.system(self.cmd)

class Operation(object):
    def valid (self, a, b):
        return True

    def result(self, a, b):
        raise TypeError

    def symbol(self):
        raise TypeError

class Addition(Operation):
    def __init__(self):
        pass

    def result(self, a, b):
        return a+b

    def symbol(self):
        return "+"

class Multiplication(Operation):
    def __init__(self):
        pass

    def result(self, a, b):
        return a*b

    def symbol(self):
        return "*"

class Substraction(Operation):
    def __init__(self):
        pass

    def valid(self, a, b):
        return a >= b

    def result(self, a, b):
        return a-b

    def symbol(self):
        return "-"

class TableGenerator(object):
    def __init__(self, used_operation):
        self.usedOperation = used_operation

    def table(self, a):
        result = []
        for i in range(1,10+1):
            if self.usedOperation.valid(a, i):
                result.append((a, i))
        return result

class Game(object):
    def __init__(self, table_generator, used_operation, combiner_list):
        self.tableGenerator = table_generator
        self.usedOperation = used_operation
        self.combinations = []
        for i in combiner_list:
            self.combinations.extend(self.tableGenerator.table(i))
        self.quitAnswer = "q"
        self.rightAnswers = 0
        self.wrongAnswers = 0
        self.CORRECT_SIGN = "\u2713 Yes!"
        self.INCORRECT_SIGN = "\u2717 No"
        self.currentSign = "Welcome! To quit the game, answer '%s' to any question" % (self.quitAnswer,)

    def run(self):
        questions = []
        clearer = ScreenClearer()
        continue_playing = True
        while continue_playing:
            if len(questions) == 0:
                questions = self.combinations[:]
                random.shuffle(questions)

            next_idx = random.choice(range(0, len(questions)))
            question = questions[next_idx]
            del questions[next_idx]

            # Repeat the question until it's right or we have to stop playing.
            while True:
                clearer.clear()
                print('%s' % self.currentSign)
                print('%s' % self.stats())
                result = self.ask(question)
                if result is None:
                    continue_playing = False
                    break
                elif result:
                    break

    def stats(self):
        total = self.rightAnswers + self.wrongAnswers
        percent_good = 0.0 if total == 0 else (float(self.rightAnswers) / float(total) * 100.0)
        percent_bad  = 0.0 if total == 0 else (100.0 - percent_good)
        good_sign = 'Right: %10d (%.1f%%)' % (self.rightAnswers, percent_good)
        bad_sign  = 'Wrong: %10d (%.1f%%)' % (self.wrongAnswers, percent_bad)
        return '%s\n%s' % (good_sign, bad_sign)

    # Returns True if the answer was right, False if not, None if we need to quit the game.
    def ask(self, question):
        a, b = question
        correct_answer = self.usedOperation.result(a, b)
        while True:
            answer = input("%s %s %s = " % (a, self.usedOperation.symbol(), b))
            if answer.lower() == self.quitAnswer:
                return None
            try:
                numerical_answer = int(answer)
                is_right = (numerical_answer == correct_answer)
                if is_right:
                    self.currentSign = self.CORRECT_SIGN
                    self.rightAnswers += 1
                else:
                    self.currentSign = self.INCORRECT_SIGN
                    self.wrongAnswers += 1
                return is_right
            except ValueError:
                pass

if __name__ == "__main__":
    def usage():
        sys.exit("Usage: %s add|sub|mul NUMBER_FROM_1_TO_10..." % (sys.argv[0], ))

    arg_count = len(sys.argv)
    if arg_count < 3:
        usage()

    operation_arg = sys.argv[1]

    operation_classes = dict()
    operation_classes['add'] = Addition
    operation_classes['sub'] = Substraction
    operation_classes['mul'] = Multiplication

    if operation_arg not in operation_classes:
        usage()
    used_operation = operation_classes[operation_arg]()
    table_generator = TableGenerator(used_operation)

    def parse_numeric_arg (arg_str):
        try:
            parsed_value = int(arg_str)
            if parsed_value < 1 or parsed_value > 10:
                raise ValueError
            return parsed_value
        except ValueError:
            usage()

    values = []
    for numeric_arg in sys.argv[2:]:
        values.append(parse_numeric_arg(numeric_arg))
    values = sorted(list(set(values))) # Remove duplicates.

    game = Game(table_generator, used_operation, values)
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n")
