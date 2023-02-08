#
#
import glob
import re
import sys

initialIncSize = sys.argv[1]
totalTime = sys.argv[2]
minIncSize = sys.argv[3]
maxIncSize = sys.argv[4]
dispZ = sys.argv[5]
frequency = sys.argv[6]

inpFile = open("example.inp","w")

# ######################################################################
# write inp head  information
inpFile.write("""*Heading
*Preprint, echo=NO, model=NO, history=NO, contact=NO
** *****************************************************************
** PARTS
** *****************************************************************
** always use the default name: Part-1
**
*Part, name=Part-1
**
""")

# ######################################################################
# write Node information
inpFile.write("""** **********************************************
** Node information will be read from the following file
** **********************************************
*Include, input=./extractNeperInp/nodeInfo.txt
**
""")
# write reference point
inpFile.write("""
** to declare the RP node
**
11881, 0.0,  0.0,  15.0
""")

# ######################################################################
# write Element information
inpFile.write("""** ***********************************************
** Element information will be read from the following file
** **********************************************
*Include, input=./extractNeperInp/elementInfo.txt
**
""")

# ######################################################################
# write Elset information, i.e., Grain information
inpFile.write("""** **********************************************
** list all element sets for each grains and create sections
** for material assignments
** **********************************************
""")
# to find all elset txt files
currentPath = './extractNeperInp'
elsetList = []
for files in glob.glob(currentPath + '/*elset_*'):
    # print(files)
    elsetList.append(files)
   # print(type(files))
#print(elsetList)
# create a file to store the numbering of poly set
polySetFile = open("./extractNeperInp/poly_sets_numbering.txt","w")
for elsetFileDir in elsetList:
   # print(elsetFileDir)
   # print(re.findall(r'\d+', elsetFileDir))
    numList = re.findall(r'\d+', elsetFileDir)
    # store this into a file for future use
    polySetFile.write(str(numList[0])+"\n")
    # print(numList[0]) # give a number
    inpFile.write("""**Grain """ + str(numList[0])  + """
""")
    inpFile.write("""**
*Include, input=""" + elsetFileDir+"""
""")
    # not a general method
    inpFile.write("""*Solid Section, elset=poly"""+ str(numList[0])
                  +""",controls=EC-1,material=Properties_poly"""+str(numList[0])
                  +"""
""")
    inpFile.write("""**
""")
# write end part
inpFile.write("""**
*End Part
""")

# ######################################################################
#  write Assembly information
inpFile.write("""** *****************************************************************
** ASSEMBLY
** *****************************************************************
*Assembly, name=Assembly
**  
*Instance, name=Part-1-1, part=Part-1
*End Instance
**
""")
## list all node set in Assembly
inpFile.write("""**
** list all node sets here by reading from the neper file
**
""")
# to store nset dir
nsetList = []
for files in glob.glob(currentPath + '/*nset_*'):
    nsetList.append(files)
# to add all nset
for nsetFileDir in nsetList:
    inpFile.write("""**
*Include, input=""" + nsetFileDir+"""
""")
# to declare node set for RP
inpFile.write("""**
** to delcare node set for RP
**
*Nset, nset=disp-load,instance=Part-1-1
11881,
**
** to declare element set and surface set for coupling
** the elset should be z1
*Nset, nset=_s_Surf-3_S2, instance=Part-1-1
11551, 11552, 11553, 11554, 11555, 11556, 11557, 11558, 11559, 11560,
11561, 11562, 11563, 11564, 11565, 11566, 11567, 11568, 11569, 11570,
11571, 11572, 11573, 11574, 11575, 11576, 11577, 11578, 11579, 11580,
11581, 11582, 11583, 11584, 11585, 11586, 11587, 11588, 11589, 11590,
11591, 11592, 11593, 11594, 11595, 11596, 11597, 11598, 11599, 11600,
11601, 11602, 11603, 11604, 11605, 11606, 11607, 11608, 11609, 11610,
11611, 11612, 11613, 11614, 11615, 11616, 11617, 11618, 11619, 11620,
11621, 11622, 11623, 11624, 11625, 11626, 11627, 11628, 11629, 11630,
11631, 11632, 11633, 11634, 11635, 11636, 11637, 11638, 11639, 11640,
11641, 11642, 11643, 11644, 11645, 11646, 11647, 11648, 11649, 11650,
11651, 11652, 11653, 11654, 11655, 11656, 11657, 11658, 11659, 11660,
11661, 11662, 11663, 11664, 11665, 11666, 11667, 11668, 11669, 11670,
11671, 11672, 11673, 11674, 11675, 11676, 11677, 11678, 11679, 11680,
11681, 11682, 11683, 11684, 11685, 11686, 11687, 11688, 11689, 11690,
11691, 11692, 11693, 11694, 11695, 11696, 11697, 11698, 11699, 11700,
11701, 11702, 11703, 11704, 11705, 11706, 11707, 11708, 11709, 11710,
11711, 11712, 11713, 11714, 11715, 11716, 11717, 11718, 11719, 11720,
11721, 11722, 11723, 11724, 11725, 11726, 11727, 11728, 11729, 11730,
11731, 11732, 11733, 11734, 11735, 11736, 11737, 11738, 11739, 11740,
11741, 11742, 11743, 11744, 11745, 11746, 11747, 11748, 11749, 11750,
11751, 11752, 11753, 11754, 11755, 11756, 11757, 11758, 11759, 11760,
11761, 11762, 11763, 11764, 11765, 11766, 11767, 11768, 11769, 11770,
11771, 11772, 11773, 11774, 11775, 11776, 11777, 11778, 11779, 11780,
11781, 11782, 11783, 11784, 11785, 11786, 11787, 11788, 11789, 11790,
11791, 11792, 11793, 11794, 11795, 11796, 11797, 11798, 11799, 11800,
11801, 11802, 11803, 11804, 11805, 11806, 11807, 11808, 11809, 11810,
11811, 11812, 11813, 11814, 11815, 11816, 11817, 11818, 11819, 11820,
11821, 11822, 11823, 11824, 11825, 11826, 11827, 11828, 11829, 11830,
11831, 11832, 11833, 11834, 11835, 11836, 11837, 11838, 11839, 11840,
11841, 11842, 11843, 11844, 11845, 11846, 11847, 11848, 11849, 11850,
11851, 11852, 11853, 11854, 11855, 11856, 11857, 11858, 11859, 11860,
11861, 11862, 11863, 11864, 11865, 11866, 11867, 11868, 11869, 11870,
11871, 11872, 11873, 11874, 11875, 11876, 11877, 11878, 11879, 11880
**
** create surface
*Surface, type=NODE, name=s_Surf-3, internal
_s_Surf-3_S2, 1
**
** to add constraint coupling
**
** Constraint: Constraint-1
*Coupling, constraint name=Constraint-1, ref node=disp-load, surface=s_Surf-3
*Kinematic
**
""")
# to write ende assembly
inpFile.write("""**
*End Assembly
**
** ELEMENT CONTROLS
**
*Section Controls, name=EC-1, ELEMENT DELETION=YES
1., 1., 1.
""")

