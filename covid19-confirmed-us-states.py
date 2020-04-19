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
        res.append(0 if len(x) == 0 else x[0])
    return res

# states = ['California', 'New York', 'Massachusetts', 'Louisiana', 'Texas', 'Alabama']
states = ['California', 'Washington', 'New York', 'New Jersey', 'Massachusetts', 'Louisiana', 'Texas', 'Florida', 'Michigan', 'Illinois']

# source: https://github.com/nytimes/covid-19-data
data = pd.read_csv('../../covid-19-data/us-states.csv')

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
days = data['date'].drop_duplicates(keep='last')
x = [d[5:] for d in days] + xexts

yStates = {}
for state in states:
    stateData = data[(data['state'] == state)][['date', 'cases']]
    yStates[state] = prepYData(days, stateData) + exts

filterOutDays = 0

print('California Y: {}'.format(yStates['California']))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 400000])
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
        ax.annotate(str(q), xy=(i, 100), xytext=(i, 55), arrowprops=dict(facecolor='red', shrink=0.05))
        quotes[i] = timeline[d]
        ax.text(70, (1.5)**(len(timeline)-q), str(q) + ': ' + timeline[d])
        q += 1

ax.text(70, 50, 'Notes:')

print('x: {}'.format(x[filterOutDays:]))
for state in states:
    ax.plot(x[filterOutDays:], yStates[state][filterOutDays:], label=state)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('States of US Confirmed COVID-19 Cases (based on NYTimes)')
plt.xticks(rotation=45)
plt.xticks(x[::2])

# mplcursors.cursor(line)

plt.show()