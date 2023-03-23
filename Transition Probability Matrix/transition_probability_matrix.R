## Load libraries

library(dplyr)
library(tidyr)
library(tibble)


## Create structured transition matrix

# initialize matrix
w <- expand_grid(word = 1:4, syl = 1:3) %>% unite(label, word, syl, sep = "_")
X <- matrix(0, nrow = nrow(w), ncol = nrow(w), dimnames = list(w$label, w$label))

X["1_1", "1_2"] <- 1
X["1_2", "1_3"] <- 1
X["1_3", "1_1"] <- .25
X["1_3", "2_1"] <- .25
X["1_3", "3_1"] <- .25
X["1_3", "4_1"] <- .25

X["2_1", "2_2"] <- 1
X["2_2", "2_3"] <- 1
X["2_3", "2_1"] <- .25
X["2_3", "1_1"] <- .25
X["2_3", "3_1"] <- .25
X["2_3", "4_1"] <- .25

X["3_1", "3_2"] <- 1
X["3_2", "3_3"] <- 1
X["3_3", "3_1"] <- .25
X["3_3", "1_1"] <- .25
X["3_3", "2_1"] <- .25
X["3_3", "4_1"] <- .25

X["4_1", "4_2"] <- 1
X["4_2", "4_3"] <- 1
X["4_3", "4_1"] <- .25
X["4_3", "1_1"] <- .25
X["4_3", "2_1"] <- .25
X["4_3", "3_1"] <- .25

X


## Structured Transition Probability Matrix

# Simulate sequence
n <- 32 # number of trials
rand_seq <- numeric(n)
cur <- sample(nrow(X), size = 1)
rand_seq[1] <- cur

for (i in 2:length(rand_seq)) {
  cur <- sample(nrow(X), size = 1, prob = X[cur, ])
  rand_seq[i] <- cur
}

# Summarize sequence
ecountS <- table(rand_seq[1:(n - 1)], rand_seq[2:n]) # empirical count of transitions
dmatS <- diag(1 / rowSums(ecountS))
eprobS <- dmatS %*% ecountS # empirical transitional probabilities

eprobS

## Un-structured Transition Probability Matrix

# Define transition matrix
Rtransition <- matrix(0.083, nrow = 4, ncol = 4)
diag(Rtransition) <- 0.0

# Simulate sequence
n <- 32 # number of trials
rand_seq <- numeric(n)
cur <- sample(nrow(Rtransition), size = 1)
rand_seq[1] <- cur

for (i in 2:length(rand_seq)) {
  cur <- sample(nrow(Rtransition), size = 1, prob = Rtransition[cur, ])
  rand_seq[i] <- cur
}

# Summarize sequence
ecountR <- table(rand_seq[1:(n - 1)], rand_seq[2:n]) # empirical count of transitions
dmatR <- diag(1 / rowSums(ecountR))
eprobR <- dmatR %*% ecountR # empirical transitional probabilities
