import matplotlib.pyplot as plt

def plot_opt_vs_exp(strain_opt,stress_opt,strain_exp,stress_exp):
# ###### Input:
# opt_strain, opt_stress (MPa)
# exp_strain, exp_stress (MPa)
# ###### Output:
# plot the two data in one figure for comparision purposes
# set x and y limit

        # clear plt state
        plt.clf()
        # plt.xlim([xlim_min,xlim_max])
        # plt.ylim([ylim_min,ylim_max])
        # plot experimental curve
        plt.plot(strain_exp, stress_exp, 'k', label='exp')        
        # plot optimized curve
        plt.plot(strain_opt, stress_opt, 'r--', label='opt')
        # set legend
        plt.legend(loc='best', shadow=True)
        # save this image
        plt.savefig('opt_vs_exp.png',dpi=500)
        return