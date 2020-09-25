library(h2o)
library(tidyverse)

train <- read_csv("https://mdporter.github.io/SYS6018/data/linkage_train.csv")
test <- read_csv("https://mdporter.github.io/SYS6018/data/linkage_test.csv")



h2o.init()

train$y <- as.factor(train$y)

model <- h2o.randomForest(x = colnames(train %>% select(-y)),
                          y = 'y',
                          training_frame = as.h2o(train),
                          stopping_metric = 'logloss',
                          stopping_rounds = 10,
                          nfolds = 10,
                          seed = 666)




pred <- h2o.predict(model, newdata = as.h2o(test)) %>% 
  as.data.frame()

h2o.confusionMatrix(model)

h2o.shutdown(prompt = F)



library(xgboost)

