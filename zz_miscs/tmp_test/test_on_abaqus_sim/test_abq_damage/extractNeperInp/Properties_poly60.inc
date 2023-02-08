************************************************************************
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
    168400.0, 121400.0, 75400.0,
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
0.00030657207251582024,0.012195800934564216,0.9999255814575047,  0.,   0.,   1.,
** direction in local system ,      global system       , of the 1st vector
**    ---  ,   --   ,   --   ,   --   ,   --   ,   --   ,
** (the first vector to determine crystal orientation in global system)
**
0.03481459950013649,0.9993193313915018,-0.01219908065743744,  0.,   1.,   0.,
** direction in local system ,      global system       , of the 2nd vector
**    --   ,   --   ,   --   ,   --   ,   --   ,   --   ,
** (the second vector to determine crystal orientation in global system)
**
** constraint:  The angle between two non-parallel vectors in the local
**              and global systems should be the same.  The relative 
**              difference must be less than 0.1%. 
**
**
      10.0 ,  0.001  ,
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
     541.5 , 109.5 , 60.84  ,
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
     1.0   ,1.0     ,
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
