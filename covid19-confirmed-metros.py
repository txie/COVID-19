from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplcursors
import itertools
import math

plt.style.use('bmh')
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

counties = [
    ('Santa Clara', 'California'), 
    ('San Francisco', 'California'), 
    ('Los Angeles', 'California'), 
    ('New York City', 'New York'), 
    ('Orleans', 'Louisiana'), 
    ('Cook', 'Illinois'), 
    ('Wayne', 'Michigan')
]
# source: https://github.com/CSSEGISandData/COVID-19/
data = pd.read_csv('../../covid-19-data/us-counties.csv')

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
days = data['date'].drop_duplicates(keep='last')
x = [d[5:] for d in days] + xexts

yCounties = {}
for (county, state) in counties:
    print('county: {}, state: {}'.format(county, state))
    countyData = data[ (data['county'] == county) & (data['state'] == state) ][['date', 'cases']]
    yCounties[county] = prepYData(days, countyData) + exts

filterOutDays = 0

print('santa clara Y: {}'.format(yCounties['Santa Clara']))

maxY = max(list(itertools.chain(*yCounties.values())))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, math.ceil(maxY/10000)*10000])
ax.minorticks_on()
ax.grid(color='gray')

# build the timeline
timeline = {
    '01-23': 'Wuhan lockdown',
    '01-30': 'WHO: Global Emergency',
    '02-25': 'Mardi Gras',
    '03-08': 'LA marathon',
    '03-11': 'WHO declared Pandemic', 
    '03-13': 'National Emergency', 
    '03-17': 'Bay Area Shelter-in-Place', 
    '03-19': 'CA Shelter-in-Place', 
    '03-20': 'NY Stay-at-Home'
}
quotes, q = {}, 1

for i, d in enumerate(x): 
    # print('d = {}'.format(d))
    if d in timeline.keys():
        ax.annotate(str(q), xy=(i, 100), arrowprops=dict(facecolor='red', shrink=0.05))
        quotes[i] = timeline[d]
        ax.text(58, (1.5)**(len(timeline)-q), str(q) + ': ' + timeline[d])
        q += 1

ax.text(58, 40, 'Notes:')

print('x: {}'.format(x[filterOutDays:]))
for (county, state) in counties:
    ax.plot(x[filterOutDays:], yCounties[county][filterOutDays:], marker='o', label=county)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('US Metros Confirmed COVID-19 Cases (based on NYTimes)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

# mplcursors.cursor(line)

plt.show()