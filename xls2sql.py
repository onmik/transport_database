import pandas as pd
import sqlite3

database_name = "transport.db"

#----------------------- Radionuclides -------------------------------
Radionuclide_sql = ''' INSERT INTO Radionuclide (Name)
    VALUES(?) '''
Radionuclides = [
    ('Cs-137'),
    ('Cl-36'),
    ('Sr-85'),
    ('Se'),
    ('U')
    ]



#------------------------------ Water ------------------------------------
Water_sql = ''' INSERT INTO Water (Name, pH, 'Na+ (mg/l)', 'K+ (mg/l)', 'Ca2+ (mg/l)', 'Mg2+ (mg/l)', 
            'F- (mg/l)', 'Cl- (mg/l)', 'SO4-- (mg/l)', 'HCO3- (mg/l)', Type)
    VALUES(?,?,?,?,?,?,?,?,?,?,?) '''

Water = [
    ('SGW2', 8.2, 16.5, 2.1, 34.6, 8.3, 0, 3.3, 21.0, 168.7, 'Ca-HCO3'),
    ('SGW3', 9.2, 89.4, 0.7, 1.3, 0.1, 9.9, 18.7, 10.5, 163.5, 'Na-HCO3')
         ]

#----------------------------- Sample --------------------------------------
df_sample = pd.read_excel('Transport1_Export.xlsx')
df_sample_1 = df_sample[['Označení vzorku', 'Název lokality', 'Typ materiálu','Hloubka odběru', ]]
df_sample_2 = df_sample_1.reindex(df_sample_1.columns.tolist() + ['Reference', 'Comment'], axis=1)
df_drop = df_sample_2.drop_duplicates() 
Sample = list(zip(*map(df_drop.get, df_drop)))

Sample_sql = ''' INSERT INTO Sample (Name, Site,Rock,'Sampling Depth (m)', Reference, Comment )
    VALUES(?,?,?,?,?,?) '''
#----------------------------- Data --------------------------------------
df = pd.read_excel('Transport1_Export.xlsx')
df = df.loc[df['Měřená veličina'] == 'Distribuční koeficient']
df_1 = df[['Stopovač', 'Označení vzorku','Kapalná fáze' , 'Název lokality', 'Výsledná hodnota', 'Nejistota']]
df_2 = df[['Poznámky']]
#df = df.assign(industry='yyy')
"""
df_1['Stopovač'] = 'Radionuclide_id'
df_1['Označení vzorku'] = 'Sample_id'
df_1['Kapalná fáze'] = 'Water_id'
"""
df_3 = df_1.reindex(df_1.columns.tolist() + ['Kd conversion factor','De mean' , 'De st dev', 'Da mean' , 'Da st dev',
                                       'method_id', 'Reference'], axis=1)
Data = pd.concat([df_3, df_2], axis=1, join="inner")
Data = list(zip(*map(Data.get, Data)))

Data_sql = ''' INSERT INTO Data(Radionuclide_id, Sample_id, Water_id, Site,'Kd mean','Kd st. dev.','Kd conversion factor',
 'De mean', 'De st dev', 'Da mean', 'Da st dev', Method , Reference, Comment )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

#--------------------- INSERT -------------------------------------------    
def add_rows_single(connection, value, sql):
    cursor = connection.cursor()
    cursor.execute(sql, [value])
    connection.commit()
    return cursor.lastrowid

def add_rows(connection, value, sql):
    cursor = connection.cursor()
    cursor.execute(sql, value)
    connection.commit()
    return cursor.lastrowid

def main():
    try:
        with sqlite3.connect(database_name) as connection:
            
            for radionuclide in Radionuclides:
                Radionuclide_id = add_rows_single(connection, radionuclide, Radionuclide_sql)
                print(f'Created a Radionuclide with the id {Radionuclide_id}')
                
            for sample in Sample:
                Sample_id = add_rows(connection, sample, Sample_sql)
                print(f'Created a Sample with the id {Sample_id}')
            
            for water in Water:
                Water_id = add_rows(connection, water, Water_sql)
                print(f'Created a Water with the id {Water_id}')
           
            for data in Data:
                Data_id = add_rows(connection, data, Data_sql)
                print(f'Created a Data with the id {Data_id}')
                
    except sqlite3.Error as err:
        print(err)
        
if __name__ == '__main__':
    main()