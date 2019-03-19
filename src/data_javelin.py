#!/usr/local/bin/python2
# -*- coding: utf-8 -*-

#
# fitting light curve with JAVELIN
# (https://bitbucket.org/nye17/javelin/overview author: Ying Zu @ SJTU)
# return fitting parameters tau and sigma in five photometric bands
# author: topol @ USTC
# last modified: 2019/3/19
#

from javelin.zylc import get_data
from javelin.lcmodel import Cont_Model
from numpy import exp

def javelin_fit(ID):
    # 对ugriz五个band分别跑javelin连续谱模型拟合
    # 得到五个拟合结果
    band_pho = ['u', 'g', 'r', 'i', 'z']
    tau_pho = [] # in ugriz order
    sigma_pho = [] # in ugriz order
    for band in band_pho:
        filename = "./data/light_curve/" + band + \
            "_LC_" + ID + ".dat"
        # JAVELIN
        c = get_data([filename])
        cmod = Cont_Model(c)
        cmod.do_mcmc(threads=4)
        
        # 这里只记录了med的结果:

        # tau_mc_low = exp(cmod.hpd[0,1])
        tau_mc_med = exp(cmod.hpd[1,1])
        # tau_mc_hig = exp(cmod.hpd[2,1])
        
        # sigma_mc_low = exp(cmod.hpd[0,0])
        sigma_mc_med = exp(cmod.hpd[1,0])
        # sigma_mc_hig = exp(cmod.hpd[2,0])
        
        tau_pho.append(tau_mc_med)
        sigma_pho.append(sigma_mc_med)
    
    # 返回五个tau,sigma
    # 顺序是urgriz
    return tau_pho, sigma_pho