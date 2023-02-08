import os

##
os.system('rm *.lck *.sta *.stt *.sim *.res *.prt *.mdl *.com *.odb *.dat *.msg *.excep* *.log *.fil')

##
cpus_abq = 96
job_name  =  "example_rp"
user_name = "umat.f"
abq_full_cmd = "exec abq2020 job="+job_name+" user="+user_name+" cpus=" \
    + str(cpus_abq)

# launch it
os.system(abq_full_cmd)

# sleep some seconds to let compiling process pass
# this time may be extended if the fortran compiling process
# takes more time
# 不要吝啬这 60 秒，要是时间不够长，很有可能还没进入standard计算就开始如下的
# 判断，那将产生很大的问题。
os.system('sleep 60')

# handle exceptions
while(1):
    # exception 1: bad parameters leads to crash
    if not os.path.exists(job_name+'.sta'):
        print('.sta not exists, errors occur')
        break
    # exception 2: singularity matrix
    # sigularity has been avoided in umat.f
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # if os.path.exists(job_name+'.log'):
    #     # read the last line
    #     with open(job_name+'.log','r') as file:
    #         last_line = file.readlines()[-1]
    #     file.close()
    #     # 
    #     if "Singular matrix" in last_line or\
    #         "PAUSE prompt" in last_line:
    #         break

    # normal case 1:
    if os.path.exists(job_name+'.lck'):
        #print('.lck exists, sleep 60s to wait!')
        os.system('sleep 60')
    else:
        #print('.lck does not exist, break')
        #print('abaqus process has been killed')
        break

# -------------------------------------------------------
# Post process
cmd_abq_post = 'abq2020 script=get_disp_load_RP.py'
os.system(cmd_abq_post)