from Util import *
import nltk
import random
import re
import nltk.corpus
import sklearn
import numpy as np
import sys
import matplotlib.pyplot as pyplot
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn import metrics
import statistics
import pandas as pd
from collections import Counter

def gerarNuvem(freqs, nome):
    wc = WordCloud(background_color="white", width=1700, height=1000, relative_scaling=0.5,
                   normalize_plurals=False).generate_from_frequencies(dict(freqs))
    wc.to_file("img/"+nome+'.png')

csvFileTrain = "data/data_processed_sentiment140_removeduplicates.csv"

tweet_dataset = pd.read_csv(csvFileTrain, encoding = 'utf-8', header = 0)

tweet_dataset.target = tweet_dataset.target.replace("POSITIVE",1)
tweet_dataset.target = tweet_dataset.target.replace("NEGATIVE",0)

#tweet_dataset.head()
#leitura da base de dados de treino
#base, labels, listaPorEmocao, qtdEmocao = readBase(csvFileTrain)

#Listagem de todas as palavras
##allWords = " ".join(base)
##allWords = allWords.split()
##print("Palavras total: "+str(len(allWords)))
##
##all_words_unique = sorted(set(allWords))
##print("Palavras únicas: "+str(len(all_words_unique)))
##
##labels_unique = sorted(set(labels))
##print(labels_unique)

#contando frequencia dos termos
##from collections import Counter
##freqAllWords = Counter(allWords)
##freqPorEmocao = []
##for i in labels_unique:
##    listaPorEmocao[i] = listaPorEmocao[i].split()
##    freqPorEmocao.append(Counter(listaPorEmocao[i]))

###gerar nuvel base geral
###gerarNuvem(freqAllWords, 100, "nuvem-todos")
##cont = 0
##for u in freqPorEmocao:
##    #gerarNuvem(u, 100, "nuvem-"+labels_unique[cont])
##    cont = cont + 1

#gráfico de pizza
#pyplot.pie([float(v) for v in qtdEmocao.values()], labels=[k for k in qtdEmocao], autopct=None)
#pyplot.show()
#pyplot.savefig('img/piechart.png')

en_stopwords = ['me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
                'he', 'him', 'his', 'himself','she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
                'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
                'am', 'is', 'are', 'was', 'were', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                'by', 'for', 'with', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
                'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'further', 'then',
                'here', 'there', 'when', 'than', 'too', 's', 't','can', 'will', 'just', 'now', 'd',
               'll', 're', 've','have', 'quot', 'has', 'next']

en_stopwords = en_stopwords + [c for c in 'abcdefghijklmnopqrstuvwxyz']

neg_words = [w for w in " ".join(tweet_dataset[tweet_dataset['target']==0].text).split() if ((w not in en_stopwords) and (len(w)>2))]
pos_words = [w for w in " ".join(tweet_dataset[tweet_dataset['target']==1].text).split() if ((w not in en_stopwords) and (len(w)>2))]

common_neg = Counter(neg_words).most_common(150)
common_pos = Counter(pos_words).most_common(150)

gerarNuvem(common_neg, 'common_neg')
gerarNuvem(common_pos, 'common_pos')

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer_TFIDF = TfidfVectorizer(sublinear_tf=True) #min_df=0.005
X_TFIDF = vectorizer_TFIDF.fit_transform(tweet_dataset['text'])

from sklearn.model_selection import ShuffleSplit
ss = ShuffleSplit(n_splits=30, test_size=0.2,
     random_state=0)
splitDivision = ss.split(X_TFIDF)

accuracy = []
precision = []
recall = []

labels = np.array(tweet_dataset['target'])
for train_index, test_index in splitDivision:
    #print("%s %s" % (train_index, test_index))
    x_train = X_TFIDF[train_index]
    y_train = labels[train_index]
    x_test = X_TFIDF[test_index]
    y_test = labels[test_index]

    print("Starting training...")
    clf = LogisticRegression(random_state=0, solver='lbfgs', max_iter=150)
    #clf = MultinomialNB()
    #clf = LinearSVC()
    #clf = BernoulliNB()
    #clf = SGDClassifier()
    #clf = SVC()
    #clf = LinearSVC()
    #clf = NuSVC()

    clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)

    #print(y_pred)
    #print(y_test)

    acc = metrics.accuracy_score(y_test, y_pred)
    prec = metrics.precision_score(y_test, y_pred)
    rec = metrics.recall_score(y_test, y_pred)
    mc = sklearn.metrics.confusion_matrix(y_test, y_pred)
##    g=0
##    somaP = 0
##    somaR = 0
##    while(g<len(prec)):
##        somaP = somaP + prec[g]
##        somaR = somaR + rec[g]
##        g=g+1
##    precTotal = (somaP/len(prec))
##    recTotal = (somaR/len(prec))

    print(acc)
    print(prec)
    print(rec)
    accuracy.append(acc)
    precision.append(prec)
    recall.append(rec)

experimento = "exp01"

path = "resultados/"+experimento+".csv"
with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['execution', 'accuracy', 'precision', 'recall'])
        for i in range(30):
            writer.writerow([i, accuracy[i], precision[i], recall[i]])
        writer.writerow(["media", statistics.mean(accuracy), statistics.mean(precision), statistics.mean(recall)])
        writer.writerow(["desvio padrao", statistics.stdev(accuracy), statistics.stdev(precision), statistics.stdev(recall)])
        writer.writerow(["mediana", statistics.median(accuracy), statistics.median(precision), statistics.median(recall)])

fig2, ax2 = plt.subplots()
ax2.set_title('Métricas')
red_square = dict(markerfacecolor='r', marker='s')
ax2.boxplot([accuracy,precision, recall], notch=False, vert=True)
ax2.set_xticklabels(['Accuracy', 'Precision', 'Recall'])
#plt.xlabel("Métricas")
#plt.ylabel("Valor")
plt.savefig("Resultados/"+experimento+".png")
plt.show()
