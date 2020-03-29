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
data = pd.read_csv('../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

itData = data[(data['Country/Region'] == 'Italy')]
frData = data[(data['Country/Region'] == 'France')]
usData = data[(data['Country/Region'] == 'US')]
deData = data[(data['Country/Region'] == 'Germany')]
esData = data[(data['Country/Region'] == 'Spain')]
ukData = data[(data['Country/Region'] == 'United Kingdom')]

brData = data[(data['Country/Region'] == 'Brazil')]
agData = data[(data['Country/Region'] == 'Argentina')]

idData = data[(data['Country/Region'] == 'Indonesia')]
myData = data[(data['Country/Region'] == 'Malaysia')]

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
yUSPredicts = [150000, 170000, 185000, 200000, 230000]

yFr = filterZeros([frData[d].sum() for d in frData.columns[20:]]) + exts
yIt = filterZeros([itData[d].sum() for d in itData.columns[20:]]) + exts
yUS = filterZeros([usData[d].sum() for d in usData.columns[20:]]) + exts
yDE = filterZeros([deData[d].sum() for d in itData.columns[20:]]) + exts
yES = filterZeros([esData[d].sum() for d in itData.columns[20:]]) + exts
yUK = filterZeros([ukData[d].sum() for d in itData.columns[20:]]) + exts

yBR = filterZeros([brData[d].sum() for d in usData.columns[20:]]) + exts
yAG = filterZeros([agData[d].sum() for d in itData.columns[20:]]) + exts

yID = filterZeros([idData[d].sum() for d in usData.columns[20:]]) + exts
yMY = filterZeros([myData[d].sum() for d in itData.columns[20:]]) + exts

x = list(map(lambda x: x[:-3], data.columns[20:])) + xexts
# x = [i for i in range(len(yNY))]

print('confirmed cases: {}'.format(yUS))


fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 1000000])
ax.minorticks_on()
ax.grid(color='gray')


# build the timeline
timeline = {
    '1/23': 'Wuhan lockdown',
    '1/30': 'WHO: Global Emergency',
    '3/11': 'WHO: Pandemic', 
    '3/13': 'National Emergency', 
    '3/19': 'Bay Area Shelter-in-Place'
}
quotes, q = {}, 1

for i, d in enumerate(x): 
    # print('d = {}'.format(d))
    if d in timeline.keys():
        ax.annotate(str(q), xy=(i, 5), arrowprops=dict(facecolor='red', shrink=0.05))
        quotes[i] = timeline[d]
        print('y cord: {}'.format(100-q*20))
        ax.text(44, 100 - q*20, str(q) + ': ' + timeline[d])
        q += 1
        # print('event: {}'.format(timeline[d]))
        # plt.figtext(10, 0.01 + q, timeline[d])
        # ax.text(71, 10+q*2, timeline[d])
    # ax.annotate('3/13: National Emergency', xy=(20, 0))
ax.text(71, 120, 'Notes:')


ax.plot(x, yFr, marker='o', label='FR')
ax.plot(x, yIt, marker='o', label='IT')
ax.plot(x, yDE, marker='o', label='DE')
ax.plot(x, yES, marker='o', label='ES')
ax.plot(x, yUK, marker='o', label='UK')

ax.plot(x, yBR, marker='o', label='BR')
ax.plot(x, yAG, marker='o', label='AG')

ax.plot(x, yID, marker='o', label='ID')
ax.plot(x, yMY, marker='o', label='MY')

line = ax.plot(x, yUS, lw=3, marker='o', label='US')

realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [yUS[-6]] + yUSPredicts, marker='o', linestyle=':', label='US Predicted')

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('Confirmed COVID-19 Cases (based on JHU data)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

mplcursors.cursor(line)

plt.show()
