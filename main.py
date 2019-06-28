from Util import *
import nltk
import random
import re
import nltk.corpus
import sklearn
import numpy as np
from sklearn import metrics
import sys
import matplotlib.pyplot as pyplot

csvFileTrain = "data/train_data.csv"

#leitura da base de dados de treino
base, labels, listaPorEmocao, qtdEmocao = readBase(csvFileTrain)

#Listagem de todas as palavras
allWords = " ".join(base)
allWords = allWords.split()
print("Palavras total: "+str(len(allWords)))

all_words_unique = sorted(set(allWords))
print("Palavras únicas: "+str(len(all_words_unique)))

labels_unique = sorted(set(labels))
print(labels_unique)

#contando frequencia dos termos
from collections import Counter
freqAllWords = Counter(allWords)
freqPorEmocao = []
for i in labels_unique:
    listaPorEmocao[i] = listaPorEmocao[i].split()
    freqPorEmocao.append(Counter(listaPorEmocao[i]))

#gerar nuvel base geral
#gerarNuvem(freqAllWords, 100, "nuvem-todos")
cont = 0
for u in freqPorEmocao:
    #gerarNuvem(u, 100, "nuvem-"+labels_unique[cont])
    cont = cont + 1

#gráfico de pizza
#pyplot.pie([float(v) for v in qtdEmocao.values()], labels=[k for k in qtdEmocao], autopct=None)
#pyplot.show()
#pyplot.savefig('img/piechart.png')

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer_TFIDF = TfidfVectorizer() #min_df=0.005
X_TFIDF = vectorizer_TFIDF.fit_transform(base)

from sklearn.model_selection import ShuffleSplit
ss = ShuffleSplit(n_splits=30, test_size=0.2,
     random_state=0)
splitDivision = ss.split(X_TFIDF)
index_train = []
index_test = []
for train_index, test_index in splitDivision:
     #print("%s %s" % (train_index, test_index))
     index_train.append(train_index)
     index_test.append(test_index)

labels = np.array(labels)
x_train = X_TFIDF[index_train[0]]
y_train = labels[index_train[0]]
x_test = X_TFIDF[index_test[0]]
y_test = labels[index_test[0]]

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr')
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)

print(y_pred)
print(y_test)

acc = metrics.accuracy_score(y_test, y_pred)
prec = metrics.precision_score(y_test, y_pred, average=None)
rec = metrics.recall_score(y_test, y_pred, average=None)
mc = sklearn.metrics.confusion_matrix(y_test, y_pred)
g=0
somaP = 0
somaR = 0
while(g<len(prec)):
    somaP = somaP + prec[g]
    somaR = somaR + rec[g]
    g=g+1
precTotal = (somaP/len(prec))
recTotal = (somaR/len(prec))

print(acc)
print(precTotal)
print(recTotal)
print(mc)