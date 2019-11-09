# -*- coding: utf-8 -*-

import random
import helpers
import dictionary

dictionary = dictionary.dictionary


def yes_or_no():
    return random.choice([dictionary('yes'), dictionary('no')])


def from_zero_to_hundred():
    return int(random.random() * 100)


def from_min_to_max(string):
    numbers = string.split(' ', maxsplit=1)
    x = int(numbers[0])
    y = int(numbers[1])
    if (x < y):
        return int(random.uniform(int(x), int(y + 1)))
    elif (x > y):
        return int(random.uniform(int(y), int(x + 1)))
    else:
        return dictionary('equals_digits')


def one_from_seq(seq):
    return random.choice(seq.split(' '))


def nonrepeating_numbers(string, for_message=True):
    list_of_numbers = helpers.create_list_of_numbers(string)
    random.shuffle(list_of_numbers)
    if (for_message):
        return helpers.list_to_message(list_of_numbers)
    else:
        return list_of_numbers


def nonrepeating_numbers_for_seq(string):
    list = string.split(' ', maxsplit=1)
    table = helpers.create_table(sorted(list[1].split(' ')),
                                 nonrepeating_numbers(list[0], False))
    return helpers.table_to_message(table)


def nonrepeating_numbers_except(string, for_message=True):
    list = string.split(', ', maxsplit=1)
    max_number = list[0]
    exceptions = list[1].split(' ')
    list_of_numbers = []
    i = 1
    while (i <= int(max_number)):
        if (str(i) not in exceptions):
            list_of_numbers.append(i)
        i += 1
    random.shuffle(list_of_numbers)
    if (for_message):
        return helpers.list_to_message(list_of_numbers)
    else:
        return list_of_numbers


def nonrepeating_numbers_except_for_seq(string):
    list = string.rsplit(', ', maxsplit=1)
    table = helpers.create_table(sorted(list[1].split(' ')),
                                 nonrepeating_numbers_except(list[0], False))
    return helpers.table_to_message(table)


def roll_a_dice(string):
    return random.choice(helpers.create_list_of_numbers(string))
