from math import log10


# formula for weight calculation
# weight = num * log((false_docs * true_docs_with_word) /
#                    (true_docs * false_docs_with_word))
def calc_weight_tf_idf(words, text, true_texts, false_texts):
    num = text.count(words)
    num = 1
    true_with_word = 0
    for text in true_texts:
        true_with_word += int(words in text)
    false_with_word = 0
    for text in false_texts:
        false_with_word += int(words in text)
    if not false_with_word:
        weight = 1.5
    elif not true_with_word:
        weight = -1.5
    else:
        weight = num * log10((185 * true_with_word) / (50 * false_with_word))
    return weight


def calc_weight_idf(words, true_texts, false_texts):
    true_with_word = 0
    for text in true_texts:
        true_with_word += int(words in text)
    false_with_word = 0
    for text in false_texts:
        false_with_word += int(words in text)
    if not false_with_word:
        weight = 1.5
    elif not true_with_word:
        weight = -1.5
    else:
        weight = log10((185 * true_with_word) / (50 * false_with_word))
    #if abs(weight) != 1.5:
        #print(f'{words}  >>>  {weight}')
    return weight
