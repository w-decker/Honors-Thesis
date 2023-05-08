# simulating timeseries

v1 <- rnorm(300)
v2 <- rnorm(300)
v3 <- rnorm(300)
v4 <- rnorm(300)

# create correlations

v1v2 <- v1[1:100] + v2 
v2v3 <- v2[1:100] + v3
v3v4 <- v3[1:100] + v4


