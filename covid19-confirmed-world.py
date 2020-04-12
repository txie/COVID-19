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
countries = ['Italy', 'France', 'Germany', 'Spain', 'United Kingdom', 'US', 'Brazil', 'Argentina', 'Indonesia', 'Malaysia', 'Czechia', 'Slovakia']

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
yUSPredicts = [520000, 600000, 650000, 700000, 750000]

filterOutDays = 20

yCountryData = {}
for country in countries:
    _countryData = data[(data['Country/Region'] == country)]
    yCountryData[country] = filterZeros([_countryData[d].sum() for d in _countryData.columns[filterOutDays:]]) + exts

x = list(map(lambda x: x[:-3], data.columns[20:])) + xexts
print('US confirmed cases: {}'.format(yCountryData['US']))


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
    '3/13': 'US: National Emergency', 
}
quotes, q = {}, 1

for i, d in enumerate(x): 
    # print('d = {}'.format(d))
    if d in timeline.keys():
        ax.annotate(str(q), xy=(i, 5), arrowprops=dict(facecolor='red', shrink=0.05))
        quotes[i] = timeline[d]
        ax.text(44, 100 - q*20, str(q) + ': ' + timeline[d])
        q += 1
ax.text(71, 120, 'Notes:')

for country in countries:
    ax.plot(x, yCountryData[country], label=country)

line = ax.plot(x, yCountryData['US'], lw=3, marker='o', label='US')

realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [yCountryData['US'][-6]] + yUSPredicts, marker='o', linestyle=':', label='US Predicted')

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('Confirmed COVID-19 Cases (based on JHU data)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

mplcursors.cursor(line)

plt.show()
