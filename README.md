# dectree_QSO
decision tree for selecting Quasar using photometric and variation information

pre-requsite: JAVELIN

step1: Download Stripe82 Variable Source Catalog from http://faculty.washington.edu/ivezic/sdss/catalogs/S82variables.html

step2: Wash raw data with `wash.py` and `wash.sh` to generate washed light curve data

step3: Use `python gen_data.py` to generate training data from washed light curve data(in python2 env)

step4: Use `python dectree.py` to train decision tree model(in python3 env)
