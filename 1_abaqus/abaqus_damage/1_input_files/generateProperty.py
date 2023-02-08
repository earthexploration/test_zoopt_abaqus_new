#
#
import math
import numpy as np
# ######################################################################
#
# function: eulerToRotMtrx
#
def eulerToRotMtrx(phi1, Psi, phi2):
    # directly copied from the pdf file
    # g1(phi1) matrix
    g1_ph1 = np.array([[+math.cos(phi1), +math.sin(phi1), 0.0],
                       [-math.sin(phi1), +math.cos(phi1), 0.0],
                       [0.0,                   0.0,       1.0]])

    # g2(Psi) matrix
    g2_Psi = np.array([[1.0,       0.0,                 0.0],
                       [0.0, +math.cos(Psi), +math.sin(Psi)],
                       [0.0, -math.sin(Psi), +math.cos(Psi)]])

    # g3(phi2) matrix
    g3_phi2 = np.array([[+math.cos(phi2), +math.sin(phi2), 0.0],
                        [-math.sin(phi2), +math.cos(phi2), 0.0],
                        [0.0,                   0.0,       1.0]])

    # rotation matrix
    rotationMatrix = np.array([[0.0, 0.0, 0.0],
                               [0.0, 0.0, 0.0],
                               [0.0, 0.0, 0.0]])
    # Amatrix  matmul  Bmatrix -->>  np.matmul(A,B)
    rotationMatrix =np.matmul(g3_phi2 , np.matmul(g2_Psi,g1_ph1))
    #print(rotationMatrix)
    #quit() 

    return rotationMatrix

# ######################################################################
# define material properties globally
# these may be updated frequently
c11  = 168400.0
c12  = 121400.0
c44  = 75400.0
#
n    = 10.0
adot = 0.001
#
# initial hardening modulus
h0   = 541.5
# saturation stress
taus = 109.5
# initial critical resolved shear stress
tau0 = 60.84
# ratio of latent to self-hardening: the same sets
q   = 1.0
# ration of laten to self-hardening: different sets
q1  = 1.0
#
isRadiansEuler = False

# ######################################################################
# Calculate 1st and 2nd vectors in the local system (crystal coordinate)
#
# This can be calculated by rotating the 1st and 2nd vectors defined in
# the global system (sample coordinate) into the local system by the
# multiplification of a rotation matrix, which can be calculated by the
# Euler angles of a grain,
#
# For more details, refer to the following link:
# https://www.notion.so/orientation-PROPS-57-PROPS-72-003bc3d17de74406a59178006aefd868
#
# The calculation of rotation matrix from euler angles can alsoe be found
# in the above link, via a pdf document named "Computing euler angles
# from a rotation matrix.pdf"
# define an euler angle (phi1, Psi, phi2) temparoliy
# phi1 in [0,2*pi)
# Psi  in [0,pi)
# phi2 in [0,2*pi)
#eulerAngle = [30,60,45] # in degrees, consider radians case later
# read euler anglers from file
#
eulerAngleFileDir = "./extractNeperInp/2-5_Phase_1.txt"
with open(eulerAngleFileDir,"r") as eulerAngleFileHandlder:
    eulerAngleLines = eulerAngleFileHandlder.readlines()
# declare an array
eulerAnglesArray = np.zeros((len(eulerAngleLines),3))
for index, item in enumerate(eulerAngleLines):
   #print(item.split()[0])
   eulerAnglesArray[index][0] = item.split()[0]
   eulerAnglesArray[index][1] = item.split()[1]
   eulerAnglesArray[index][2] = item.split()[2]
#print(eulerAngleLines)
#print(eulerAnglesArray)
#print(len(eulerAnglesArray))
#quit()
# convert the euler angles into radians if they are in degree format
if not isRadiansEuler:
    for index, item in enumerate(eulerAnglesArray):
        eulerAnglesArray[index][0] = math.radians(item[0])
        eulerAnglesArray[index][1] = math.radians(item[1])
        eulerAnglesArray[index][2] = math.radians(item[2])
#print(eulerAngle)
#quit()
#
# phi1 = eulerAngle[0]
# Psi  = eulerAngle[1]
# phi2 = eulerAngle[2]
#

