import os
import glob
from user_utils.readCurve import readCurve
from user_utils.global_variables import global_variables


def calculate_in_abaqus_plasticity(x, cpus_abq):
    # declare variables for convenience
    # # to avoid too long folder name using if
    # flag_e_p_ = global_variables("flag_e_p", 1)
    flag_e_p = 1
    C11_ = global_variables("C11", 1)
    C12_ = global_variables("C12", 1)
    C44_ = global_variables("C44", 1)
    n_ = global_variables("n", 1)
    adot_ = global_variables("adot", 1)
    h0_ = global_variables("h0", 1)
    taus_ = global_variables("taus", 1)
    tau0_ = global_variables("tau0", 1)
    q_ = global_variables("q", 1)
    q1_ = global_variables("q1", 1)
    # read inp data
    initialIncSize_ = (global_variables("Static", 4))
    totalTime_ = (global_variables("Static", 4))
    minIncSize_ = (global_variables("Static", 4))
    maxIncSize_ = (global_variables("Static", 4))
    dispZ_ = (global_variables("z1", 1))
    frequency_ = (global_variables("frequency", 1))

    C11 = C11_[0]
    C12 = C12_[0]
    C44 = C44_[0]
    # n = global_variables.global_variables("n",1)
    n = x[0]
    adot = adot_[0]
    # h0 = global_variables.global_variables("h0",1)
    h0 = x[1]
    # tau0 = global_variables.global_variables("tau0",1)
    tau0 = x[2]
    # taus = global_variables.global_variables("taus",1)
    taus = x[3]
    q = q_[0]
    q1 = q1_[0]

    # if flag_e_p == 1, then it is plastic determination
    # for plastic parameters determination, x stores only plastic parameters

    # store the cwd where the pso_damask.py located
    cwd = os.getcwd()

    """
        launch the pre-processing script
    """
    # ---------------------------------------------------------------
    # create folder named by input list X and copy files into created folder
    os.chdir('./1_abaqus/0_sim_preparation/0_pre_process/')
    # prepare command with 4 variables to be transferred
    cmd_pre_process = 'python3 pre-process.py' + ' ' + \
        str(C11) + ' ' + \
        str(C12) + ' ' + \
        str(C44) + ' ' + \
        str(n) + ' ' + \
        str(adot) + ' ' + \
        str(h0) + ' ' + \
        str(taus) + ' ' + \
        str(tau0) + ' ' + \
        str(q) + ' ' + \
        str(q1) + ' ' + \
        str(flag_e_p) + ' ' +\
        '> pre_run.log'
    # launch pre-process.py
    os.system(cmd_pre_process)
    # return to the cwd: where the pso_damask.py located
    os.chdir(cwd)

    # update paramaters in created folder
    # get mySimDirName to avoid too long folder name using if
    mySimDirName = 'n_' + str(n) + \
        '_adot_' + str(adot) + \
        '_h0_' + str(h0) + \
        '_taus_' + str(taus) + \
        '_tau0_' + str(tau0) + \
        '_q_' + str(q) + \
        '_q1_' + str(q1)

    # chdir to the newly created folder
    newDir = './1_abaqus/1_sim_for_iterations/' + mySimDirName
    os.chdir(newDir)

    # update Property command
    update_Property_cmd = 'python3 generateProperty.py' + ' ' + \
        str(C11) + ' ' + \
        str(C12) + ' ' + \
        str(C44) + ' ' + \
        str(n) + ' ' + \
        str(adot) + ' ' + \
        str(h0) + ' ' + \
        str(taus) + ' ' + \
        str(tau0) + ' ' + \
        str(q) + ' ' + \
        str(q1)
    os.system(update_Property_cmd)

    # update inp command
    initialIncSize = initialIncSize_[0]
    totalTime = totalTime_[1]
    minIncSize = minIncSize_[2]
    maxIncSize = maxIncSize_[3]
    dispZ = dispZ_[0]
    frequency = frequency_[0]
    update_Inp_cmd = 'python3 inpFileWriteTmp.py' + ' ' + \
        str(initialIncSize) + ' ' + \
        str(totalTime) + ' ' + \
        str(minIncSize) + ' ' + \
        str(maxIncSize) + ' ' + \
        str(dispZ) + ' ' + \
        str(frequency) + ' '
    os.system(update_Inp_cmd)
    # return to the cwd: where the pso_damask.py located
    os.chdir(cwd)

    """
        launch the simulation
    """
    # ---------------------------------------------------------------
    #
    # chdir to the current simulation directory for the current
    # particle in the current iteration
    os.chdir('./1_abaqus/1_sim_for_iterations/'+mySimDirName)
    #
    job_name = "example_rp"
    user_name = "umat.f"
    abq_full_cmd = "abq2020 job="+job_name+" user="+user_name+" cpus=" \
        + str(cpus_abq) + " &"

    # launch it
    os.system(abq_full_cmd)

    # sleep some seconds to let compiling process pass
    # this time may be extended if the fortran compiling process
    # takes more time
    # 不要吝啬这 60 秒，要是时间不够长，很有可能还没进入standard计算就开始如下的
    # 判断，那将产生很大的问题。
    os.system('sleep 60')

    # handle exceptions
    while (1):
        # exception 1: bad parameters leads to crash
        if not os.path.exists(job_name+'.sta'):
            print('.sta not exists, errors occur')
            break
        else:
            # read the last line
            # open sta to read the last line
            with open(job_name+'.sta', 'r') as file:
                last_line = file.readlines()[-1]
                file.close()
        if "THE ANALYSIS HAS" in last_line:
            os.system("rm *.lck")
            break
        else:
            """
            In some cases during testing, there does not exsit "THE ANALYSIS HAS..." in the 
            .sta file but the calculation was terminated as well.
            In this case, this loop can never been terminated and the program will be blocked.
            Therefore, to avoid this situation, when the simuation was terminated without the 
            feature "THE ANALYSIS HAS..." in the .stat file but one type of  execetion file
            occured. The else condition should ternimation this loop.
            """
            if glob.glob('*.exception'):
                # 很奇怪，有时候会无缘无故的出现一个exception，但是sta还在正常的运行，所以会出问题
                with open(job_name+'.sta', 'r') as file:
                    last_line = file.readlines()[-1]
                    file.close()
                old_tail = last_line
                os.system('sleep 30')
                with open(job_name+'.sta', 'r') as file:
                    last_line = file.readlines()[-1]
                    file.close()
                new_tail = last_line
                if old_tail == new_tail:
                    print("***The calculation was terminated abnormally!!!\n"
                      + "***check the exception explanation in calculate_in_abaqus.py")
                    break
        # sleep for 30s to avoid excessive condition checking
        os.system('sleep 30')

    # special attention should be paid here
    #
    # return to the cwd
    os.chdir(cwd)

    """
        launch the post process
    """
    # ---------------------------------------------------------------
    #
    # go to the current simulation dir for the current
    # particle in the current iteration
    os.chdir('./1_abaqus/1_sim_for_iterations/'+mySimDirName)
    # Post process
    cmd_abq_post = 'abq2020 script=get_disp_load_RP.py > post_run.log'
    os.system(cmd_abq_post)
    # # launch with nohup
    # os.system('nohup python3 -u get_disp_load_RP.py > post.log 2>&1')
    # rm the hdf5 file
    os.system('rm *.odb')
    # os.system('rm *.sta *.stt *.sim *.res *.prt *.mdl *.com *.odb *.dat *.msg *.excep* *.log *.fil')

    # return to the cwd
    os.chdir(cwd)

    # read data to stress_sim and strain_sim
    # this is the same as the current iteration simulation directory
    disp_load_sim_file = './1_abaqus/1_sim_for_iterations/' + \
        mySimDirName + '/' + 'disp-load-rp.txt'
    # read data by readCurve function
    disp_sim, load_sim = readCurve(disp_load_sim_file, 1, 2)

    return disp_sim, load_sim
