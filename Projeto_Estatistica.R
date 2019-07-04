require(caret)
require(MASS)

setwd("C:\\Users\\apaf.lincs-PC\\Desktop\\Projeto-Estatistica-Cins")
exe1 <- read.csv("exp01.csv", header = TRUE, sep = ";")
exe3 <- read.csv("exp03.csv", header = TRUE, sep = ";")
exe4 <- read.csv("exp04.csv", header = TRUE, sep = ";")
exe2 <- read.csv("exp02.csv", header = TRUE, sep = ";")

#1=LOGISTICA
#2=SVM
#3=MultinomialNB
#4=SGD

acuracia1 = exe1$accuracy
acuracia3 = exe3$accuracy
acuracia4 = exe4$accuracy
acuracia2 = exe2$accuracy

precisao1 = exe1$precision
precisao3 = exe3$precision
precisao4 = exe4$precision
precisao2 = exe2$precision
  
Recall1 = exe1$recall
Recall3 = exe3$recall
Recall4 = exe4$recall
Recall2 = exe2$recall

AcuraciaMedia1=mean(acuracia1)
AcuraciaDesvio1=sd(acuracia1)

AcuraciaMedia5=mean(acuracia2)
AcuraciaDesvio5=sd(acuracia2)

AcuraciaMedia3=mean(acuracia3)
AcuraciaDesvio3=sd(acuracia3)

AcuraciaMedia4=mean(acuracia4)
AcuraciaDesvio4=sd(acuracia4)

#intervalo de confianca
t.test(acuracia1) 
t.test(acuracia2) 
t.test(acuracia3) 
t.test(acuracia4) 

#normalidade
ks.test(acuracia1,'pnorm')
ks.test(acuracia2,'pnorm')
ks.test(acuracia3,'pnorm')
ks.test(acuracia4,'pnorm')

#histograma
hist(acuracia1)
hist(acuracia2)
hist(acuracia3)
hist(acuracia4)
#hist(h)

hist(acuracia1)
hist(acuracia2)
hist(acuracia4)

#Teste Wilcoxon
wilcox.test(acuracia1,acuracia2, alternative = 'two.sided', paired = T) 
wilcox.test(acuracia1,acuracia4, alternative = 'two.sided', paired = T) 
wilcox.test(acuracia2,acuracia4, alternative = 'two.sided', paired = T) 

wilcox.test(acuracia4,acuracia1, alternative = 'less', paired = T) 
wilcox.test(acuracia4,acuracia2, alternative = 'less', paired = T) 
wilcox.test(acuracia2,acuracia1, alternative = 'less', paired = T) 

wilcox.test(acuracia4,acuracia1, alternative = 'greater', paired = T) 
wilcox.test(acuracia4,acuracia2, alternative = 'greater', paired = T) 
wilcox.test(acuracia2,acuracia1, alternative = 'greater', paired = T)



n_reps = 30
sample_size = 3
res_list = list()

for (i in 1:30) {
  amostra = sample(acuracia1, 3, replace = FALSE)
  h.sample = as.data.frame(sample(acuracia1, sample_size))
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
