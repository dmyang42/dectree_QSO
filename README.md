# dectree_QSO
decision tree for selecting Quasar using photometric and variation information

pre-requsite: JAVELIN

step1: Download Stripe82 Variable Source Catalog from http://faculty.washington.edu/ivezic/sdss/catalogs/S82variables.html

step2: Wash raw data with `data_wash.py` and `data_wash.sh` to generate washed light curve data

step3: Use `python data_generate.py` to generate training data from washed light curve data(in python2 env)

step4: Use `python data_organize.py 0` or `python data_organize.py 1` to organize generated data(in python3 env)
- mode 0 - spec-confirmed star to form nQSO
- mode 1 - i < 19.0 to form nQSO

step4: Use `python dectree.py 0 3` or `python dectree.py 1 3` to train decision tree model(in python3 env), 3 represents a random seed
