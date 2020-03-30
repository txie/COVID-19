from typing import List
import matplotlib.pyplot as plt
plt.style.use('bmh')
import numpy as np
import pandas as pd
import mplcursors
from scipy import stats

plt.rcParams["figure.figsize"] = (16, 8)

def filterZeros(nums: List[int]):
    return [x if x > 0 else float('nan') for x in nums]

# OBSOLETE, JHU no longer updates its state data
# source: https://github.com/CSSEGISandData/COVID-19/
data = pd.read_csv('time_series_19-covid-Confirmed.csv')
usData = data[(data['Country/Region'] == 'US')]
ny = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'New York')]
ca = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'California')]
wa = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'Washington')]
fl = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'Florida')]
nj = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'New Jersey')]


exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
yUSPredicts1 = [42000, 50000, 56000, 69000, 81000]
yUSPredicts2 = [47000, 68000, 86000, 110000, 131000]

yUS = filterZeros([usData[d].sum() for d in usData.columns[20:]]) + exts

yNY = filterZeros([ny[d].sum() for d in ny.columns[20:]]) + exts
yCA = filterZeros([ca[d].sum() for d in ca.columns[20:]]) + exts
yWA = filterZeros([wa[d].sum() for d in wa.columns[20:]]) + exts
yFL = filterZeros([fl[d].sum() for d in fl.columns[20:]]) + exts
yNJ = filterZeros([nj[d].sum() for d in nj.columns[20:]]) + exts

x = list(map(lambda x: x[:-3], data.columns[20:])) + xexts

print('confirmed cases: {}'.format(yUS))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 100000])
ax.minorticks_on()
ax.grid(color='gray')

line = ax.plot(x, yUS, lw=3, marker='o', label='US')

realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [yUS[-6]] + yUSPredicts1, marker='o', linestyle=':', label='Predict-1')
ax.plot([ realNumDays - 1 + i for i in range(6)], [yUS[-6]] + yUSPredicts2, marker='*', linestyle=':', label='Predict-2')

ax.plot(x, yNY, marker='o', label='NY')
ax.plot(x, yCA, marker='o', label='CA')
ax.plot(x, yWA, marker='o', label='WA')
ax.plot(x, yFL, marker='o', label='FL')
ax.plot(x, yNJ, marker='o', label='NJ')

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('Confirmed COVID-19 Cases (based on JHU data)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

mplcursors.cursor(line)

plt.show()
