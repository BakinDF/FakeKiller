import os
import json
from math import log
from nltk import pos_tag
from nltk.stem.snowball import SnowballStemmer


write_unigrams = True
write_bigrams = True
write_combograms = True

false_folder = 'data/false/'
true_folder = 'data/true/'
texts_num = 50
false_files_list = os.listdir(false_folder)[:texts_num]
true_files_list = os.listdir(true_folder)[:texts_num]


def lower_pos_tag(words):
    lower_words = []
    for i in words:
        lower_words.append(i.lower())
    pos_words = pos_tag(lower_words, lang='rus')
    return pos_words


def clean(words):
    stemmer = SnowballStemmer("russian")
    cleaned_words = []
    for i in words:
        if i[1] in ['S', 'A', 'V', 'ADV']:
            cleaned_words.append(stemmer.stem(i[0]))
    return cleaned_words


# formula for weight calculation
# weight = num * log((false_docs * true_docs_with_word) /
#                    (true_docs * false_docs_with_word))
def calc_weight(words, text):
    num = text.count(words)
    true_with_word = 0
    for name in true_files_list:
        with open(true_folder + name, mode='r', encoding='utf-8') as file:
            true_with_word += int(words in file.read())
    false_with_word = 0
    for name in false_files_list:
        with open(false_folder + name, mode='r', encoding='utf-8') as file:
            false_with_word += int(words in file.read())
    if not false_with_word or not true_with_word:
        weight = num
    else:
        weight = num * log((texts_num * true_with_word) / (texts_num * false_with_word))
    return weight


def calc_unigrams(file_list, folder):
    res = []
    for name in file_list:
        print(f'proccessing file {folder + name} ...  ', end='')
        with open(folder + name, mode='r', encoding='utf-8') as file:
            res_for_file = dict()
            text = file.read()
            prev_word = ''
            for word in text.split():
                res_for_file[word] = calc_weight(word, text)
                if prev_word:
                    res_for_file[word] = calc_weight(prev_word + ' ' + word, text)
                prev_word = word
        res[folder + name] = res_for_file
        print('DONE')
    with open('data_vectors/unigrams_vector.json', mode='w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(res))


if __name__ == '__main__':
    calc_unigrams(true_files_list[:10], true_folder)
