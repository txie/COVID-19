from typing import List
import matplotlib as mpl
import matplotlib.pyplot as plt
#plt.style.use('bmh')
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
        x = list(data[(data['date'] == d)]['deaths'])
        res.append(0 if len(x) == 0 else x[0])
    return res

counties = ['Contra Costa', 'Alameda', 'Santa Clara', 'San Mateo', 'San Francisco', 'Marin']
# source: https://github.com/nytimes/covid-19-data
data = pd.read_csv('../../covid-19-data/us-counties.csv')

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
days = data['date'].drop_duplicates(keep='last')
x = [d[5:] for d in days] + xexts
yContraCostaPredict = [500, 600, 700, 800, 1000]
ySantaClaraPredict = [1500, 1600, 1700, 1800, 2000]

yCounties = {}
for county in counties:
    countyData = data[ (data['county'] == county) & (data['state'] == 'California') ][['date', 'deaths']]
    yCounties[county] = prepYData(days, countyData) + exts

filterOutDays = 300

print('santa clara Y: {}'.format(yCounties['Santa Clara']))
maxY = max(list(itertools.chain(*yCounties.values())))

fig, ax = plt.subplots()
# ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, math.ceil(maxY/10)*11])
ax.minorticks_on()
ax.grid(color='gray')

# build the timeline
timeline = {
    '01-23': 'Wuhan lockdown',
    '01-30': 'WHO: Global Emergency',
    '03-08': 'LA marathon',
    '03-11': 'WHO declared Pandemic', 
    '03-13': 'National Emergency', 
    '03-17': 'Bay Area Shelter-in-Place',
    '03-19': 'CA Shelter-in-Place'
}
quotes, q = {}, 1

for i, d in enumerate(x): 
    if d in timeline.keys():
        ax.annotate(str(q), xy=(i, 15), arrowprops=dict(facecolor='brown', shrink=0.05))
        quotes[i] = timeline[d]
        ax.text(1, 60 - 3*q, str(q) + ': ' + timeline[d])
        q += 1
ax.text(1, 60, 'Notes:')

print('x: {}'.format(x[filterOutDays:]))
for county in counties:
    ax.plot(x[filterOutDays:], yCounties[county][filterOutDays:], marker='o', label=county)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of deaths')
plt.title('SF Bay Area COVID-19 Deaths (based on NYTimes)')
plt.xticks(rotation=45)
plt.xticks(x[::2])

# mplcursors.cursor(line)

plt.show()
