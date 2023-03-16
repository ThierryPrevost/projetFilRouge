import numpy as np
import pandas as pd
import csv
import time

debut = time.time()

DATAPATH="./data/"

dfImmo = pd.read_csv(DATAPATH+'immo.csv', sep=",")

print(len(dfImmo.axes[0]),'lignes')
# code_type_local = 1 Maison 2 Appartement (type_local)
print(dfImmo[["code_commune", "valeur_fonciere", "code_type_local", "surface_reelle_bati"]].head())
print(dfImmo.columns)

# manip columns
dfImmo.rename(columns={'code_commune':'codeInseeImmo'}, inplace=True)
dfImmo['codeInseeImmo'] = dfImmo.codeInseeImmo.astype('str')
dfImmo['local_total'] = np.where(dfImmo["code_type_local"].isin([1, 2]), 1, 0)
dfImmo['local_maison'] = np.where(dfImmo['code_type_local']== 1, 1, 0)
dfImmo['local_appart'] = np.where(dfImmo["code_type_local"]== 2, 1, 0)
print(dfImmo[["code_type_local", "local_total", "local_maison", "local_appart"]].head())

# manip lignes
dfImmo = dfImmo[dfImmo["code_type_local"].isin([1, 2])]
#print(dfImmo["valeur_fonciere"].isna().value_counts())
#print(dfImmo["surface_reelle_bati"].isna().value_counts())
dfImmo = dfImmo[dfImmo["valeur_fonciere"].notna()]
dfImmo = dfImmo[dfImmo["surface_reelle_bati"].notna()]

#moyenne valeur foncière
dfImmo["valeur_moyenne_fonciere"] = dfImmo["valeur_fonciere"] / dfImmo["surface_reelle_bati"]
print(dfImmo[["codeInseeImmo", "valeur_moyenne_fonciere", "code_type_local"]].head())
print(dfImmo.dtypes)
print(type('codeInseeImmo'))

# new file
#dfImmoNew = dfImmo[["codeInseeImmo", "valeur_moyenne_fonciere", "code_type_local"]]
#dfImmoNew = dfImmo.groupby(['codeInseeImmo'], sort=False, as_index=False )['valeur_moyenne_fonciere'].mean()
dfImmoNew = dfImmo.groupby(['codeInseeImmo'], sort=False, as_index=False ).aggregate({'valeur_moyenne_fonciere':'mean', 'local_total': 'sum', 'local_maison': 'sum', 'local_appart': 'sum' })

# verif
#print(dfImmo[dfImmo["codeInseeImmo"]=='1053']["valeur_moyenne_fonciere"])
#print(dfImmo[dfImmo["codeInseeImmo"]=='1053']["surface_reelle_bati"])
#print(len(dfImmo[dfImmo["codeInseeImmo"]=='1053'].axes[0]))
#print(len(dfImmo[ (dfImmo["codeInseeImmo"]=='1053') & (dfImmo["code_type_local"]==1) ].axes[0]))
#print(len(dfImmo[ (dfImmo["codeInseeImmo"]=='1053') & (dfImmo["code_type_local"]==2) ].axes[0]))
#print(len(dfImmo[dfImmo["code_type_local"]==1].axes[0]))
#print(len(dfImmo[dfImmo["code_type_local"]==2].axes[0]))
#print(len(dfImmo.axes[0]))


# export csv
dfImmoNew['valeur_moyenne_fonciere'] = round(dfImmoNew['valeur_moyenne_fonciere'],0).astype(np.int64)

#dfImmoNew.to_csv(DATAPATH+'immonew.csv', index=False,  float_format="%.f")
dfImmoNew.to_csv(DATAPATH+'immonew.csv', index=False)
fin = time.time()
print('{:.0f}'.format(fin-debut), 'secondes')
