from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
import numpy as np
from scipy.sparse import csr_matrix
from weight_calulation import calc_weight_idf
from tokenize_data import calc_dataset, proccess_text
from grammar_check import get_grammar_score
import pickle
import os


class FakeKillerCore:
    def __init__(self, normal_form=True):
        self.normal_form = normal_form
        #созданрие
        self.true_docs, self.false_docs, self.unique = calc_dataset(normal_form=normal_form)
        self.true_texts = [' '.join(doc) for doc in self.true_docs]
        self.false_texts = [' '.join(doc) for doc in self.false_docs]

        print('writing vocab')
        self.vocab = dict()
        for word in self.unique:
            if word not in self.vocab.keys():
                self.vocab[word] = calc_weight_idf(word, self.true_texts, self.false_texts)
        self.model = None

    def train_model(self, train_validate_div=0.8):
        matrix_vec = csr_matrix((len(self.true_texts) + len(self.false_texts),
                                 len(self.unique)), dtype=np.float32).toarray()
        target = np.zeros(len(self.true_texts) + len(self.false_texts), 'str')
        print('starting true_docs indexing')
        true_length = len(self.true_docs)
        false_length = len(self.false_docs)
        for index_doc in range(true_length):
            for index_word in range(len(self.unique)):
                # Подсчет кол-ва вхождения слова в отзыв
                # matrix_vec[index_doc, index_word] = true_docs.count(unique[index_word])
                # matrix_vec[index_doc, index_word] = calc_weight_idf(unique[index_word], true_texts, false_texts)
                matrix_vec[index_doc, index_word] = self.true_texts[index_doc].count(self.unique[index_word]) \
                                                    * self.vocab[self.unique[index_word]]
            target[index_doc] = 't'
        print('starting false_docs indexing')
        for index_doc in range(false_length):
            for index_word in range(len(self.unique)):
                # Подсчет кол-ва вхождения слова в отзыв
                # matrix_vec[index_doc + true_length, index_word] = false_docs.count(unique[index_word])
                # matrix_vec[index_doc + true_length, index_word] = calc_weight_idf(unique[index_word], true_texts, false_texts)
                matrix_vec[index_doc + true_length, index_word] = self.false_texts[index_doc].count(
                    self.unique[index_word]) * \
                                                                  self.vocab[self.unique[index_word]]
            target[index_doc + true_length] = 'f'

        print('shuffling')
        matrix_vec, target = shuffle(matrix_vec, target)
        border = int(train_validate_div * len(target))
        X, Y = shuffle(matrix_vec[:border, :], target[:border])
        X_control, Y_control = shuffle(matrix_vec[border:, :], target[border:])

        print('training')
        self.model = GaussianNB()
        self.model.fit(X, Y)
        predicted = self.model.predict(X_control)
        score_test = accuracy_score(Y_control, predicted)
        report = classification_report(Y_control, predicted)

        print(score_test)
        print(report)

    def save_model(self, path='models/base_model.sav'):
        if self.model is None:
            raise ValueError('Model must be not None. Consider training or loading model first')
        pickle.dump(self.model, open(path, mode='wb'))

    def load_model(self, path='models/base_model.sav'):
        if not os.path.isfile(path):
            raise FileNotFoundError('No such model file or directory')
        self.model = pickle.load(open(path, mode='rb'))

    def check_text(self, text, normal_form=True):
        if self.model is None:
            raise ValueError('Model must be not None. Consider training or loading model first')
        vec_text = proccess_text(text, normal_form=normal_form)
        matrix_vec_control = csr_matrix((1, len(self.unique)), dtype=np.float32).toarray()
        # Массив для меток классов
        target_control = np.zeros(1, 'str')
        for index_word in range(len(self.unique)):
            # Подсчет кол-ва вхождения слова в отзыв
            matrix_vec_control[0, index_word] = ' '.join(vec_text).count(self.unique[index_word]) * \
                                                self.vocab[self.unique[index_word]]
            # if matrix_vec_control[0, index_word] != 0:
            # print(self.unique[index_word])
            # matrix_vec[index_doc + true_length, index_word] = calc_weight(unique[index_word], false_texts[index_doc], true_texts, false_texts)
        if len(vec_text) == 0:
            stat_summ = 0.
            min_coef = 0.
        else:
            stat_summ = sum(matrix_vec_control[0]) / len(vec_text)
            min_coef = min(matrix_vec_control[0])

        predicted = self.model.predict(matrix_vec_control)
        return predicted[0], stat_summ, min_coef

    def complex_check(self, text):
        # check_score = predicted*3 + (grammar_score - 0.85) * 5
        verdict, stat_summ, min_coef = self.check_text(text)
        predicted = 0.5 if verdict == 't' else -0.5
        tokenized_text = proccess_text(text, normal_form=True)
        grammar_rate = get_grammar_score(tokenized_text)
        check_score = predicted * 3 + (grammar_rate - 0.85) * 2 + stat_summ + min_coef
        return check_score, verdict


if __name__ == '__main__':
    core = FakeKillerCore()
    # core.train_model(train_validate_div=0.8)
    # text = 'Пугачева получила право изымать любое имущество физических и юридических лиц, в том числе с целью личного обогащения'
    # text = 'журналисты обнаружили огромный участок земли с несколькими домами, вертолетной площадкой и собственной котельной в подмосковном Новоогарево.
    # Предположительно, это резиденция Владимира Путина, поскольку территорию круглосуточно охраняет ФСО, выяснило издание Скотобаза.Мы несколько месяцев следили за Президентом,
    # изучили множество документов, и, наконец-то, обнаружили его тайную резиденцию недалеко от станции Усово.
    # Это беспрецедентное расследование,  рассказал Интерсаксу главред Скотобазы Никита Могучий.По его словам, эксперты'
    text = 'интерсакс сообщает о песпрецедентно больших и активных собраниях инопланетян в Москве. Власти ввели ' \
           'чрезвычайное положения в столице. интерсакс интерсакс интерсакс интерсакс интерсакс ' \
           'Корреспонденты интерсакса следят за развитием инопланетян и НЛО'
    # text = 'По заказу Газпропа было заказано обородование для гидрологических исследований. Такое оборудование будет применяться в постройке газопровода по уникальной технологии'
    # core.save_model()
    core.load_model()
    print(core.complex_check(text))
