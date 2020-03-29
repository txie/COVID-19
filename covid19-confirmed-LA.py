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

counties = ['Los Angeles', 'Orange', 'San Bernardino', 'Riverside', 'Ventura']
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

fig, ax = plt.subplots()
# ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 2000])
ax.minorticks_on()
ax.grid(color='gray')

print('x: {}'.format(x[filterOutDays:]))
for county in counties:
    ax.plot(x[filterOutDays:], yCounties[county][filterOutDays:], marker='o', label=county)

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('Greater Los Angeles Area Confirmed COVID-19 Cases (based on NYTimes)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

# mplcursors.cursor(line)

plt.show()