# read experiment data from excel file
from operator import itemgetter
import pandas as pd
import numpy as np


def readExpDataSorted(fileName, flagPercent, flagTrueStrainStress):
    """
    Parameters
    -----------------
    fileName:
        experimental data file name including directory information
    flagPercent:
        to check whether strain is measured in percent (%) form
        0: correct form, strain = 0.01,0.02, etc
        1: percent form, strain = 0.01 should actually be 0.01%.
            therefore, should * 0.01 to strain_exp list
    flagTrueStrainStress:
        controls whether convert exp data into true strain stress data
        0: not convert, this means maybe we dont need true strain stress
            data, or the exp data has been converted to true strain stress
        1: convert exp data to true strain stress data by the following
            equation: 
            sigma_true = sigma_engineering * (1 + epsilon_engineering)
            epsilon_true = ln(1 + epsilon_engineering)

    Return:
    -----------------
    strain_exp and stress_exp lists sorted following strain_exp list
        in an ascending order
    
    strain_exp:
        strain values in a list form
    stress_exp:
        stress values in a list form
    """
    df = pd.read_excel(fileName)

    # check flagPercent
    if flagPercent == 1:
        strain_exp = df.values[:, 0] * 0.01
    else:
        strain_exp = df.values[:, 0]

    stress_exp = df.values[:, 1]

    # ###################################################################
    # sort it to avoid possible fatal errors
    # assemble into a 2d list
    strain_stress_exp = list(zip(strain_exp, stress_exp))
    # sort it
    strain_stress_exp.sort(key=itemgetter(0), reverse=False)
    # get 1st column in strain_stress_exp
    strain_exp = [i[0] for i in strain_stress_exp]
    # get 2nd column in strain_stress_exp
    stress_exp = [i[1] for i in strain_stress_exp]

    # convert to true strain stress data when flagTrueStrainStress == 1
    if flagTrueStrainStress == 1:
        stress_exp = [item * (1 + strain_exp[index]) for
                      index, item in enumerate(stress_exp)]
        strain_exp = [np.log(1 + i) for i in strain_exp]

    return strain_exp, stress_exp
