#import damask
import numpy as np
import os
import sys

# ##############################################################################
# ## create a folder for this parameter
# read from sys.argv
# sys.argv = ['python3 pre-process.py','h_0_sl_sl','n_sl','xi_0_sl','xi_inf_sl']
C11 = (sys.argv[1])
C12 = (sys.argv[2])
C44 = (sys.argv[3])
#
n    = (sys.argv[4])
adot = (sys.argv[5])
#
# initial hardening modulus
h0   = (sys.argv[6])
# saturation stress
taus = (sys.argv[7])
# initial critical resolved shear stress
tau0 = (sys.argv[8])
# ratio of latent to self-hardening: the same sets
q   = (sys.argv[9])
# ration of laten to self-hardening: different sets
q1  = (sys.argv[10])
# xi_inf_sl = sys.argv[4]
flag_e_q  = (sys.argv[11])

# create myPath to avoid too long folder name using if
if int(flag_e_q) == 0:
    myPath = '../../1_sim_for_iterations/' + \
        'C11_' + str(C11) + \
        '_C12_' + str(C12) + \
        '_C44_' + str(C44)
elif int(flag_e_q) == 1:
    myPath = '../../1_sim_for_iterations/' + \
        'n_' + str(n) + \
        '_adot_' + str(adot) + \
        '_h0_' + str(h0) + \
        '_taus_' + str(taus) + \
        '_tau0_' + str(tau0) + \
        '_q_' + str(q) + \
        '_q1_' + str(q1)
else:
    sys.exit("check flag_e_q!!!!!!!!")
            

# myPath = '../../1_sim_for_iterations/' + \
#     'C11_' + str(C11) + \
#     '_C12_' + str(C12) + \
#     '_C44_' + str(C44)
try:
    if not os.path.isdir(myPath):
        os.mkdir(myPath)
except OSError:
    print("Cannot create the following directory: %s" % myPath)
else:
    print("Successfully created the directory %s " % myPath)


# ##############################################################################
# copy files in the ./1_abaqus_related/input_file/* into the just created folder
cp_cmd = 'cp -r ../1_abaqus_related/abaqus_damage_latest_version/1_input_files/*'\
    + ' ' + myPath
os.system(cp_cmd)
