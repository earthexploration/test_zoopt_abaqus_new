#!/bin/bash
# to set number of threads
export OMP_NUM_THREADS=16
# to generate
neper -T -dim 3 -n 100 -domain "cube(2,3,5)" -morpho "diameq:lognormal(1,0.05),1-sphericity:lognormal(0.145,0.03)"
# to visualize
neper -V n100-id1.tess -print img1
