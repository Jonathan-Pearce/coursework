## ----setup, include=FALSE------------------------------------------------
knitr::opts_chunk$set(echo = TRUE)
options(scipen=2)

## ------------------------------------------------------------------------
library(MASS)
file1<-"http://www.math.mcgill.ca/yyang/regression/data/salary.csv"
#code from assginment document
salary<-read.csv(file1,header=TRUE)
x1<-salary$SPENDING/1000
y<-salary$SALARY
fit.Salary<-lm(y~x1)
sum<-summary(fit.Salary)
#sum

## ----a_1-----------------------------------------------------------------
n <- length(x1)
p <- 2

intercept = 0
intercept = (1/(sum(x1^2) - (1/n)*(sum(x1)^2))) * (mean(y)*(sum(x1^2)) - mean(x1)*sum(x1*y))
intercept

## ----a_2-----------------------------------------------------------------
slope = 0
slope = (1/(sum(x1^2) - (1/n)*(sum(x1)^2))) * (sum(x1*y) - sum(x1)*sum(y)/n)
slope

## ----b-------------------------------------------------------------------
ssresidual = sum((y - (intercept + slope*x1))^2)
meanSqError = ssresidual/(n-p)
resStandError = sqrt(meanSqError)
resStandError

## ----c_1-----------------------------------------------------------------
stdError = sum$coefficients[[1]]/sum$coefficients[[5]]
stdError

## ----c_2-----------------------------------------------------------------
var = ssresidual/(n-2)
sxx = sum((x1 - mean(x1))^2)

stdErrorData = sqrt(var * (1/n + (mean(x1)^2)/sxx))
stdErrorData

## ----d-------------------------------------------------------------------
ssr = sum((mean(y) - (intercept + slope*x1))^2)
sst = sum((y - mean(y))^2)

rsq = ssr/sst
rsq

## ------------------------------------------------------------------------
#from previous question
print(ssr, digits = 14) 

## ------------------------------------------------------------------------
#verification: product of slope estimate and s_xy
sxy = sum((y - mean(y))*(x1 - mean(x1)))
ssr_2 = sxy * slope
print(ssr_2, digits = 14)

## ----f-------------------------------------------------------------------
F = (ssr/(p-1))/(ssresidual/(n-p))
F

## ------------------------------------------------------------------------
one = matrix( rep(1, len=n), ncol = 1)
H1 = (1/n)*(one %*% t(one))

sum(diag(diag(n)-H1))


## ------------------------------------------------------------------------
colOne = matrix( rep(1, len=n), ncol = 1)
colTwo = data.matrix(x1, rownames.force = NA)
xMatrix = cbind(colOne, x1)

H = xMatrix %*% ginv(t(xMatrix) %*% xMatrix) %*% t(xMatrix)

sum(diag(H-H1))

## ------------------------------------------------------------------------
fitted = intercept + x1*slope
res = y - fitted
plot(x1,res,abline(h=0,lty=2))
title('Residual vs. X1')

## ------------------------------------------------------------------------
plot(fitted,res,abline(h=0,lty=2))
title('Residual vs. Predicted Y')

## ----h-------------------------------------------------------------------
#part 1
t(one)  %*%  res

#part 2
t(xMatrix) %*% res

#part 3
t(fitted) %*% res

## ----i-------------------------------------------------------------------
yHatOne = intercept + (4800/1000)*slope
yHatOne

## ----j-------------------------------------------------------------------
x1New<-matrix(c(1,4.8),nrow=1)

stdErrorYNew = sqrt(var * x1New %*% (ginv(t(xMatrix) %*% xMatrix)) %*% t(x1New))
stdErrorYNew

