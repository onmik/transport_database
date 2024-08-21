import subprocess
import pandas as pd
from re import sub


def run_model(LOG_K_VAR, PH_VAR, U_VAR):
    
    #----------------prepares the model file----------------
    f1 = open('SCM.phr','r')          # original file
    f1_read = f1.read()
    f1.close()
    f2 = open("SCM_run.phr", "w")          # file to run model
    def replace_param(dict_replace, target):
        for old_param, new_param in list(dict_replace.items()):
            target = sub(old_param, new_param, target)
        return target
    dict_replace = {
        'LOG_K_VAR': str(LOG_K_VAR),
        'PH_VAR': str(PH_VAR),
        'U_VAR': str(U_VAR)
        }
    f2.write(replace_param(dict_replace, f1_read))
    f2.close() 
    
    #------------------- runs simulation------------------------
    subprocess.run(["bash", "-c", "mpirun -n 1 phreeqc SCM_run.phr SCM_run.phr.out phreeqc/database/llnl.dat"])
    
    #----------------- write quantity of interest to be evaluated-----------------
    out_data = pd.read_csv("output_2.xls", skiprows=1, header=None, delim_whitespace=True)
    out_data = out_data.iloc[1]
    out_data = out_data.loc[17]
    #pH_data = float(pH_data)
    return out_data 

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

problem = {
    'num_vars': 3,
    'names': ['surf_logK', 'pH', 'U'],
    'bounds': [[2, 3],
               [-9, -7],
               [0.1, 10]]
}

parameter_values = saltelli.sample(problem, 1024)

out_array = np.zeros([parameter_values.shape[0], 1])
for i, param in enumerate(parameter_values):
    out_array[i] = run_model(*param)

SI = sobol.analyze(problem, out_array[:,0], print_to_console=True)

SI.plot()
