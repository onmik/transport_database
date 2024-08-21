import pandas as pd

conc = pd.read_csv("output_2.xls", skiprows=1, header=None, delim_whitespace=True)
conc = conc.iloc[1]
conc = conc.loc[17]
