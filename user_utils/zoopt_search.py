import numpy as np
from zoopt import Objective, Dimension, Parameter, ExpOpt
from user_utils.myobjective import myobjective
from user_utils.global_variables import global_variables
from user_utils.StoppingCriterion import StoppingCriterion


def zoopt_search(config):
    # current_bounds = np.array([[200.e6, 800.e6,],
    #                             [10., 50.,],
    #                             [100.e6, 150.e6,]])
    # optimization parameters
    dim_elastic_ = global_variables("dim_elastic", 1)
    dim_plastic_ = global_variables("dim_plastic", 1)
    budget_ = global_variables("budget", 1)
    parallel_ = global_variables("parallel", 1)
    server_num_ = global_variables("server_num", 1)
    opt_plot_file_ = global_variables("opt_plot_file", 1)
    # bounds type parameters
    C11_bounds_ = global_variables("C11_bounds", 2)
    C12_bounds_ = global_variables("C12_bounds", 2)
    C44_bounds_ = global_variables("C44_bounds", 2)
    n_bounds_ = global_variables("n_bounds", 2)
    adot_bounds_ = global_variables("adot_bounds", 2)
    h0_bounds_ = global_variables("h0_bounds", 2)
    taus_bounds_ = global_variables("taus_bounds", 2)
    tau0_bounds_ = global_variables("tau0_bounds", 2)
    q_bounds_ = global_variables("q_bounds", 2)
    q1_bounds_ = global_variables("q1_bounds", 2)

    # # constant type parameters
    # C11_ = global_variables.global_variables("C11", 1)
    # C12_ = global_variables.global_variables("C12", 1)
    # C44_ = global_variables.global_variables("C44", 1)
    # n_ = global_variables.global_variables("n", 1)
    # adot_ = global_variables.global_variables("adot", 1)
    # h0_ = global_variables.global_variables("h0", 1)
    # taus_ = global_variables.global_variables("taus", 1)
    # tau0_ = global_variables.global_variables("tau0", 1)
    # q_ = global_variables.global_variables("q", 1)
    # q1_ = global_variables.global_variables("q1", 1)
    # print(flag_e_p)

    # plastic parameter determination
    # the unknowns are:
    # n: rate sensitivity exponent (parameter)
    # h0: initial hardening modulus
    # tau0: initial critical resolved stress
    # taus: saturation stress
    current_bounds = \
        np.array([[float(n_bounds_[0]), float(n_bounds_[1]),],
                  [float(h0_bounds_[0]),   float(h0_bounds_[1]),],
                  [float(tau0_bounds_[0]),   float(tau0_bounds_[1]),],
                  [float(taus_bounds_[0]),   float(taus_bounds_[1]),]])

    dim = Dimension(int(dim_plastic_[0]), current_bounds, [
                    True] * int(dim_plastic_[0]))

    objective = Objective(myobjective, dim)
    parameter = Parameter(budget=int(budget_[0]),
                          #stopping_criterion=StoppingCriterion(),
                          parallel=bool(parallel_[0]), server_num=int(server_num_[0]),
                          sequential=False, ponss=False,
                          intermediate_result=True, intermediate_freq=1)
    # opt and plot
    # 需要传入的是lower_dim和upper_dim，
    # 例如希望第一个维度的值始终小于第二个维度， lower_dim=0， upper_dim=1
    # 希望第一个维度大于第二个维度，那就传入,   lower_dim=1,  upper_dim=0
    # current_bounds [0,1,2,3] 2 -->> [100.e6, 150.e6,],  3 -->> [200.e6, 1500.e6,]
    # current_bounds[2] should always smaller than current_bounds[3]
    #
    #   搜索,权宜之计，修改 lower_dim 和 upper_dim
    #
    solution_list = ExpOpt.min(objective,
                               parameter,
                               lower_dim=2, upper_dim=3,
                               repeat=1, 
                               plot=True, plot_file=opt_plot_file_[0])

    # record the best result
    x_record = []
    for solution in solution_list:
        print(solution.get_x(), solution.get_value())
        x_record.append(solution.get_x())

    #
    x_record = np.asarray(x_record)
    # x_record = np.round(x_record.astype('float'), 2)
    print("x_record", x_record)
    np.savetxt("x_record.txt", x_record, fmt="%f")
