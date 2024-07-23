import sqlite3
import pandas as pd

def get_task_by_id():
    try:
        with sqlite3.connect('transport.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT "Kd mean" FROM Data WHERE Site = "Hrádek"')
            row = cur.fetchall()
            return row
    except sqlite3.Error as e:
        print(e)
        return None      

if __name__ == '__main__':
    task = get_task_by_id()

df = pd.DataFrame(task)
print(df)