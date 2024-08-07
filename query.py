import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_task_by_id():
    try:
        with sqlite3.connect('transport.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT "Kd mean" FROM Data WHERE Site = "Čihadlo" OR Site= "Hrádek" AND Radionuclide_id="Cs-137";')
            row = cur.fetchall()
            return row
    except sqlite3.Error as e:
        print(e)
        return None      

if __name__ == '__main__':
    task = get_task_by_id()

df = pd.DataFrame(task)
dfnp = df.to_numpy().flatten()



print(dfnp)
print()
print("min Kd", + np.min(dfnp))
print("max Kd", + np.max(dfnp))
print("mean Kd", + np.mean(dfnp))
print("stdev Kd", + np.std(dfnp))

plt.plot(dfnp)
plt.show()

hist, bin_edges = np.histogram(dfnp, density=True)

plt.plot(hist)
plt.hist(dfnp, bins=5)
plt.show()
