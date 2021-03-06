from typing import List
import matplotlib.pyplot as plt
plt.style.use('bmh')
import numpy as np
import pandas as pd
import mplcursors
import itertools
import math

plt.rcParams["figure.figsize"] = (16, 8)

def filterZeros(nums: List[int]):
    return [x if x > 0 else float('nan') for x in nums]

def prepYData(days, data):
    res = []
    for d in days:
        x = list(data[(data['date'] == d)]['cases'])
        # print('d: {}, x: {}'.format(d, x))
        res.append(0 if len(x) == 0 else x[0])
    return res

counties = ['Los Angeles', 'Orange', 'San Bernardino', 'Riverside', 'Ventura', 'San Diego']
# source: https://github.com/CSSEGISandData/COVID-19/
data = pd.read_csv('../../covid-19-data/us-counties.csv')

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
days = data['date'].drop_duplicates(keep='last')
x = [d[5:] for d in days] + xexts

yCounties = {}
for county in counties:
    countyData = data[ (data['county'] == county) & (data['state'] == 'California') ][['date', 'cases']]
    yCounties[county] = prepYData(days, countyData) + exts

maxY = max(list(itertools.chain(*yCounties.values())))

filterOutDays = 0

fig, ax = plt.subplots()
# ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, math.ceil(maxY/100)*100 + 1000])
ax.minorticks_on()
ax.grid(color='gray')

# build the timeline
timeline = {
    '01-23': 'Wuhan lockdown',
    '01-30': 'WHO: Global Emergency',
    '03-08': 'LA marathon',
    '03-11': 'WHO declared Pandemic', 
    '03-13': 'National Emergency', 
    '03-19': 'CA Shelter-in-Place'
}
quotes, q = {}, 1

for i, d in enumerate(x): 
    # print('d = {}'.format(d))
    if d in timeline.keys():
        ax.annotate(str(q), xy=(i, 2000), arrowprops=dict(facecolor='red', shrink=0.05))
        quotes[i] = timeline[d]
        ax.text(1, 6000 - 300*q, str(q) + ': ' + timeline[d])
        q += 1
ax.text(1, 6000, 'Notes:')

print('x: {}'.format(x[filterOutDays:]))
for county in counties:
    ax.plot(x[filterOutDays:], yCounties[county][filterOutDays:], marker='o', label=county)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('Greater Los Angeles Area Confirmed COVID-19 Cases (based on NYTimes)')
plt.xticks(rotation=45)
plt.xticks(x[::2])

# mplcursors.cursor(line)

plt.show()