import subprocess
import pandas as pd
from re import sub
import openturns as ot
import openturns.viewer as otv

def run_model(X):
    X_2, X_3, X_4 = X
    
    #----------------prepares the model file----------------
    f1 = open('testcase.in','r')          # original file
    f1_read = f1.read()
    f1.close()
    f2 = open("testcase_run.in", "w")          # file to run model
    def replace_param(dict_replace, target):
        for old_param, new_param in list(dict_replace.items()):
            target = sub(old_param, new_param, target)
        return target
    dict_replace = {
        'X_2': str(X_2),
        'X_3': str(X_3),
        'X_4': str(X_4)
        }
    f2.write(replace_param(dict_replace, f1_read))
    f2.close() 
    
    #------------------- runs simulation------------------------
    subprocess.run(["bash", "-c", "mpirun -n 1 /home/ondro/pflotran/src/pflotran/pflotran -input_prefix testcase_run"])
    
    #----------------- write quantity of interest to be evaluated-----------------
    conc = pd.read_csv("testcase_run-obs-0.pft", skiprows=1, header=None, delim_whitespace=True)
    conc = conc.iloc[80]
    conc = conc.loc[4]
    return [conc] 

model = ot.PythonFunction(3, 1, run_model)
model = ot.MemoizeFunction(model)
model.setInputDescription(["X_2", "X_3", "X_4"])
model.setOutputDescription(["conc"])

#-------------------- define marginals --------------------------------
marginals = [ot.Uniform(1.0e-11, 1.0e-10), ot.Uniform(1.0e-13, 1.0e-10), ot.Uniform(1.0e-13, 1.0e-10)]
distribution = ot.ComposedDistribution(marginals)
distribution.setDescription(["K_overburden", "K_fault1", "K_fault2"])
inputNames = distribution.getDescription()

#--------------- PCE Sobol ----------------------------------------
sizePCE = 1000
inputDesignPCE = distribution.getSample(sizePCE)
outputDesignPCE = model(inputDesignPCE)

algo = ot.FunctionalChaosAlgorithm(inputDesignPCE, outputDesignPCE, distribution)
algo.run()
result = algo.getResult()
print(result.getResiduals())
print(result.getRelativeErrors())

sensitivityAnalysis = ot.FunctionalChaosSobolIndices(result)
print(sensitivityAnalysis)
firstOrder = [sensitivityAnalysis.getSobolIndex(i) for i in range(3)]
totalOrder = [sensitivityAnalysis.getSobolTotalIndex(i) for i in range(3)]
graph = ot.SobolIndicesAlgorithm.DrawSobolIndices(inputNames, firstOrder, totalOrder)
graph.setTitle("Sobol indices by Polynomial Chaos Expansion - testcase")
view = otv.View(graph)