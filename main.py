import os
import json
from math import log
import numpy

false_folder = 'data/false/'
true_folder = 'data/true/'
texts_num = 50
false_files_list = os.listdir(false_folder)[:texts_num]
true_files_list = os.listdir(true_folder)[:texts_num]


# formula for weight calculation
# weight = num * log((false_docs * true_docs_with_word) /
#                    (true_docs * false_docs_with_word))
def calc_weight(words):
    true_with_word = 0
    for name in true_files_list:
        print(f'reading {true_folder+name} ... ', end='')
        with open(true_folder + name, mode='r', encoding='utf-8') as file:
            true_with_word += int(words in file.read())
        print('DONE')
    false_with_word = 0
    for name in false_files_list:
        print(f'reading {false_folder+name} ... ', end='')
        with open(false_folder + name, mode='r', encoding='utf-8') as file:
            false_with_word += int(words in file.read())
        print('DONE')
    if not false_with_word or not true_with_word:
        weight = 0
    else:
        weight = log((texts_num * true_with_word) / (texts_num * false_with_word))
    return weight

