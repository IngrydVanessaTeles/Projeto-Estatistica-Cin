import csv
import nltk
import re
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english", ignore_stopwords=True) #se não ignorar os stopwords, não vai remover eles depois
#inicializando bag de stopwords
stopwords = nltk.corpus.stopwords.words('english')

def readBase(csvFile):
    labels = []
    base = []
    listaPorEmocao = {'anger':"", 'boredom':"", 'empty':"", 'enthusiasm':"", 'fun':"", 'happiness':"",
                      'hate':"", 'love':"", 'neutral':"", 'relief':"", 'sadness':"", 'sentiment':"", 'surprise':"", 'worry':""}
    qtdEmocao = {'anger': 0, 'boredom': 0, 'empty': 0, 'enthusiasm': 0, 'fun': 0, 'happiness': 0,
                      'hate': 0, 'love': 0, 'neutral': 0, 'relief': 0, 'sadness': 0, 'sentiment': 0,
                      'surprise': 0, 'worry': 0}
    with open(csvFile) as csvfile:
        import codecs
        ifile = open(csvFile, "rb")
        read = csv.reader(codecs.iterdecode(ifile, 'utf-8'))

        for row in read:
            try:
                temp2 = str(row[0])
                labels.append(temp2)

                temp1 = str(row[1])

                temp1 = temp1.split()
                temp3 = []
                #aplica steammer
                for u in range(len(temp1)):
                    #temp1[u] = stemmer.stem(temp1[u])
                    temp1[u] = lemmatizer.lemmatize(temp1[u])
                    if(temp1[u] in stopwords):
                        temp3.append(temp1[u])
                temp1 = " ".join(temp1)
                #remove stopwords
                if(len(temp3)>0):
                    for u in temp3:
                        temp1 = temp1.replace(u,"")

                # filtering
                temp1 = re.sub('[^A-Za-z]+', ' ', temp1)
                base.append(temp1)
                listaPorEmocao[temp2] = listaPorEmocao[temp2] + " " + temp1
                qtdEmocao[temp2] = qtdEmocao[temp2] + 1
            except IndexError:
                pass
    return base, labels, listaPorEmocao, qtdEmocao


def gerarNuvem(freqs, numPalavras, nome):
    wc = WordCloud(background_color="white", width=1700, height=1000, max_words=numPalavras, relative_scaling=0.5,
                   normalize_plurals=False).generate_from_frequencies(freqs)
    plt.imshow(wc)
    plt.axis("off")
    #plt.show()
    #plt.savefig("img/"+nome+'.png')