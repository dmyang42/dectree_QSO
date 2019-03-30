# -*- coding: utf-8 -*-

# 
# This is the script to generate a list of spectroscopic confirmed stars-
# -by s82 standard stars catalog(Ivezic): http://faculty.washington.edu/ivezic/sdss/catalogs/stripe82.html
# !-- NOTICE: this catalog has a bias, thus applying it directly to training procedure may leads to lower precision
# author: topol @ USTC
# last modified: 2019/3/21
#
from astropy.io import fits

star_fits = fits.open('./data/s82_spec_star.fits')
star_data = star_fits[1].data
with open('./data/stripe82candidateVar_v1.1.dat') as f:
    lines = f.readlines()
    ID, ra, dec, MiQSO = [], [], [], []
    for line in lines[1:]:
        line = line.split()
        ID.append(line[0]) # this ID is not sdssID!
        ra.append(float(line[1]))
        dec.append(float(line[2]))
        MiQSO.append(float(line[16])) # as label

for i in range(len(MiQSO)):
    if -0.0001 < MiQSO[i] + 9.9 < 0.0001:
        MiQSO[i] = 0 # not sure if quasar
    else:
        MiQSO[i] = 1 # is quasar

nq_id = ID
nq_ra = [round(i,2) for i in ra]
nq_dec = [round(i,2) for i in dec]
q_ra = [round(i,2) for i in star_data['ra']]
q_dec = [round(i,2) for i in star_data['dec']]
l1 = list(zip(nq_ra, nq_dec, nq_id, MiQSO))
l2 = list(zip(q_ra, q_dec))

count = 0
outfile = open("./data/additional_confirmed_star", "w+")
for nq in l1:
    if nq[3] is 0: # not sure if quasar in s82var catalog
        for q in l2: 
            if nq[0] == q[0] and nq[1] == q[1]: # confirmed in s82stdstar catalog
                count = count + 1
                print(nq[2], file=outfile)
                break
print(count)