######################################################################
from ast import *
import os
######################################################################
from user_utils import calculate_in_abaqus
from user_utils import readExpDataSorted
from user_utils import plot_opt_vs_exp
from user_utils import argsparser
from user_utils import zoopt_search
from user_utils import global_variables
######################################################################


#####################################################################
if __name__ == '__main__':
    # copyt parameters into user_utils folder
    cp_cmd = "cp ./parameters.csv ./user_utils/"
    os.system(cp_cmd)
    #
    threads_per_abq = global_variables.global_variables("OMP_NUM_THREADS",1)
    # experimental data file directory
    expDataFileName_ = global_variables.global_variables("expDataFileName",1)
    # 注意到上述实验数据中，使用的应变是%比的形式，且是工程应力应变,因此做如下转换
    # flagPercent_ = global_variables.global_variables("",)
    flagPercent_ = global_variables.global_variables("flagPercent",1)
    flagTrueStrainStress_ = global_variables.global_variables("flagTrueStrainStress",1)
    lengthSection = global_variables.global_variables("lengthSection",1)
    areaSection = global_variables.global_variables("areaSection",1)
    
    # -------------------------------------------------------------------

    # config = argsparser.argsparser()
    # zoopt_search.zoopt_search(config)

    # read optimized result which is stored in "x_record.txt"
    # opt_results = open('./x_record.txt').read().split()
    opt_results = open('./x_record_testPara.txt').read().split()

    disp_opt, load_opt = calculate_in_abaqus.\
        calculate_in_abaqus(opt_results, threads_per_abq[0])
    strainEng_opt = disp_opt / float(lengthSection[0])
    stressEng_opt = load_opt / float(areaSection[0])
    #
    strainEng_exp, stressEng_exp = readExpDataSorted.readExpDataSorted(
        fileName=expDataFileName_[0],
        flagPercent=int(flagPercent_[0]),
        flagTrueStrainStress=int(flagTrueStrainStress_[0]))

    plot_opt_vs_exp.plot_opt_vs_exp(strainEng_opt, stressEng_opt,
                                    strainEng_exp, stressEng_exp)