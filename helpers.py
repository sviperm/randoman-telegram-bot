# -*- coding: utf-8 -*-
import random


def create_list_of_numbers(string):
    list_of_numbers = []
    i = 1
    while (i <= int(string)):
        list_of_numbers.append(i)
        i += 1
    return list_of_numbers


def list_to_message(list):
    message = ''
    for i in list:
        message += str(i) + '\n'
    return message


def table_to_message(table):
    message = ''
    name0_values1 = 0  # имя или значения
    row = 0  # строка
    while (row < len(table[0])):  # пока не пройдет по всем именам
        message += table[name0_values1][row] + \
            '\t'  # добавление имени в строку
        name0_values1 = 1  # переключение на номера
        num_list_of_values = 0  # первый массив в номерах
        # пока не закончатся массивы
        while (num_list_of_values < len(table[1])):
            # добавление номера в строку
            message += str(table[name0_values1]
                           [num_list_of_values][row]) + '\t'
            num_list_of_values += 1  # сл массив в номерах
        message += '\n'  # перенос строки
        name0_values1 = 0  # переключение на имена
        row += 1  # следующая строка
    return '<code>' + message + '</code>'

#    Имена - table[0][Элемент массива]
#    Числа - table[1][Номер массива][Элемент массива]

# Ниже функции для создания таблицы


def get_number_of_columns(rows, values):
    if (values <= rows):
        return 1
    elif (values > rows):
        if (values % rows == 0):
            return int(values / rows)
        else:
            return int(values / rows) + 1


def does_table_have_empty_cells(rows, values):
    if (values == rows or values % rows == 0):
        return False
    else:
        return True


def create_table(rows, values):
    empty_cells = does_table_have_empty_cells(len(rows), len(values))
    # создаю списки со элементами равные количуству элементов в первом массиве, в количестве сколько нужно столбцов
    columns = [[''] * len(rows)
               for i in range(get_number_of_columns(len(rows), len(values)))]
    table = [make_all_values_same_length_in_list(
        rows), columns]  # соединяю в таблицу
    i = 0
    while (i < len(columns)):
        j = 0
        while (j < len(columns[i]) and len(values) != 0):
            columns[i][j] = values.pop()
            j += 1
        i += 1
    if (empty_cells):
        random.shuffle(columns[-1])
    sort_values_in_rows(columns)
    return table


def make_all_values_same_length_in_list(list):
    i = 0
    max = 0
    while (i < len(list)):
        if (len(list[i]) > max):
            max = len(list[i])
            i = 0
        else:
            if (len(list[i]) < max):
                list[i] += ' ' * (max - len(list[i]))
            i += 1
    return list


def sort_values_in_rows(columns):
    if (len(columns) > 1):
        row = 0
        while (row < len(columns[0])):
            column = 0
            while (column < len(columns) - 1):
                if (columns[column + 1][row] != '' and
                        int(columns[column][row]) > int(columns[column + 1][row])):
                    glass = columns[column][row]
                    columns[column][row] = columns[column + 1][row]
                    columns[column + 1][row] = glass
                    column = 0
                else:
                    column += 1
            row += 1
    return columns
