import sys
import numpy as np

filename = sys.argv[1]

colors = ['r', 'i', 'u', 'z', 'g']

with open('./data/light_curve/' + filename) as f:
	lines = f.readlines()

	atbss = []

	atbs_r = []
	atbs_i = []
	atbs_u = []
	atbs_z = []
	atbs_g = []

	atbss.append(atbs_r)
	atbss.append(atbs_i)
	atbss.append(atbs_u)
	atbss.append(atbs_z)
	atbss.append(atbs_g)

	count = 0

	for line in lines:
		atb=[]
		line = line.split()

		try:
			atb.append(float(line[0]))
			atb.append(float(line[2]))
			atb.append(float(line[3]))
		except:
			count = count + 1
			if count == 5:
				count = 0
			continue

		atbss[count].append(atb)

		count = count + 1
		if count == 5:
			count = 0

for j in range(0, 5):

	color = colors[j]

	with open(filename + str(color) + '.dat', 'w+') as ff:
		for i in range(len(atbss[j])):
			print >>ff, atbss[j][i][0], atbss[j][i][1], atbss[j][i][2]



