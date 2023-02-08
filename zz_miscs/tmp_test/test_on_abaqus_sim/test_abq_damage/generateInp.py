#
#
import glob
import re

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
0.01, 10., 1e-08, 0.01
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
*Boundary
z1, 1, 1
z1, 2, 2, 2.
z1, 3, 3
z1, 4, 4
z1, 5, 5
z1, 6, 6
**
** OUTPUT REQUESTS
**
*Restart, write, frequency=0
**
** FIELD OUTPUT: F-Output-1
**
*Output, field
*Node Output
CF, RF, U
*Element Output, directions=YES
LE, PE, PEEQ, PEMAG, S, SDV, STATUS
*Contact Output
CDISP, CSTRESS
**
** HISTORY OUTPUT: H-Output-1
**
*Output, history, variable=PRESELECT
*End Step
""")

inpFile.close()
