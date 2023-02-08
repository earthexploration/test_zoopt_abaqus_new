#!/bin/bash
# to set nubmer of threads
export OMP_NUM_THREADS=16
neper -M ./n100-id1.tess -elttype hex
neper -M ./n100-id1.tess -elttype hex -format inp
neper -V n100-id1.tess,n100-id1.msh -print thisMesh
