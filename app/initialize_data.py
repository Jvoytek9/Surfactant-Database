import os
import numpy as np
import pandas as pd
from color import color

basedir = os.path.abspath(os.path.dirname(__file__))
dv = pd.read_csv(basedir + '/data/dv.csv')
dv = dv.loc[:, ~dv.columns.str.contains('^Unnamed')]
print(dv.columns)

dv.dropna(
    axis=0,
    how='all',
    thresh=None,
    subset=None,
    inplace=True
)
dv[['Study','Gas','Surfactant','Surfactant Concentration','Additive','Additive Concentration','LiquidPhase']] = dv[['Study','Gas','Surfactant','Surfactant Concentration','Additive','Additive Concentration','LiquidPhase']].fillna(value="None")

unique_studies = np.sort(np.unique(dv['Study']))
unique_gasses = np.sort(np.unique(dv['Gas']))
unique_surfactants = np.sort(np.unique(dv['Surfactant']))
unique_surfconcs = np.sort(np.unique(dv['Surfactant Concentration']))
unique_additives = np.sort(np.unique(dv['Additive']))
unique_addconcs = np.sort(np.unique(dv['Additive Concentration']))
unique_liquidphase = np.sort(np.unique(dv['LiquidPhase']))

if "None" in unique_additives:
    unique_additives = np.delete(unique_additives,np.where(unique_additives == "None"))
    unique_additives = np.append(unique_additives,"None")
if "None" in unique_addconcs:
    unique_addconcs = np.delete(unique_addconcs,np.where(unique_addconcs == "None"))
    unique_addconcs = np.append(unique_addconcs,"None")
if "None" in unique_liquidphase:
    unique_liquidphase = np.delete(unique_liquidphase,np.where(unique_liquidphase == "None"))
    unique_liquidphase = np.append(unique_liquidphase,"None")

dv['Color'] = "any"
for i in range(0,len(unique_studies)):
    dv.loc[dv.Study == unique_studies[i], 'Color'] = color[i]