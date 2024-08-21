import openturns as ot
import subprocess
import pandas as pd

def run_model(X):
    X_1, X_2 = X
    filename = 'ex13a'
    f = open(filename,'w')

    model = """
    TITLE Example 13A.--1 mmol/L NaCl/NO3 enters column with stagnant zones.
                    Implicit definition of first-order exchange model.
SOLUTION 0    # 1 mmol/L NaCl
   units   mmol/l
   pH       7.0
   pe      13.0    O2(g)   -0.7
   Na       1.0    # Na has Retardation = 2
   Cl       1.0    # Cl has Retardation = 1, stagnant exchange
   N(5)     1.0    # NO3 is conservative
#       charge imbalance is no problem ...
END
SOLUTION 1-41  # Column with KNO3
   units   mmol/l
   pH       7.0
   pe      13.0   O2(g)    -0.7
   K        1.0
   N(5)     1.0
EXCHANGE_SPECIES # For linear exchange, make KX exch. coeff. equal to NaX
   K+ + X- = KX
   log_k   0.0
   -gamma  3.5     0.015
EXCHANGE 1-41
   -equil  1
   X       1.e-3
END
PRINT
   -reset false
   -echo_input true
   -status false
TRANSPORT
   -cells  20
   -shifts 5
   -flow_direction  forward
   -time_step       3600
   -boundary_conditions   flux  flux
   -diffusion_coefficient   0.0
   -lengths         0.1
   -dispersivities  """ + str(X_1) + """
   -stagnant   1  6.8e-6  0.3        """ + str(X_2) + """
#   1 stagnant layer^, ^alpha, ^epsil(m), ^epsil(im)
END
SOLUTION 0  # Original solution with KNO3 reenters
   units   mmol/l
   pH       7.0
   pe      13.0   O2(g)    -0.7
   K        1.0
   N(5)     1.0
END
SELECTED_OUTPUT
   -file   ex13a.sel
   -reset  false
   -solution
   -distance       true
USER_PUNCH
   -headings Cl_mmol Na_mmol
  10 PUNCH TOT("Cl")*1000, TOT("Na")*1000
TRANSPORT
   -shifts 10
   -punch_cells        1-20
   -punch_frequency    10
    """

    f.write(model)
    f.close()

    subprocess.run(["bash", "-c", "phreeqc ex13a"])
    
    out_data = pd.read_csv("ex13a.sel", skiprows=1, header=None, delim_whitespace=True)
    out_data = out_data.iloc[38]
    out_data = out_data.loc[2]
    #pH_data = float(pH_data)
    return [out_data] 



result = ot.PythonFunction(2, 1, run_model)
X = [0.1, 0.2]
result(X)









