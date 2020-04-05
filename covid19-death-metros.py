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
        x = list(data[(data['date'] == d)]['deaths'])
        res.append(0 if len(x) == 0 else x[0])
    return res

counties = ['Santa Clara', 'San Francisco', 'Los Angeles', 'New York City', 'Orleans']
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
    countyData = data[(data['county'] == county)][['date', 'deaths']]
    yCounties[county] = prepYData(days, countyData) + exts

filterOutDays = 0

print('santa clara Y: {}'.format(yCounties['Santa Clara']))

fig, ax = plt.subplots()
# ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 2500])
ax.minorticks_on()
ax.grid(color='gray')

print('x: {}'.format(x[filterOutDays:]))
for county in counties:
    ax.plot(x[filterOutDays:], yCounties[county][filterOutDays:], marker='o', label=county)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of deaths')
plt.title('US Metros COVID-19 Deaths (based on NYTimes)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

# mplcursors.cursor(line)

plt.show()
