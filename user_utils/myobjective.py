from user_utils.calculate_in_abaqus import calculate_in_abaqus_plasticity
from user_utils.readExpDataSorted import readExpDataSorted
from user_utils.global_variables import global_variables
import numpy as np


def myobjective(config):
    """
        inputs:
            X is an array of dimension (n_particles, dimension)
        outputs:
            must return an array of size (n_particles,)
    """
    # store stress train data for simulation of each  particle
    # stress_strain_sim_particles[particles, [stress_sim,strain_sim]]
    disp_load_sim_particles = []

    # transfer all particles into calculate_in_damask_allParticles to
    # calculate in parallelled.
    #
    threads_per_abq = global_variables("OMP_NUM_THREADS", 1)
    abq_cpus = threads_per_abq[0]
    
    disp_load_sim_particles.append(calculate_in_abaqus_plasticity(config.get_x(),
                                                                  abq_cpus))
    # sys.exit()

    #####################################################################
    # 新添加的
    # 读取实验数据
    # 现将实验数据读到 strain_exp, stress_exp 中
    # expDataFileName = './2_exp_data/Exp_data/HR3C BM/拉伸曲线/HR3C BM工程应力-应变曲线.xlsx'
    expDataFileName_ = global_variables("expDataFileName", 1)
    flagPercent_ = global_variables("flagPercent", 1)
    flagTrueStrainStress_ = global_variables("flagTrueStrainStress", 1)

    strainEng_exp, stressEng_exp = readExpDataSorted(
        fileName=expDataFileName_[0],
        flagPercent=int(flagPercent_[0]),
        flagTrueStrainStress=int(flagTrueStrainStress_[0]))
    ###################################################################
    #
    lengthSection = global_variables("lengthSection", 1)
    areaSection = global_variables("areaSection", 1)
    # lengthSection = get_value.get_value("./parameters.csv",
    #               item_name="lengthSection",
    #               item_length=1)
    # areaSection = get_value.get_value("./parameters.csv",
    #               item_name="areaSection",
    #               item_length=1)
    # define objective function now
    Obj = [0] * len(disp_load_sim_particles)
    for index, item in enumerate(disp_load_sim_particles):
        ###########################################################
        # 新添加的
        # lengthSection = 1.0
        # areaSection   = 1.0
        # strain for the current particle
        #
        # pay attention to the units
        #
        strainEng_sim = item[0] / float(lengthSection[0])
        # stress for the current particle
        stressEng_sim = item[1] / float(areaSection[0])
        # 下面的这个名字看起来很奇怪，它实际上是指的是与模拟的应变值对应的实验的应力值
        stress_exp_adaptedTo_stress_sim = np.interp(strainEng_sim,
                                                    strainEng_exp,
                                                    stressEng_exp)

        Obj[index] = 0.0

        # loop all stress points to calculate:
        # the root mean square deviation referred by Ma et al 2022
        for subIndex, subItem in enumerate(stressEng_sim):
            # subIndex refers to the i-th strain point
            # subItem refers to stress_sim corresponding to subIndex-th strain
            # point
            stress_sim_ith = subItem
            ############################################################
            # 新添加的
            # to avoid 0 as denominator
            if abs(stress_exp_adaptedTo_stress_sim[subIndex]) <= 1.e-9:
                stress_exp_adaptedTo_stress_sim[subIndex] = 1.e-9

            # 新更新的
            Obj[index] = Obj[index] + (
                (stress_sim_ith - stress_exp_adaptedTo_stress_sim[subIndex])
                / stress_exp_adaptedTo_stress_sim[subIndex]
            ) ** 2
            ###############################################

    return Obj[0]
