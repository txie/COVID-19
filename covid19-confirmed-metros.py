from typing import List
import matplotlib.pyplot as plt
plt.style.use('bmh')
import numpy as np
import pandas as pd
import mplcursors

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

counties = ['Santa Clara', 'San Francisco', 'Los Angeles', 'New York City']
# source: https://github.com/CSSEGISandData/COVID-19/
data = pd.read_csv('../../covid-19-data/us-counties.csv')

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
days = data['date'].drop_duplicates(keep='last')
x = [d[5:] for d in days] + xexts
yContraCostaPredict = [500, 600, 700, 800, 1000]
ySantaClaraPredict = [1500, 1600, 1700, 1800, 2000]


yCounties = {}
for county in counties:
    countyData = data[(data['county'] == county)][['date', 'cases']]
    yCounties[county] = prepYData(days, countyData) + exts

filterOutDays = 0

print('santa clara Y: {}'.format(yCounties['Santa Clara']))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 30000])
ax.minorticks_on()
ax.grid(color='gray')

# build the timeline
timeline = {
    '03-08': 'LA marathon',
    '03-11': 'WHO declared Pandemic', 
    '03-13': 'National Emergency', 
    '03-19': 'Bay Area Shelter-in-Place'
}
quotes, q = {}, 1

for i, d in enumerate(x): 
    # print('d = {}'.format(d))
    if d in timeline.keys():
        ax.annotate(str(q), xy=(i, 5), arrowprops=dict(facecolor='red', shrink=0.05))
        quotes[i] = timeline[d]
        print('y cord: {}'.format(100-q*20))
        ax.text(71, 100 - q*20, str(q) + ': ' + timeline[d])
        q += 1
        # print('event: {}'.format(timeline[d]))
        # plt.figtext(10, 0.01 + q, timeline[d])
        # ax.text(71, 10+q*2, timeline[d])
    # ax.annotate('3/13: National Emergency', xy=(20, 0))
ax.text(71, 120, 'Notes:')

        # ax.annotate(timeline[d], xy=(i, 300), arrowprops=dict(facecolor='black', shrink=0.05))
# ax.annotate('3/13: National Emergency', xy=(20, 300))
# ax.annotate('3/19: Bay Area Shelter-in-Place', xy=(30, 300))

print('x: {}'.format(x[filterOutDays:]))
for county in counties:
    ax.plot(x[filterOutDays:], yCounties[county][filterOutDays:], marker='o', label=county)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('US Metros Confirmed COVID-19 Cases (based on NYTimes)')
plt.xticks(rotation=20)
plt.xticks(x[::2])
# plt.text(71, 10, 'Notes')

# mplcursors.cursor(line)

plt.show()