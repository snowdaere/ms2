#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 08:58:14 2020

authors:
Jared Young
James Wendolek
Haley Kaufell


"""


import numpy as np
import matplotlib.pyplot as plt

inputpath = 'data/'

# save figures or not
save = False
# format of figures
format = 'jpg'

#import variables
lon = np.load(inputpath + "XLONG.npy")
lat = np.load(inputpath + "XLAT.npy")

olr = np.load(inputpath + "OLR.npy")
qrainsfc = np.load(inputpath + "QRAINsfc.npy")
qraincmp = np.load(inputpath + "QRAINcmp.npy")
tinterp = np.load(inputpath + "tInterp.npy")
uwind = np.load(inputpath + 'uInterp.npy')
vwind = np.load(inputpath + 'vInterp.npy')
wwind = np.load(inputpath + 'wInterp.npy')


# define function for taking the distances of each point in a 2d array to an arbitrary point
# takes in a shape, returns array with distances to arbitrary point
def arraydis(shape, center):
    dis = np.zeros(shape)
    for row in range(shape[0]):
        for col in range(shape[1]):
            dis[row][col] = np.sqrt((col - center[0])**2 + (row - center[1])**2)
    return dis


##############################################################
# warning: the following code is abysmally janky. I apologize for long runtime
varlist = [wwind]

# define the dimensions of the plots (to optimize for an arbitrary num of variables)
length = len(varlist)
n = int(np.floor(np.sqrt(length)))
m = int(np.ceil(length / n))

# define the radius of the bins (in gridpoints)
binrad = 6

# find shape of the general data arrays
shape = np.shape(lat)

# initialize figure
plt.figure(figsize=(8, 12))

# create 2d array of distances from a center
dis = arraydis(shape, (144, 146))

# logically index dis based on bins
# round dis down to nearest multiple of six, indexing based n*6
# logical indexing can now be used to mask out the desired
for i in range(shape[0]):
    for j in range(shape[1]):
        value = dis[i][j]
        dis[i][j] = (value - (value % binrad))/binrad
# this populates dis with the bins each gridpoint belongs to


# PLOTTING
for v in range(len(varlist)):

    variable = varlist[v]
    # find height of variable array
    varheight = np.shape(variable)[0]
    # initialize a subplot
    plt.subplot(n, m, v + 1)
    # put values into an array of shape (height, no of bins)
    vals = np.zeros((varheight, int(np.ceil(np.amax(dis)) + 1)))

    # val dim 1 is height
    # val dim 2 is radius
    for bin in range(0, int(np.ceil(np.amax(dis)) + 1)):
        mask = (dis == bin)
        for height in range(varheight):
            # define slice
            slice = variable[height][:][:]
            # apply mask to slice
            slice = np.multiply(slice, mask)
            # remove zeros
            slice[slice == False] = np.NAN
            vals[height][bin] = np.nanmean(slice)

    plt.pcolormesh(vals)

plt.show()
###############################################################