#
# Rotate 1st and 2nd vectors
# The following gives what has been defined in the Properties.inc
#
#      -1.  ,   0.   ,   1.   ,   0.   ,   0.   ,   1.   ,
# ** direction in local system ,  global system, of the 1st vector
# **    ---  ,   --   ,   --   ,   --   ,   --   ,   --   ,
# ** (the first vector to determine crystal orientation in global system
# **
#       0.   ,   1.   ,   0.   ,   0.   ,   1.   ,   0.   ,
# ** direction in local system ,   global system , of the 2nd vector
# **    --   ,   --   ,   --   ,   --   ,   --   ,   --   ,
# ** (the second vector to determine crystal orientation in global syste
# **
# ** constraint:  The angle between two non-parallel vectors in the loca
# **              and global systems should be the same.  The relative 
# **              difference must be less than 0.1%.
#
#
# Attention, rotation matrix maps vectors from specimen coordinate (Vs)
# to crystal coordinate (Vc), i.e., in formulised equations as,
# Vc = RotationMatrix .dot(Vs)
# Therefore, we will fix the vectors in the specimen (global) coordinate
# and updates the vectors in the crystal (local) for each euler angle. 
# 1st vector in speciment (global) coordiante
Vs1 = np.array([0.0, 0.0, 1.0])
Vs2 = np.array([0.0, 1.0, 0.0])
# initialized to 0
Vc1 = np.array([0.0, 0.0, 0.0])
Vc2 = np.array([0.0, 0.0, 0.0])
# need to confirm whether this is correct
#Vc1 = np.matmul(rotationMatrix, Vs1)
#Vc2 = np.matmul(rotationMatrix, Vs2)
#
# print(Vc1[0])
# print(Vc2)
# 0.6123724356957945
# [ 0.65973961 -0.04736717 -0.75      ]



# ######################################################################
# read poly set numbering form file and store it in a list
with open("./extractNeperInp/poly_sets_numbering.txt","r") as polySetNumFile:
    lines = polySetNumFile.readlines()
# to remove the "\n" and store it in a list for future use
polySetList = []
for line in lines:
    polySetList.append(line[:-1])
