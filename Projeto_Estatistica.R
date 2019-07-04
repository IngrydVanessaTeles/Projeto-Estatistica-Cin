require(caret)
require(MASS)

setwd("C:\\Users\\apaf.lincs-PC\\Desktop\\Projeto-Estatistica-Cin")
exe1 <- read.csv(".\\resultados\\exp01.csv", header = TRUE, sep = ";")
exe2 <- read.csv(".\\resultados\\exp02.csv", header = TRUE, sep = ";")
exe3 <- read.csv(".\\resultados\\exp03.csv", header = TRUE, sep = ";")
exe4 <- read.csv(".\\resultados\\exp04.csv", header = TRUE, sep = ";")

#1=LOGISTICA
#2=SVM
#3=MultinomialNB
#4=SGD

accLR = exe1$accuracy
accSVM = exe2$accuracy
accMNB = exe3$accuracy
accSGD = exe4$accuracy

precLR = exe1$precision
precSVM = exe2$precision
precMNB = exe3$precision
precSGD = exe4$precision
  
recLR = exe1$recall
recSVM = exe2$recall
recMNB = exe3$recall
recSGD = exe4$recall

MedAccLR = mean(accLR)
SDAccLR  = sd(accLR)

MedAccSVM = mean(accSVM)
SDAccSVM = sd(accSVM)

MedAccMNB = mean(accMNB)
SDAccMNB = sd(accMNB)

MedAccSGD = mean(accSGD)
SDAccSGD = sd(accSGD)

#intervalo de confianca
t.test(accLR) 
t.test(accSVM) 
t.test(accMNB) 
t.test(accSGD) 

#normalidade
ks.test(accLR, "pnorm", mean(accLR), sd(accLR))
ks.test(accSVM, "pnorm", mean(accSVM), sd(accSVM))
ks.test(accMNB, "pnorm", mean(accMNB), sd(accMNB))
ks.test(accSGD, "pnorm", mean(accSGD), sd(accSGD))

#histograma
hist(accLR)
hist(accSVM)
hist(accMNB)
hist(accSGD)
#hist(h)


#Teste Wilcoxon
t.test(accLR, accSVM, paired = TRUE, alternative = "two.sided")
t.test(accLR, accSGD, paired = TRUE, alternative = "two.sided")
t.test(accSVM, accSGD, paired = TRUE, alternative = "two.sided")

t.test(accLR, accSVM, paired = TRUE, alternative = "greater")
t.test(accLR, accSGD, paired = TRUE, alternative = "greater")
t.test(accSVM, accSGD, paired = TRUE, alternative = "greater")

t.test(accLR, accSVM, paired = TRUE, alternative = "less")
t.test(accLR, accSGD, paired = TRUE, alternative = "less")
t.test(accSVM, accSGD, paired = TRUE, alternative = "less")


n_reps = 30
sample_size = 3
res_list = list()

for (i in 1:30) {
  amostra = sample(accLR, 3, replace = FALSE)
  h.sample = as.data.frame(sample(accLR, sample_size))
  res_list[[i]] = t.test(h.sample, mu=AcuraciaMedia1)
}

library(ggplot2)
#res_list = t.test(Todos_MAE_linear)
dat = data.frame(id=seq(length(res_list)),
                 estimate=sapply(res_list, function(x) x$estimate),
                 conf_int_lower=sapply(res_list, function(x) x$conf.int[1]),
                 conf_int_upper=sapply(res_list, function(x) x$conf.int[2]))

ggplot(data=dat, aes(x=estimate, y=id)) +
  geom_vline(xintercept=AcuraciaMedia1, color="red", linetype=6) +
  geom_point(color="grey30") +
  geom_errorbarh(aes(xmin=conf_int_lower, xmax=conf_int_upper), 
                 color="grey30", height=0.9)+xlab("Intervalo") +   ylab("Amostra")+
  ggtitle("Intervalo  de Confiânça para a média") +theme_bw()
