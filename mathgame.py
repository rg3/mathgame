#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021 Ricardo Garcia <r@rg3.name>
# SPDX-License-Identifier: MIT

import random
import sys

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
    def __init__(self, table_generator, used_operation, combiner_min, combiner_max):
        self.tableGenerator = table_generator
        self.usedOperation = used_operation
        self.combinations = []
        for i in range(combiner_min, combiner_max+1):
            self.combinations.extend(self.tableGenerator.table(i))
        self.quitAnswer = "q"
        self.rightAnswers = 0
        self.wrongAnswers = 0

    def run(self):
        print("Welcome! To quit the game, answer '%s' to any question" % (self.quitAnswer,))
        questions = []
        while True:
            if len(questions) == 0:
                questions = self.combinations[:]
                random.shuffle(questions)

            next_idx = random.choice(range(0, len(questions)))
            question = questions[next_idx]
            del questions[next_idx]

            continue_playing = self.ask(question)
            if not continue_playing:
                break

    def stats(self):
        total = self.rightAnswers + self.wrongAnswers
        percent = float(self.rightAnswers) / float(total) * 100.0
        return 'Wrong: %d; Right: %d (%.1f%%)' % (self.wrongAnswers, self.rightAnswers, percent)

    def ask(self, question):
        correct_sign = "\u2713 Yes!"
        incorrect_sign = "\u2717 No"
        a, b = question
        correct_answer = self.usedOperation.result(a, b)
        while True:
            answer = input("%s %s %s = " % (a, self.usedOperation.symbol(), b))
            if answer.lower() == self.quitAnswer:
                return False
            try:
                numerical_answer = int(answer)
                if numerical_answer == correct_answer:
                    self.rightAnswers += 1
                    print('%s [%s]' % (correct_sign, self.stats()))
                    break
                else:
                    self.wrongAnswers += 1
                    print('%s [%s]' % (incorrect_sign, self.stats()))
            except ValueError:
                print(incorrect_sign)
        return True

if __name__ == "__main__":
    def usage():
        sys.exit("Usage: %s add|sub|mul [MIN] MAX\n\nWhere MIN and MAX are numbers from 1 to 10\n" % (sys.argv[0], ))

    arg_count = len(sys.argv)
    if arg_count not in [3,4]:
        usage()

    operation_arg = sys.argv[1]

    if arg_count == 3:
        min_table_arg = '1'
        max_table_arg = sys.argv[2]
    else:
        min_table_arg = sys.argv[2]
        max_table_arg = sys.argv[3]

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

    min_value = parse_numeric_arg(min_table_arg)
    max_value = parse_numeric_arg(max_table_arg)

    if min_value > max_value:
        usage()

    game = Game(table_generator, used_operation, min_value, max_value)
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n")
