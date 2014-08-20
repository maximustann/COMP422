data_classifier_1 = read.csv('result/classifier_1/tp_fp.csv', header=T, sep=',')
data_classifier_2 = read.csv('result/classifier_2/tp_fp.csv', header=T, sep=',')
y1 = array(data_classifier_1$tp)
x1 = data_classifier_1$fp
y1 = sort(y1)
x1 = sort(x1)


y2 = array(data_classifier_2$tp)
x2 = data_classifier_2$fp
y2 = sort(y2)
x2 = sort(x2)

xx = seq(0, 1, length=50)
xl = seq(0, 1, length=50)

lo = loess(y1~x1)
loo = loess(y2~x2)

fit = lm(y1~poly(x1, 3, raw=TRUE))
fit2 = lm(y2~poly(x2, 3, raw=TRUE))
png(filename='result/roc.png')
plot(x1, y1, xlab='FP', ylab='TP', xlim=c(0, 1), ylim=c(0, 1), las=1, main='ROC curve', col='red')
lines(xx, predict(fit, data.frame(x1 = xx)), col="red")
par(new=TRUE)
plot(x2, y2, xlab='FP', ylab='TP', xlim=c(0, 1), ylim=c(0, 1), las=1, main='ROC curve', col='green')
lines(xl, predict(fit2, data.frame(x2 = xl)), col="green")
dev.off()
