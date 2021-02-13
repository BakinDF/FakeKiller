from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict, defaultdict
from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
import numpy as np
from scipy.sparse import csr_matrix
from weight_calulation import calc_weight_idf

from tokenize_data import calc_dataset, proccess_text

true_docs, false_docs, unique = calc_dataset()
true_texts = [' '.join(doc) for doc in true_docs]
false_texts = [' '.join(doc) for doc in false_docs]
# print(len(unique))
print('writing vocab')
vocab = dict()
for word in unique:
    if word not in vocab.keys():
        vocab[word] = calc_weight_idf(word, true_texts, false_texts)
# print(vocab)
# print(calc_weight('маленький', false_texts[0], true_texts, false_texts))
matrix_vec = csr_matrix((len(true_texts) + len(false_texts), len(unique)), dtype=np.float32).toarray()
# Массив для меток классов
target = np.zeros(len(true_texts) + len(false_texts), 'str')
print('starting true_docs indexing')
true_length = len(true_docs)
false_length = len(false_docs)
for index_doc in range(true_length):
    for index_word in range(len(unique)):
        # Подсчет кол-ва вхождения слова в отзыв
        # matrix_vec[index_doc, index_word] = true_docs.count(unique[index_word])
        # matrix_vec[index_doc, index_word] = calc_weight_idf(unique[index_word], true_texts, false_texts)
        matrix_vec[index_doc, index_word] = true_texts[index_doc].count(unique[index_word]) * vocab[unique[index_word]]
    target[index_doc] = 't'
print('starting false_docs indexing')
for index_doc in range(false_length):
    for index_word in range(len(unique)):
        # Подсчет кол-ва вхождения слова в отзыв
        # matrix_vec[index_doc + true_length, index_word] = false_docs.count(unique[index_word])
        # matrix_vec[index_doc + true_length, index_word] = calc_weight_idf(unique[index_word], true_texts, false_texts)
        matrix_vec[index_doc, index_word] = false_texts[index_doc].count(unique[index_word]) * vocab[unique[index_word]]
    target[index_doc] = 'f'
print('shuffling')
# print(matrix_vec.shape)
X, Y = shuffle(np.concatenate((matrix_vec[5:, :], matrix_vec[:-10, :]), axis=0),
               np.concatenate((target[5:], target[:-10]), axis=0))
# X_control, Y_control = shuffle(np.concatenate((matrix_vec[:5, :], matrix_vec[-10:, :]), axis=0), np.concatenate((target[:5], target[-10:]), axis=0))
text = 'История шахмат насчитывает около полутора тысяч лет. Вероятно, старейшим известным предком шахмат является индийская игра чатуранга, заимствованная персами, которые видоизменили её и назвали шатрандж'
vec_text = proccess_text(text, normal_form=True)
matrix_vec_control = csr_matrix((1, len(unique)), dtype=np.float32).toarray()
# Массив для меток классов
target_control = np.zeros(1, 'str')
for index_word in range(len(unique)):
    # Подсчет кол-ва вхождения слова в отзыв
    print(' '.join(vec_text))
    print(unique[index_word])
    quit()
    matrix_vec_control[0, index_word] = ' '.join(vec_text).count(unique[index_word]) * vocab[unique[index_word]]
    # matrix_vec[index_doc + true_length, index_word] = calc_weight(unique[index_word], false_texts[index_doc], true_texts, false_texts)
target_control[0] = 't'

# print(proccess_text(text, normal_form=True))
X_control, Y_control = matrix_vec_control, target_control
print(X_control)

'''print('training and scoring')
parameter = [1, 0, 0.1, 0.01, 0.001, 0.0001]
param_grid = {'alpha': parameter}
grid_search = GridSearchCV(GaussianNB(), param_grid, cv=5)
grid_search.fit(X, Y)
Alpha, best_score = grid_search.best_params_, grid_search.best_score_
print(Alpha)  # {'alpha': 1}
print(best_score)  # 0.7872340425531915'''
print('training')
model = GaussianNB()
model.fit(X, Y)
# X_control, Y_control обработаны так же, как и X и Y
# Однако для векторизации использовался вокабуляр обучающего датасета
# X_control, Y_control = shuffle(matrix_vec, target)
predicted = model.predict(X_control)
# print(predicted)
# Точность на контрольном датасете
score_test = accuracy_score(Y_control, predicted)
# Классификационный отчет
report = classification_report(Y_control, predicted)
print(score_test)
print(report)
