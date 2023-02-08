# convert st12 from Gauss point to node
# extract st12 of the center node
# extract u1 on top right node
# write (u1,st12) into file 
from abaqusConstants import *
from odbAccess import *
from array import array
import sys, getopt

########################################################################
#convert st12 from Gauss point to node
########################################################################
odbPath="example_rp.odb"
odb=openOdb(path=odbPath,readOnly=FALSE)

# rp node
rp_Node = odb.rootAssembly.nodeSets['DISP-LOAD']

# time
# odb.steps['Step-1'].historyRegions['Node ASSEMBLY.1'].historyOutputs['U2'].data[x][0]
# disp
# odb.steps['Step-1'].historyRegions['Node ASSEMBLY.1'].historyOutputs['U2'].data[x][1]



file = open("disp-load-rp.txt","w")
file.write('#disp    load'+'\n')

lastStepPeriod = 0.0

for stepName in odb.steps.keys():
    # for multiple frames
    step = odb.steps[stepName]
    # historyUutput for U2
    # rp_historyOutput = (data0(time,u2),data1(time,u2),...data_n(time,u2))
    rp_u3_historyOutput   = step.historyRegions['Node PART-1-1.11881'].historyOutputs['U3'].data
    rp_rf3_historyOutput = step.historyRegions['Node PART-1-1.11881'].historyOutputs['RF3'].data

    # loop to get displacement and rf2
    this_disp  = []
    this_force = []

    if hasattr(rp_u3_historyOutput,"__iter__"):
        for index, item in enumerate(rp_u3_historyOutput):
            this_disp.append(item[1])
        #print("")
    else:
        #print("")
        this_disp.append("0.0")
    if hasattr(rp_rf3_historyOutput,"__iter__"):
        for index, item in enumerate(rp_rf3_historyOutput):
            this_force.append(item[1])
    else:
        this_force.append("1.e9")

    # for index, item in enumerate(rp_u3_historyOutput):
    #     this_disp.append(item[1])
    # for index, item in enumerate(rp_rf3_historyOutput):
    #     this_force.append(item[1])

    for i in range(len(this_disp)):
        file.write(str(this_disp[i])+ ' '+ str(this_force[i]) + '\n')


file.close()
odb.close()
