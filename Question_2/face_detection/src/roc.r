data <- read.csv('result/tp_fp.csv', header=T, sep=',')
y = array(data$tp)
x = data$fp
y = sort(y)
x = sort(x)


xx <- seq(0, 1, length=50)
fit <- lm(y~poly(x, 3, raw=TRUE))
plot(x, y, xlab='FP', ylab='TP', xlim=c(0, 1), ylim=c(0, 1), las=1, main='ROC curve')
lines(xx, predict(fit, data.frame(x=xx)), col='red')

dev.copy(png, filename='result/roc.png')
dev.off()