#print(polySetList[0])
#
# use a loop to
# 1 - create property files
# 2 - copy contents into it
# 3 - to be added
for index, item in enumerate(polySetList):
#for num in polySetList:
    #print(num)
    # Properties_poly47.inc
    thisPropertyName = "./extractNeperInp/"+\
                        "Properties_poly"  +item+".inc"  
    thisPropertyFile = open(thisPropertyName,"w")
    #
    # calculate rotation matrix for this num
    #
    phi1 = eulerAnglesArray[index][0]
    Psi  = eulerAnglesArray[index][1]
    phi2 = eulerAnglesArray[index][2]
    #
    rotationMatrix = eulerToRotMtrx(phi1, Psi, phi2)
    #
    Vc1 = np.matmul(rotationMatrix, Vs1)
    Vc2 = np.matmul(rotationMatrix, Vs2)
    #
    # copy from Huang Yonggang umat 1991 and expose some varialbes
    # use the above defined: c11, c12, c44, etc 
    #
    thisPropertyFile.write("""************************************************************************
** This file is prepared by CAI Lei for facilating the usage of UMAT by
**      HUANG Yonggang 1991.
** The followings are just a copy from the .inp file associated with
**     HUANG UMAT 1991.
************************************************************************
**
*USER MATERIAL,CONSTANTS=160,UNSYMM
**
**
** All the constants below must be real numbers!
**
    """+str(c11)+""", """+str(c12)+""", """+str(c44)+""",
**    c11  ,   c12  ,   c44  , (elastic constants of copper crystal)
**    MPa  ,   MPa  ,   MPa  , 
**
      0.   ,
** constants only used for an elastic orthotropic or anisotropic material
**    MPa  ,
**
      0.   ,
** constants only used for an elastic anisotropic material
**    MPa  ,
**
** The elastic constants above are relative to crystal axes, where
**   1 -- [100],  2 -- [010],  3 -- [001] .  These elastic constants 
**   are arranged in the following order:  
**   eight constants each line (data card)
**
** (1) isotropic: 
**     E    ,  Nu      (Young's modulus and Poisson's ratio)
**     0.
**     0.
**
** (2) cubic:
**     c11  ,  c12  ,  c44
**     0.
**     0.
**
** (3) orthotropic:
**     D1111,  D1122,  D2222,  D1133,  D2233,  D3333,  D1212,  D1313,  
**     D2233
**     0.
**
** (4) anisotropic:
**     D1111,  D1122,  D2222,  D1133,  D2233,  D3333,  D1112,  D2212,
**     D3312,  D1212,  D1113,  D2213,  D3313,  D1213,  D1313,  D1123,
**     D2223,  D3323,  D1223,  D1323,  D2323
**
**
      1.   ,
** number of sets of slip systems
** This is only for cubic cyrstal, hcp should be re-considered
** number of sets of slip systems (family)
** for FCC, 1 family slip system, i.e., {111}<110>
** for BCC, 1 family slip system, i.e., {110}<111>
**                                      {112}<111>
**					{123}<111>
**    --   ,
**
      1.   ,   1.   ,   1.   ,   1.   ,   1.   ,   0.   ,
**    normal to slip plane   ,      slip direction      , of the 1st set
**    --   ,   --   ,   --   ,   --   ,   --   ,   --   ,
**
      0.   ,
**    normal to slip plane   ,      slip direction      , of the 2nd set
**    --   ,   --   ,   --   ,   --   ,   --   ,   --   ,
**
      0.   ,
**    normal to slip plane   ,      slip direction      , of the 3rd set
**    --   ,
**
**
"""+str(Vc1[0]) +""","""+str(Vc1[1])+""","""+str(Vc1[2])+""",  0.,   0.,   1.,
** direction in local system ,      global system       , of the 1st vector
**    ---  ,   --   ,   --   ,   --   ,   --   ,   --   ,
** (the first vector to determine crystal orientation in global system)
**
"""+str(Vc2[0])+""","""+str(Vc2[1])+""","""+str(Vc2[2])+""",  0.,   1.,   0.,
** direction in local system ,      global system       , of the 2nd vector
**    --   ,   --   ,   --   ,   --   ,   --   ,   --   ,
** (the second vector to determine crystal orientation in global system)
**
** constraint:  The angle between two non-parallel vectors in the local
**              and global systems should be the same.  The relative 
**              difference must be less than 0.1%. 
**
**
      """+str(n)+""" ,  """+str(adot)+"""  ,
**     n   ,  adot  , of 1st set of slip systems
**    ---  ,  1/sec ,
** (power hardening exponent and hardening coefficient)
**  gammadot = adot * ( tau / g ) ** n
**
** Users who want to use their own constitutive relation may change the
**   function subprograms F and DFDX called by the subroutine 
**   STRAINRATE and provide the necessary data (no more than 8) in the 
**   above line (data card).
**
**
      0.   ,   0.
**    n    ,  adot  , of 2nd set of slip systems
**    ---  ,  1/sec ,
**
      0.   ,   0.   ,
**    n    ,  adot  , of 3rd set of slip systems
**    --   ,  1/sec ,
**
**
     """+str(h0)+""" , """+str(taus)+""" , """+str(tau0)+"""  ,
**    h0   ,  taus  ,  tau0  , of 1st set of slip systems
**    MPa  ,   MPa  ,   MPa  ,
** (initial hardening modulus, saturation stress and initial critical 
**  resolved shear stress)
**  H = H0 * { sech [ H0 * gamma / (taus - tau0 ) ] } ** 2
**
** Users who want to use their own self-hardening law may change the 
**   function subprogram HSELF called by the subroutine LATENTHARDEN 
**   and provide the necessary data (no more than 8) in the above line 
**   (data card).
**
**
     """+str(q)+"""   ,"""+str(q1)+"""     ,
**    q    ,   q1   , Latent hardening of 1st set of slip systems
**    --   ,   --   ,
** (ratios of latent to self-hardening in the same and different sets 
**   of slip systems)
**
** Users who want to use their own latent-hardening may change the 
**   function subprogram HLATNT called by the subroutine LATENTHARDEN 
**   and provide the additional data (beyond the self-hardening data, 
**   no more than 8) in the above line (data card).
**
**
      0.   ,
**    h0   ,  taus  ,  tau0  , of 2nd set of slip systems
**    MPa  ,   MPa  ,   Mpa  ,
**
      0.   ,
**    q    ,   q1   , of 2nd set of slip systems
**    --   ,   --   ,
**
      0.   ,
**    h0   ,  taus  ,  tau0  , of 3rd set of slip systems
**    MPa  ,   MPa  ,   MPa  ,
**
      0.   ,
**    q    ,   q1   , of 3rd set of slip systems
**    --   ,   --   ,
**
**
      .5   ,   1.   ,
**   THETA , NLGEOM ,
**    --   ,   --   ,
**
** THETA:  implicit integration parameter, between 0 and 1
**
** NLGEOM:  parameter determining whether finite deformation of single 
**   crystal is considered
**
**   NLGEOM=0. --- small deformation
**   otherwise --- finite rotation and finite strain,  Users must 
**                 declare "NLGEOM" in the input file, at the *STEP 
**                 card
**
**
      1.   ,   10.  , 1.E-5  ,
**  ITRATN , ITRMAX , GAMERR ,
**    --   ,   --   ,   --   ,
** ITRATN:  parameter determining whether iteration method is used to 
**   solve increments of stresses and state variables in terms of 
**   strain increments
**
**   ITRATN=0. --- no iteration
**   otherwise --- iteration
**
** ITRMAX:  maximum number of iterations
**
** GAMERR:  absolute error of shear strains in slip systems
""")
    # close the current file
    thisPropertyFile.close()


# **
# **
# *DEPVAR
# 125
# **   number of state dependent variables, must be larger than (or equal 
# **   to) ten times total number of slip systems in all sets, plus 
# **   five, plus the additional number of state variables users 
# **   introduced for their own single crystal model
# **
# ** For example, {110}<111> has twelve slip systems.  There are 
# **   12*10+5=113 state dependent variables.
# **
# **
# *
