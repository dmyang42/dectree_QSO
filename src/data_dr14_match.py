# -*- coding: utf-8 -*-

# 
# match variable source catalog with dr14
# output two ID file for matched stars and quasars
# subsitution of data_add_star.py & data_add_qso.py
# author: snowball and topol @ USTC
# last modified: 2019/3/23
#

from astropy.io import ascii
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np

def _convert_csv_to_coordinates(_csv_file, _ra, _dec):
    #Converters for CSV reading
    converters = {'col1': [ascii.convert_numpy(np.float32)], 'col2': [ascii.convert_numpy(np.float32)]}
    _data = ascii.read(_csv_file, converters=converters)

    for i in range(len(_data)):
        _ra.append(_data['ra'][i])
        _dec.append(_data['dec'][i])
    
def _read_s82varcatalog_coordinates(_ra, _dec, _ID):
    with open('./data/stripe82candidateVar_v1.1.dat') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.split()
            _ID.append(line[0])
            _ra.append(float(line[1]))
            _dec.append(float(line[2]))

def _print_ID(_ID, filename):
    output_file = open(filename, "w+")
    for i in range(len(_ID)):
        print(_ID[i], file=output_file) 

# read csv file(s) of dr14 star
# may take ~ 1 min.
_dr14_star_ra, _dr14_star_dec = [], []
_convert_csv_to_coordinates("./data/pho_star_0_62_mostbill.csv", _dr14_star_ra, _dr14_star_dec)
_convert_csv_to_coordinates("./data/pho_star_306_360_mostbill.csv", _dr14_star_ra, _dr14_star_dec)
print(len(_dr14_star_ra), len(_dr14_star_dec))

# read csv file(s) of dr14 qso
_dr14_qso_ra, _dr14_qso_dec = [], []
_convert_csv_to_coordinates("./data/spec_qso_0_62_mostbill.csv", _dr14_qso_ra, _dr14_qso_dec)
_convert_csv_to_coordinates("./data/spec_qso_306_360_mostbill.csv", _dr14_qso_ra, _dr14_qso_dec)

# read s82 variable source catalog
_var_ra, _var_dec, _var_ID = [], [], []
_read_s82varcatalog_coordinates(_var_ra, _var_dec, _var_ID)
_var_ID = np.array(_var_ID)
print(len(_var_ra), len(_var_dec))

# convert all catalog's coordinates into .SkyCoord format
_dr14_star_coord = SkyCoord(ra=_dr14_star_ra*u.degree, dec=_dr14_star_dec*u.degree)
_dr14_qso_coord = SkyCoord(ra=_dr14_qso_ra*u.degree, dec=_dr14_qso_dec*u.degree)
_var_coord = SkyCoord(ra=_var_ra*u.degree, dec=_var_dec*u.degree)

# set the offset = 2.0 arcsec
constraint = 2.0

# stars matched
# idx is matches index
idx_star, d2d_star, d3d_star = _dr14_star_coord.match_to_catalog_sky(_var_coord)
sep_constraint_star = d2d_star.to(u.arcsec) < (constraint * u.arcsec)
dr14_star_matches = _dr14_star_coord[sep_constraint_star]
var_star_matches = _var_coord[idx_star[sep_constraint_star]]
var_star_matches_ID = _var_ID[idx_star[sep_constraint_star]]

# qsos matched
idx_qso, d2d_qso, d3d_qso = _dr14_qso_coord.match_to_catalog_sky(_var_coord)
sep_constraint_qso = d2d_qso.to(u.arcsec) < (constraint * u.arcsec)
dr14_qso_matches = _dr14_qso_coord[sep_constraint_qso]
var_qso_matches = _var_coord[idx_qso[sep_constraint_qso]]
var_qso_matches_ID = _var_ID[idx_qso[sep_constraint_qso]]

print(len(var_star_matches), len(var_qso_matches))
# _print_ID(var_matches_ID, "./data/dr14_match_star_id")