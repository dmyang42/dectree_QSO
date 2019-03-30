# -*- coding: utf-8 -*-

# 
# This is the script to generate a list of spectroscopic confirmed quasars-
# -by sdss dr7 quasar catalog: http://classic.sdss.org/dr7/products/value_added/qsocat_dr7.html
# Combining this catalog to those uncertain variable source in s82var catalog-
# -we can obtain more quasar sample
# author: topol @ USTC
# last modified: 2019/3/21
#
from astropy.io import fits

qso_fits = fits.open('./data/s82_spec_qso.fits')
qso_data = qso_fits[1].data
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
q_ra = [round(i,2) for i in qso_data['ra']]
q_dec = [round(i,2) for i in qso_data['dec']]
l1 = list(zip(nq_ra, nq_dec, nq_id, MiQSO))
l2 = list(zip(q_ra,q_dec))

count = 0
outfile = open("./data/additional_confirmed_quasar", "w+")
for nq in l1:
    if nq[3] is 0: # not sure if quasar
        for q in l2:
            if nq[0] == q[0] and nq[1] == q[1]: # confirmed by dr7 quasar catalog
                count = count + 1
                print(nq[2], file=outfile)
                break
print(count)