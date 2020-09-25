#####################################################################
## R Code for supervised learning.
## - See lecture: 01-supervised.pdf
## 
## Michael D. Porter
## Created: Oct 2019
## For: Data Mining (SYS-6018) at University of Virginia
## Website: https://mdporter.github.io/SYS6018/
#####################################################################

#-- Load Required Packages
library(tidyverse)
library(FNN)


#--------------------------------------------------------------------#
#-- Generate Data
#--------------------------------------------------------------------#

#-- Settings
n = 100                                 # number of observations
sim_x <- function(n) runif(n)           # U[0,1]
f <- function(x) 1 + 2*x + 5*sin(5*x)   # true mean function
sd = 2                                  # stdev for error
sim_y <- function(x, sd){               # generate Y|X from N{f(x),sd}
  n = length(x)
  f(x) + rnorm(n, sd=sd)             
}

#-- Generate Data
set.seed(825)                           # set seed for reproducibility
x = sim_x(n)                            # get x values
y = sim_y(x, sd=sd)                     # get y values
data_train = tibble(x, y)               # training data tibble

#-- Scatter plot
gg_example = ggplot(data_train, aes(x,y)) +   # a
  geom_point() + 
  geom_vline(xintercept=c(0, .4, .62), col="orange") + 
  scale_x_continuous(breaks=seq(0, 1, by=.20))

gg_example                              # saved base plot for later use

# plot(x, y, las=1)
# grid()
# abline(v=c(0, .40, .62), col="orange")

# My turn #1 ----
#' if x = 0.40, y is about 7 
#' if x = 0, y is about 3
#' if x = 0.62, y is about 2.5
#' We can fit a linear regression, but there seems to be a 
#' curvature pattern




#--------------------------------------------------------------------#
#-- Simple Linear Model
#--------------------------------------------------------------------#

#-- Fitting
m1 = lm(y~x, data=data_train) # fit simple OLS
summary(m1)                   # summary of model

#-- Prediction
xseq = seq(0, 1, length=200)        # sequence of 200 equally spaced values from 0 to 1
xeval = tibble(x = xseq)            # make into a tibble object
yhat1 = predict(m1, newdata=xeval)  # vector of yhat's (predictions)

#-- Plotting
gg_example +                        # re-use base plot
  geom_line(data=tibble(x=xseq, y=yhat1), col="black")  
  # geom_smooth(method="lm")                 # equivalent method

# plot(x, y, las=1)                 # plot data
# lines(xseq, yhat1, col="black")   # add fitted line

# My turn #2 ----
#' The result looks okay, but not very good
#' x new is close to 0.62
#' 
#' model is not complex enough
#' 
#' multiple linear regression, 
#' box-cox transformation on y and log transformation on x

#--------------------------------------------------------------------#
#-- Polynomial Models
#--------------------------------------------------------------------#


# My turn #3 ----
#' matrix transformation
#' beta_hat = (X ^ T \* X) ^ (-1) X ^ T \* y

#-- Fit Quadratic Model
m2 = lm(y~poly(x, degree=2), data=data_train) 
yhat2 = predict(m2, newdata=xeval)  

#- ggplot2 plot
poly.data = tibble(x = xseq, linear=yhat1, quadratic=yhat2) %>%  # long data
  pivot_longer(-x, names_to="model", values_to="y")
gg_example + 
  geom_line(data=poly.data, aes(color=model)) 

#- using geom_smooth() to fit automatically  
gg_example + 
  geom_smooth(method="lm", se=FALSE, aes(color="linear")) + 
  geom_smooth(method="lm", formula="y~poly(x,2)", se=FALSE, aes(color="quadratic")) + 
  scale_color_discrete(name="model")
    
# #- base R plot
# plot(x, y, las=1)                 
# lines(xseq, yhat1, col="black")   
# lines(xseq, yhat2, col="red")
# legend("topright", 
#        c("linear", "quadratic"), 
#        col=c("black", "red"), 
#        lty=1, cex=.8)

# My turn #4 ----
#' X new is close to 0, and 0.62
#' yes, higher adjusted R square, 
#' More complex, lose 1 degree of freedom
#' complexity: number of parameters, 3 parameters, intercept, x and x^2
#' effective degree of freedom
#' Hyper parameter tuning
#' tuning parameter: degree, balance variance and bias
#' 
#' tuning parameter for KNN: k
#' 
#'



#--------------------------------------------------------------------#
#-- kNN regression
#--------------------------------------------------------------------#

# My turn #5 ----
#' if k = N, then the estimate will be the mean of all y
#' y bar, 


library(FNN)                   # For kNN regression

#-- fit a k=20 knn regression
knn.20 = knn.reg(select(data_train, x), test=xeval, y=data_train$y, k=20)

#' when N < k, straight line, which should be a different line
#' potential to create a new function
#' 
#' n / edf = number of data points to fit


#-- ggplot2 plot
gg_example + 
  geom_line(data=tibble(x=xseq, y=knn.20$pred)) + 
  ggtitle("kNN k=20")

#-- base R plot
plot(x, y, las=1) 
lines(xseq, knn.20$pred)

# My turn #6 ----
#' What is the optimal prediction at X = x under the squared
#' error loss?
#' 
#'  Y = c
#' 
#' 
#' 
#' Assume that test and train have the same distribution!!!
#' use the most recent data to train, time series tuning applciations 
#' 
#' expected loss = risk = expected prediction error
#' 
#' R(f)
