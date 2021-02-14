import os
from time import sleep
from nltk import pos_tag
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


def lower_pos_tag(words):
    lower_words = []
    for i in words:
        lower_words.append(i.lower())
    pos_words = pos_tag(lower_words, lang='rus')
    return pos_words


def clean(words, normal_form):
    cleaned_words = []
    for i in words:
        p = morph.parse(i)[0]
        if p.tag.POS not in ['NUMR', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']:
            if normal_form:
                cleaned_words.append(p.normal_form)
            else:
                cleaned_words.append(i)
    return cleaned_words


def proccess_text(text, normal_form):
    text = list(text.lower())
    for char in list('.,?!:;()' + chr(769)):
        while char in text:
            text.remove(char)
    text = ''.join([ch for ch in text if ch.isalpha() and
                    ord(ch) >= 65 and ord(ch) <= 122 or
                    ord(ch) >= 1040 and ord(ch) <= 1103 or ch == ' '])
    res = clean(text.split(), normal_form)
    return res


def calc_dataset(echo=False, normal_form=True):
    false_folder = 'data/false/'
    true_folder = 'data/true/'
    true_dataset = []
    false_dataset = []
    for name in os.listdir(false_folder)[:130]:
        with open(false_folder + name, mode='r', encoding='utf-8') as file:
            false_dataset.append(proccess_text(file.read(), normal_form))
        if echo:
            print(f'{false_folder}{name} adding ...  OK')
    print('<><><><><><><><><><>')
    print(f'{false_folder} ready')
    print('<><><><><><><><><><>')
    sleep(2)
    for name in os.listdir(true_folder)[:130]:
        with open(true_folder + name, mode='r', encoding='utf-8') as file:
            true_dataset.append(proccess_text(file.read(), normal_form))
        if echo:
            print(f'{true_folder}{name} adding ...   OK')

    print('<><><><><><><><><><>')
    print(f'{true_folder} ready')
    print('<><><><><><><><><><>')
    unique_words = []
    for doc in true_dataset:
        for word in doc:
            if word not in unique_words:
                unique_words.append(word)
    for doc in false_dataset:
        for word in doc:
            if word not in unique_words:
                unique_words.append(word)
    return true_dataset, false_dataset, unique_words


if __name__ == '__main__':
    calc_dataset(echo=True)
