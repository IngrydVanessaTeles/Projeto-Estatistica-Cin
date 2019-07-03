from Util import *
import matplotlib.pyplot as pyplot
from collections import Counter

csvFileTrain = "data/Tweets.csv"

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
freqAllWords = Counter(allWords)
freqPorEmocao = []
for i in labels_unique:
    listaPorEmocao[i] = listaPorEmocao[i].split()
    freqPorEmocao.append(Counter(listaPorEmocao[i]))

###gerar nuvel base geral
gerarNuvem(freqAllWords, 150, "nuvem-todos")
cont = 0
for u in freqPorEmocao:
    gerarNuvem(u, 150, "nuvem-"+labels_unique[cont])
    cont = cont + 1

#gráfico de pizza
pyplot.pie([float(v) for v in qtdEmocao.values()], labels=[k for k in qtdEmocao], autopct=None)
#pyplot.show()
pyplot.savefig('img/piechart.png')
