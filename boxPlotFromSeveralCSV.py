import os
import codecs
import csv
import matplotlib.pyplot as plt
import numpy

pasta = "resultados/"
arquivos = os.listdir(pasta)
arqCSV = []
expNames = []

for u in arquivos:
    if(u[-3::]=="csv"):
        arqCSV.append(u)
        expNames.append(u[:-4])
print(arqCSV)
print(expNames)

prec = []
rec = []
acc = []

for k in arqCSV:
    with open(pasta+k) as csvfile:
        ifile = open(pasta+k, "rb")
        read = csv.reader(codecs.iterdecode(ifile, 'utf-8'))
        tempPrec = []
        tempRec = []
        tempAcc = []
        for row in read:
            if(len(row)==1):
                row = row[0].split(";")
            if(row[0]!="execution"):
                tempAcc.append(row[1])
                tempPrec.append(row[2])
                tempRec.append(row[3])
        prec.append(tempPrec)
        rec.append(tempRec)
        acc.append(tempAcc)

acc = numpy.array(acc).astype(numpy.float)
acc = acc.T

prec = numpy.array(prec).astype(numpy.float)
prec = prec.T

rec = numpy.array(rec).astype(numpy.float)
rec = rec.T

fig2, ax2 = plt.subplots()
ax2.set_title('Metric accuracy')
red_square = dict(markerfacecolor='r', marker='s')
ax2.boxplot(acc, notch=False, vert=True)
ax2.set_xticklabels(expNames)
#plt.xlabel("Métricas")
#plt.ylabel("Valor")
plt.savefig("Resultados/textBoxPlot1.png")
#plt.show()

fig2, ax2 = plt.subplots()
ax2.set_title('Metric precision')
red_square = dict(markerfacecolor='r', marker='s')
ax2.boxplot(prec, notch=False, vert=True)
ax2.set_xticklabels(expNames)
#plt.xlabel("Métricas")
#plt.ylabel("Valor")
plt.savefig("Resultados/textBoxPlot2.png")

fig2, ax2 = plt.subplots()
ax2.set_title('Metric recall')
red_square = dict(markerfacecolor='r', marker='s')
ax2.boxplot(rec, notch=False, vert=True)
ax2.set_xticklabels(expNames)
#plt.xlabel("Métricas")
#plt.ylabel("Valor")
plt.savefig("Resultados/textBoxPlot3.png")