# dectree_QSO
decision tree for selecting Quasar using photometric and variation information

pre-requsite: JAVELIN

step1: Download Stripe82 Variable Source Catalog from http://faculty.washington.edu/ivezic/sdss/catalogs/S82variables.html

step2: Wash raw data with `data_wash.py` and `data_wash.sh` to generate washed light curve data

step3: Use `python data_generate.py` to generate training data from washed light curve data(in python2 env)

step4: Use `python data_organize.py 3` or `python data_organize.py 4` to organize generated data(in python3 env)
- mode 0 - spec-confirmed star to form nQSO(作废)
- mode 1 - i < 19.0 for nQSO(作废)
- mode 2 - use pho_data of dr14 to form nQSO(作废)
- mode 3 - i < 19.0 for all sources
- mode 4 - all spec confirmed

step4: Use `python dectree.py --data-mode=3 --feature-mode=all --random-seed=3` to train decision tree model(in python3 env)
- --data-mode : 0, 1, 2, 3, 4 as in step4
- --feature-mode : all for all features / color for color features only / variability for variability features only
- --random-seed : int 