# ######################################################################
# write Materials information
inpFile.write("""** *****************************************************************
** MATERIALS
** *****************************************************************
""")
# elsetlist will be reused
# loop elsetlist to set properties for each set such as the form:
# **
# *Material, name=material_poly1
# *Include, input=./Properties_poly1.inc
# **
#
propDir = "./extractNeperInp/"
for elsetFileDir in elsetList:
   # print(elsetFileDir)
   # print(re.findall(r'\d+', elsetFileDir))
    numList = re.findall(r'\d+', elsetFileDir)
    # print(numList[0]) # give a number
    inpFile.write("""**Grain """ + str(numList[0])  +
                  """ material properties
""")
    inpFile.write("""*Material, name=Properties_poly"""+
                  str(numList[0])
                  +"""
""")
    inpFile.write("""*Include, input=""" +propDir+
                  """Properties_poly"""+str(numList[0]) +
                  """.inc
""")
    inpFile.write("""**
""")
    inpFile.write("""**
** 127 - 5 = 122
*DEPVAR,delete=122
127
**  number of state dependent variables, must be larger than (or equal
**  to) ten times total number of slip systems in all sets, plus
**  five, plus the additional number of state variables users
**  introduced for their own single crystal model
**
**   For example, {110}<111> has twelve slip systems.  There are
**   12*10+5=113 state dependent variables.
** ----------------------------------------------------------------
""")

# write step information
inpFile.write("""**
** ********************************************************************
** STEP: Step-1
** ********************************************************************
*Step, name=Step-1, nlgeom=YES, inc=100000000
*Static
"""+str(initialIncSize)+""", """+str(totalTime)+""", """+str(minIncSize)+""", """+str(maxIncSize)+"""
**
** BOUNDARY CONDITIONS
**
** for example, bottom edge maybe x0 node sets,
**              top edge maybe x1 node sets
** this should be checked carefully
**
** Name: BC-1 Type: Symmetry/Antisymmetry/Encastre
*Boundary
z0, ENCASTRE
** Name: BC-2 Type: Displacement/Rotation
** *Boundary
** z1, 1, 1
** z1, 2, 2, 
** z1, 3, 3
** z1, 4, 4
** z1, 5, 5
** z1, 6, 6
*Boundary
disp-load, 1,1
disp-load, 2,2
disp-load, 3,3,"""+str(dispZ)+"""
disp-load, 4,4
disp-load, 5,5
disp-load, 6,6
**
** OUTPUT REQUESTS
**
*Restart, write, frequency=0
**
** FIELD OUTPUT: F-Output-1
**
*Output, field, frequency="""+str(frequency)+"""
*Node Output
CF, RF, U
*Element Output, directions=YES
LE, PE, PEEQ, PEMAG, S, SDV, STATUS
*Contact Output
CDISP, CSTRESS
**
** HISTORY OUTPUT: load-disp
**
*Output, history
*Node Output, nset=disp-load
RF3, U3
**
** HISTORY OUTPUT: H-Output-1
**
*Output, history, variable=PRESELECT
*End Step
""")

inpFile.close()
