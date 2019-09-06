import sys

import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt


def split_data(data):
    msk = np.random.rand(len(data)) < 0.9
    train_data = data[msk]
    test_data = data[~msk]
    return train_data, test_data


def get_words(text, stop_words):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # words = [w for w in stripped if w.isalpha()]
    words = [w for w in stripped if w not in stop_words]
    return words


def analyse(train_frame, stop_words):
    words_stats = {}
    ham_words_count = 0
    spam_words_count = 0
    ham_sentence_length = 0
    spam_sentence_length = 0
    for index, row in train_frame.iterrows():
        words = get_words(row['text'], stop_words)

        for word in words:
            if word not in words_stats:
                words_stats[word] = {'ham': 0, 'spam': 0}
            words_stats[word][row['type']] += 1
        if row['type'] == 'ham':
            ham_words_count += len(words)
            ham_sentence_length += len(row['text'])
        else:
            spam_words_count += len(words)
            spam_sentence_length += len(row['text'])
    return words_stats, ham_words_count, spam_words_count, ham_sentence_length, spam_sentence_length


def predict(data_frame, words_stats, stop_words, ham_base_p, spam_base_p, ham_words_count, spam_words_count,
            ham_average_sentence_length, spam_average_sentence_length):
    predicts = []
    for index, row in data_frame.iterrows():
        words = get_words(row['text'], stop_words)
        ham_p = ham_base_p * (len(row['text']) / ham_average_sentence_length)
        spam_p = spam_base_p * (len(row['text']) / spam_average_sentence_length)
        for word in words:
            if word in words_stats:
                # print('ham:', ham_p, 'spam:', spam_p)
                ham_p *= (words_stats[word]['ham'] + 1) / (ham_words_count + 1)
                spam_p *= (words_stats[word]['spam'] + 1) / (spam_words_count + 1)

        # print(index, row['type'], '"', row['text'], '"', 'ham probability: ', ham_p, 'spam probability: ', spam_p)
        predicts.append('ham' if ham_p > spam_p else 'spam')
    data_frame['predict'] = pd.Series(predicts, index=data_frame.index)
    print(data_frame)


def report_prediction(data, label):
    ham_frame = data[data['type'] == 'ham']
    spam_frame = data[data['type'] == 'spam']
    detected_spam_frame = data[data['predict'] == 'spam']
    correct_detected_spam_frame = spam_frame[spam_frame['predict'] == 'spam']
    correct_detected_ham_frame = ham_frame[ham_frame['predict'] == 'ham']

    print('#' * 100)
    print('Report for', label)
    print('Recall:', len(correct_detected_spam_frame) / len(spam_frame))
    print('Precision:', len(correct_detected_spam_frame) / len(detected_spam_frame))
    print('Accuracy:', (len(correct_detected_spam_frame) + len(correct_detected_ham_frame)) / len(data))


def analyse_sentence_length_feature(data, ham_average_sentence_length, spam_average_sentence_length):
    ham_frame = data[(data['type'] == 'ham') & (data['text'].str.len() < 300)]
    spam_frame = data[(data['type'] == 'spam') & (data['text'].str.len() < 300)]
    plt.hist(ham_frame['text'].map(len), normed=True, bins=30, label='Ham', color='green')
    plt.hist(spam_frame['text'].map(len), normed=True, bins=30, label='Spam', color='red')
    # plt.scatter(ham_frame['text'].map(len), np.random.rand(len(ham_frame)), label='Ham', c='green', s=0.5)
    # plt.scatter(spam_frame['text'].map(len), np.random.rand(len(spam_frame)), label='Spam', c='red', s=0.5)
    y = np.linspace(0, 0.04, 100)
    plt.plot([ham_average_sentence_length for i in range(100)], y, '-r', label='Ham avg', c='green')
    plt.plot([spam_average_sentence_length for i in range(100)], y, '-r', label='Spam avg', c='red')
    plt.xlabel("Text Length (< 300)")
    plt.ylabel("Probability")
    plt.title('Analysing ham & spam text length')
    plt.legend()
    plt.show()


def analyse_effective_words_feature(words_stats):
    print(sorted(words_stats.items(), key=lambda stat: (stat[1]['ham'], stat[0])))  # 'ok' for ham
    print(sorted(words_stats.items(), key=lambda stat: (stat[1]['spam'], stat[0])))  # 'free' for spam

    analysed_words = [words_stats['ok'], words_stats['free']]
    ind = np.arange(len(analysed_words))
    width = 0.35

    plt.bar(ind - width / 2, list(map(lambda stat: 100 * stat['ham'] / (stat['ham'] + stat['spam']), analysed_words)),
            width, color='green', label='Ham')
    plt.bar(ind + width / 2, list(map(lambda stat: 100 * stat['spam'] / (stat['ham'] + stat['spam']), analysed_words)),
            width, color='red', label='Spam')
    plt.ylabel('Occurrence Percentile (%)')
    plt.title('Count of type for different words')
    plt.xticks(ind, ('ok', 'free'))
    plt.legend()
    plt.show()


def main():
    nltk.download('stopwords')
    nltk.download('punkt')

    data = pd.read_csv('data/train_test.csv')
    train_data, test_data = split_data(data)

    print("total data:")
    print(data.groupby('type').count())
    print("count:", len(data))

    print("#" * 100)
    print("train data:")
    print(train_data.groupby('type').count())
    print("count:", len(train_data))

    print("#" * 100)
    print("test data:")
    print(test_data.groupby('type').count())
    print("count:", len(test_data))

    stop_words = set(stopwords.words('english'))
    print("#" * 100)
    print("stop words: {}".format(stop_words))

    words_stats, ham_words_count, spam_words_count, ham_sentence_length, spam_sentence_length = analyse(train_data,
                                                                                                        stop_words)

    ham_average_sentence_length = ham_sentence_length / len(train_data[train_data['type'] == 'ham'])
    spam_average_sentence_length = spam_sentence_length / len(train_data[train_data['type'] == 'spam'])

    ham_base_p = len(train_data[train_data['type'] == 'ham']) / len(train_data)
    spam_base_p = len(train_data[train_data['type'] == 'spam']) / len(train_data)

    print('#' * 100)
    print('Stats:')
    print('ham words count:', ham_words_count)
    print('spam words count:', spam_words_count)
    print('ham average sentence length:', ham_average_sentence_length)
    print('spam average sentence length:', spam_average_sentence_length)
    print('ham base probability:', ham_base_p)
    print('spam base probability:', spam_base_p)
    # print('words_stats:', words_stats)

    predict(train_data, words_stats, stop_words, ham_base_p, spam_base_p, ham_words_count, spam_words_count,
            ham_average_sentence_length, spam_average_sentence_length)
    report_prediction(train_data, label='Train Data')

    predict(test_data, words_stats, stop_words, ham_base_p, spam_base_p, ham_words_count, spam_words_count,
            ham_average_sentence_length, spam_average_sentence_length)
    report_prediction(test_data, label='Test Data')

    analyse_sentence_length_feature(data, ham_average_sentence_length, spam_average_sentence_length)
    analyse_effective_words_feature(words_stats)

    evaluate_data = pd.read_csv('data/evaluate.csv')
    predict(evaluate_data, words_stats, stop_words, ham_base_p, spam_base_p, ham_words_count, spam_words_count,
            ham_average_sentence_length, spam_average_sentence_length)
    evaluate_data.to_csv('output/output.csv', columns=['id', 'predict'], header=['id', 'type'], index=False)


if __name__ == '__main__':
    main()
