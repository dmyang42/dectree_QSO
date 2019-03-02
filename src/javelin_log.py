javdata_c = get_data("1000359_washed_r.dat", names=["Red_as_Con"])
#先加载连续谱（这里用r当作连续谱），算出conthpd，用于后面的mcmc
cont = Cont_Model(javdata_c)
cont.do_mcmc(fchain="mychain0.dat")
cont.get_hpd()
conthpd = cont.hpd
#算出来conthpd后开始用pmap模型，接下来是加上一个band再拟合

javdata = get_data(["1000359_washed_r.dat", "1000359_washed_g.dat"], names=["Red_as_Con", "Green"]) 
# 用r作为连续谱，g作为band，套用pmap的反响映射（RM）模型
pmap = Pmap_Model(javdata)
pmap.do_mcmc(conthpd=conthpd, fchain="mychain1.dat")

####接下来的一步写的是"To isolate the peaks ...."，意义存疑，我没试过

pmap.get_hpd()
pmaphpd = pmap.hpd
par_best = pmaphpd[1,:]
print(par_best)
#which shows the median values for log(sigma), log(tau), lag_yelm, width_yelm, scale_yelm, lag_zing, width_zing, and scale_zing, respectively.

javdata_best =  pmap.do_pred(par_best)
javdata_best.plot(set_pred=True, obs=javdata)
#画图


#————————————————my log——————————————————————

>>> javdata = get_data(["1000359_washed_r.dat", "1000359_washed_g.dat"], names=["Red_as_Con", "Green"]) 
>>> pmap = Pmap_Model(javdata)
>>> javdata_c = get_data("1000359_washed_r.dat", names=["Red_as_Con"])
>>> cont = Cont_Model(javdata_c)
>>> cont.do_mcmc(fchain="mychain0.dat")
start burn-in
nburn: 50 nwalkers: 100 --> number of burn-in iterations: 5000
burn-in finished
start sampling
sampling finished
acceptance fractions for all walkers are
0.70 0.66 0.48 0.78 0.64 0.60 0.66 0.54 0.74 0.62 0.72 0.70 0.46 0.50 0.52 0.72 0.64 0.30 0.66 0.60 0.72 0.78 0.64 0.62 0.62 0.54 0.52 0.64 0.54 0.52 0.82 0.62 0.82 0.74 0.78 0.52 0.72 0.62 0.84 0.68 0.70 0.70 0.72 0.70 0.72 0.66 0.54 0.76 0.80 0.68 0.62 0.64 0.68 0.64 0.62 0.60 0.64 0.80 0.58 0.76 0.70 0.60 0.56 0.58 0.76 0.80 0.66 0.66 0.68 0.60 0.78 0.70 0.60 0.68 0.68 0.86 0.50 0.62 0.68 0.68 0.76 0.68 0.66 0.72 0.62 0.52 0.80 0.64 0.74 0.82 0.68 0.76 0.66 0.74 0.52 0.66 0.72 0.68 0.72 0.78
save MCMC chains to mychain0.dat
HPD of sigma
low:    0.055 med    0.062 hig    0.071
HPD of tau
low:    4.363 med    5.311 hig    7.114
>>> cont.get_hpd()
HPD of sigma
low:    0.055 med    0.062 hig    0.071
HPD of tau
low:    4.363 med    5.311 hig    7.114
>>> conthpd = cont.hpd
>>> pmap.do_mcmc(conthpd=conthpd, fchain="mychain1.dat")
run single chain without subdividing matrix 
start burn-in
using priors on sigma and tau from continuum fitting
[[0.055 4.363]
 [0.062 5.311]
 [0.071 7.114]]
penalize lags longer than 0.30 of the baseline
nburn: 100 nwalkers: 100 --> number of burn-in iterations: 10000
burn-in finished
start sampling
sampling finished
acceptance fractions are
0.17 0.29 0.34 0.38 0.06 0.45 0.36 0.23 0.31 0.26 0.39 0.31 0.42 0.36 0.35 0.33 0.12 0.47 0.13 0.41 0.17 0.31 0.30 0.06 0.09 0.31 0.09 0.28 0.47 0.30 0.26 0.30 0.42 0.37 0.29 0.20 0.42 0.35 0.39 0.21 0.19 0.08 0.46 0.16 0.24 0.31 0.39 0.27 0.35 0.37 0.46 0.32 0.12 0.16 0.35 0.19 0.42 0.40 0.40 0.42 0.32 0.31 0.30 0.33 0.35 0.31 0.27 0.33 0.00 0.36 0.48 0.07 0.35 0.05 0.30 0.09 0.52 0.50 0.29 0.11 0.34 0.17 0.22 0.29 0.39 0.05 0.44 0.12 0.05 0.20 0.24 0.10 0.28 0.41 0.34 0.23 0.19 0.27 0.37 0.13
save MCMC chains to mychain1.dat
HPD of sigma
low:    0.065 med    0.070 hig    0.077
HPD of tau
low:    2.744 med    3.213 hig    3.857
HPD of lag_line
low: -1216.359 med   34.474 hig 1511.549
HPD of wid_line
low:    0.619 med    1.890 hig    5.386
HPD of scale_line
low:    0.393 med    0.488 hig    0.614
HPD of alpha
low:    0.906 med    1.018 hig    1.135
>>> pmap.get_hpd()
HPD of sigma
low:    0.065 med    0.070 hig    0.077
HPD of tau
low:    2.744 med    3.213 hig    3.857
HPD of lag_line
low: -1216.359 med   34.474 hig 1511.549
HPD of wid_line
low:    0.619 med    1.890 hig    5.386
HPD of scale_line
low:    0.393 med    0.488 hig    0.614
HPD of alpha
low:    0.906 med    1.018 hig    1.135
>>> pmaphpd = pmap.hpd
>>> par_best = pmaphpd[1,:]
>>> print(par_best)
[-2.654  1.167 34.474  1.89   0.488  1.018]
>>> javdata_best =  pmap.do_pred(par_best)
covariance matrix calculated
covariance matrix decomposed and updated by U
>>> javdata_best.plot(set_pred=True, obs=javdata)
True
>>> 
