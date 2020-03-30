from typing import List
import matplotlib.pyplot as plt
plt.style.use('bmh')
import numpy as np
import pandas as pd
import mplcursors

plt.rcParams["figure.figsize"] = (16, 8)

def filterZeros(nums: List[int]):
    return [x if x > 0 else float('nan') for x in nums]

# source: https://github.com/CSSEGISandData/COVID-19/
data = pd.read_csv('../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

itData = data[(data['Country/Region'] == 'Italy')]
frData = data[(data['Country/Region'] == 'France')]
deData = data[(data['Country/Region'] == 'Germany')]
esData = data[(data['Country/Region'] == 'Spain')]
ukData = data[(data['Country/Region'] == 'United Kingdom')]

usData = data[(data['Country/Region'] == 'US')]
brData = data[(data['Country/Region'] == 'Brazil')]
agData = data[(data['Country/Region'] == 'Argentina')]

exts = [float('nan')] * 15
xexts = [str(x) for x in range(15)]
yUSPredicts = [2700, 3400, 4800, 6000, 7900]

filterOutDays = 34
yFr = filterZeros([frData[d].sum() for d in frData.columns[filterOutDays:]]) + exts
yIt = filterZeros([itData[d].sum() for d in itData.columns[filterOutDays:]]) + exts
yUS = filterZeros([usData[d].sum() for d in usData.columns[filterOutDays:]]) + exts
yDE = filterZeros([deData[d].sum() for d in itData.columns[filterOutDays:]]) + exts
yES = filterZeros([esData[d].sum() for d in itData.columns[filterOutDays:]]) + exts
yUK = filterZeros([ukData[d].sum() for d in itData.columns[filterOutDays:]]) + exts

yBR = filterZeros([brData[d].sum() for d in usData.columns[filterOutDays:]]) + exts
yAG = filterZeros([agData[d].sum() for d in itData.columns[filterOutDays:]]) + exts

x = list(map(lambda x: x[:-3], data.columns[filterOutDays:])) + xexts
# x = [i for i in range(len(yNY))]

print('deaths: {}'.format(yUS))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 34])
ax.set_ylim([0, 100000])
ax.minorticks_on()
ax.grid(color='gray')

ax.plot(x, yFr, marker='o', label='FR')
ax.plot(x, yIt, marker='o', label='IT')
ax.plot(x, yDE, marker='o', label='DE')
ax.plot(x, yES, marker='o', label='ES')
ax.plot(x, yUK, marker='o', label='UK')

ax.plot(x, yBR, marker='o', label='BR')
ax.plot(x, yAG, marker='o', label='AG')
line = ax.plot(x, yUS, lw=3, marker='o', label='US')

realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [yUS[-6]] + yUSPredicts, marker='o', linestyle=':', label='predict')

# realNumDays = len(x) - len(xexts)
# ax.plot([ realNumDays - 1 + i for i in range(6)], [yUS[-6]] + yUSPredicts, marker='o', linestyle=':', label='predict')

# ax.plot(x, yNY, marker='o', label='NY')
# ax.plot(x, yCA, marker='o', label='CA')
# ax.plot(x, yWA, marker='o', label='WA')
# ax.plot(x, yFL, marker='o', label='FL')
# ax.plot(x, yNJ, marker='o', label='NJ')

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of deaths')
plt.title('COVID-19 Deaths (based on JHU data)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

mplcursors.cursor(line)

plt.show()
