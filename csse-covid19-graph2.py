from typing import List
import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')
# plt.style.use('seaborn-dark')
# plt.style.use('seaborn-colorblind')
plt.style.use('seaborn-paper')
# plt.style.use('ggplot')
import numpy as np
import pandas as pd
import mplcursors

plt.rcParams["figure.figsize"] = (16, 8)


def filterZeros(nums: List[int]):
    return [x if x > 0 else float('nan') for x in nums]


data = pd.read_csv('../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

itData = data[(data['Country/Region'] == 'Italy')]
frData = data[(data['Country/Region'] == 'France')]
usData = data[(data['Country/Region'] == 'US')]

ny = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'New York')]
ca = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'California')]
wa = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'Washington')]
fl = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'Florida')]
nj = data[(data['Country/Region'] == 'US') & (data['Province/State'] == 'New Jersey')]


exts = [float('nan')] * 5
xexts = [x for x in range(5)]
yUSPredicts = [27000, 34000, 42000, 50000, 56000]

yFr = filterZeros([frData[d].sum() for d in frData.columns[20:]]) + exts
yIt = filterZeros([itData[d].sum() for d in itData.columns[20:]]) + exts
yUS = filterZeros([usData[d].sum() for d in usData.columns[20:]]) + exts
yNY = filterZeros([ny[d].sum() for d in ny.columns[20:]]) + exts
yCA = filterZeros([ca[d].sum() for d in ca.columns[20:]]) + exts
yWA = filterZeros([wa[d].sum() for d in wa.columns[20:]]) + exts
yFL = filterZeros([fl[d].sum() for d in fl.columns[20:]]) + exts
yNJ = filterZeros([nj[d].sum() for d in nj.columns[20:]]) + exts

x = list(map(lambda x: x[:-3], data.columns[20:])) + xexts
# x = [i for i in range(len(yNY))]

print('confirmed cases: {}'.format(yUS))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 100000])
ax.minorticks_on()
ax.grid()

ax.plot(x, yFr, marker='o', label='FR')
ax.plot(x, yIt, marker='o', label='IT')
line = ax.plot(x, yUS, lw=3, marker='o', label='US')

realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [yUS[-6]] + yUSPredicts, marker='o', linestyle=':', label='predict')
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

mplcursors.cursor(line)

plt.show()