from ast import *
import os
######################################################################
from user_utils.calculate_in_abaqus import calculate_in_abaqus_plasticity
from user_utils.readExpDataSorted import readExpDataSorted
from user_utils.plot_opt_vs_exp import plot_opt_vs_exp
from user_utils.argsparser import argsparser
from user_utils.zoopt_search import zoopt_search
from user_utils.global_variables import global_variables

#####################################################################
if __name__ == '__main__':
    # copyt parameters into user_utils folder
    cp_cmd = "cp ./parameters.csv ./user_utils/"
    os.system(cp_cmd)
    #
    threads_per_abq = global_variables("OMP_NUM_THREADS", 1)
    # experimental data file directory
    expDataFileName = global_variables("expDataFileName", 1)
    # 注意到上述实验数据中，使用的应变是%比的形式，且是工程应力应变,因此做如下转换
    # flagPercent_ = global_variables.global_variables("",)
    flagPercent = global_variables("flagPercent", 1)
    flagTrueStrainStress = global_variables("flagTrueStrainStress", 1)
    lengthSection = global_variables("lengthSection", 1)
    areaSection = global_variables("areaSection", 1)

    # -------------------------------------------------------------------
    # optimization iteration starts
    config = argsparser()
    zoopt_search(config)
    # optimization iteration ends
    # -------------------------------------------------------------------

    # read optimized result which is stored in "x_record.txt"
    opt_results = open('./x_record.txt').read().split()
    # calculate in abaqus and get disp and load
    disp_opt, load_opt = calculate_in_abaqus_plasticity(opt_results, threads_per_abq[0])
    # to calcualte engineering strain and stress
    strainEng_opt = disp_opt / float(lengthSection[0])
    stressEng_opt = load_opt / float(areaSection[0])
    #
    strainEng_exp, stressEng_exp = readExpDataSorted(
        fileName=expDataFileName[0],
        flagPercent=int(flagPercent[0]),
        flagTrueStrainStress=int(flagTrueStrainStress[0]))

    plot_opt_vs_exp(strainEng_opt, stressEng_opt,
                    strainEng_exp, stressEng_exp)
