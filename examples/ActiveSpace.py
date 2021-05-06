#! /usr/bin/env python
import macrodensity as md
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from itertools import izip




#------------------------------------------------------------------
# Get the potential
# This section should not be altered
#------------------------------------------------------------------
vasp_pot, NGX, NGY, NGZ, Lattice = md.read_vasp_density('LOCPOT.slab')
vector_a,vector_b,vector_c,av,bv,cv = md.matrix_2_abc(Lattice)
resolution_x = vector_a/NGX
resolution_y = vector_b/NGY
resolution_z = vector_c/NGZ
grid_pot, electrons = md.density_2_grid(vasp_pot,NGX,NGY,NGZ)
cutoff_varience = 1E-4
hanksConstant = 4.89E-7
## Get the gradiens (Field), if required.
## Comment out if not required, due to compuational expense.
#grad_x,grad_y,grad_z = np.gradient(grid_pot[:,:,:],resolution_x,resolution_y,resolution_z)
#------------------------------------------------------------------


##------------------------------------------------------------------
## Get the equation for the plane
## This is the section for plotting on a user defined plane; 
## uncomment commands if this is the option that you want.
##------------------------------------------------------------------
## Input section (define the plane with 3 points)
#a_point = [0, 0, 0]
#b_point = [1, 0, 1]
#c_point = [0, 1, 0]

## Convert the fractional points to grid points on the density surface
#a = pot.numbers_2_grid(a_point,NGX,NGY,NGZ)
#b = pot.numbers_2_grid(b_point,NGX,NGY,NGZ)
#c = pot.numbers_2_grid(c_point,NGX,NGY,NGZ)
#plane_coeff = pot.points_2_plane(a,b,c)

## Get the gradients
#XY = np.multiply(grad_x,grad_y)
#grad_mag = np.multiply(XY,grad_z)

## Create the plane
#xx,yy,grd =  pot.create_plotting_mesh(NGX,NGY,NGZ,plane_coeff,grad_x)
## Plot the surface
#plt.contourf(xx,yy,grd,V)
#plt.show()
##------------------------------------------------------------------
##------------------------------------------------------------------

##------------------------------------------------------------------
## Plotting a planar average (Field/potential) throughout the material
##------------------------------------------------------------------
## FIELDS
#planar = pot.planar_average(grad_x,NGX,NGY,NGZ)
## POTENTIAL
#planar = pot.planar_average(grid_pot,NGX,NGY,NGZ)
## MACROSCOPIC AVERAGE
#macro  = pot.macroscopic_average(planar,4.80,resolution_z)
#plt.plot(planar)
#plt.plot(macro)
#plt.savefig('Planar.eps')
#plt.show()
##------------------------------------------------------------------
##------------------------------------------------------------------

##------------------------------------------------------------------
# Getting the average potential in a single cube of arbitrary size
##------------------------------------------------------------------
## cube defines the size of the cube in units of mesh points (NGX/Y/Z)
cube = [2,2,2]
## origin defines the bottom left point of the cube the "0,0,0" point in fractional coordinates
origin = [0,0,0]
## Uncomment the lines below to do the business
vacuum = []
non_vacuum = []
beers = hanksConstant*NGX*NGY*NGZ
pinners = beers*1.5
print "You have time for %.1f oz of beer "%beers
print "... or %.1f oz of Pinner (TM)."%pinners
for i in range(0,NGX,cube[0]):
    print float(i)/NGX
    for j in range(0,NGY,cube[1]):
	for k in range(0,NGZ,cube[2]):
	    origin = [float(i)/NGX,float(j)/NGY,float(k)/NGZ]
            volume_average, cube_var = md.voulme_average(origin, cube, grid_pot, NGX, NGY, NGZ)
	    if cube_var <= cutoff_varience:
		vacuum.append(origin)
	    else:
		non_vacuum.append(origin)
print "Number of vacuum cubes: ", len(vacuum)
print "Number of non-vacuum cubes: ", len(non_vacuum)

print "Percentage of vacuum cubes: ",(float(len(vacuum))/(float(len(vacuum))+float(len(non_vacuum)))*100.)
print "Percentage of non-vacuum cubes: ",(float(len(non_vacuum))/(float(len(vacuum))+float(len(non_vacuum)))*100.)
