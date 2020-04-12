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

countries = ['Italy', 'France', 'Germany', 'Spain', 'United Kingdom', 'US', 'Brazil', 'Argentina']

exts = [float('nan')] * 15
xexts = [str(x) for x in range(15)]
yUSPredicts = [20000, 23000, 26600, 28000, 32000]

filterOutDays = 34

yCountryData = {}
for country in countries:
    _countryData = data[(data['Country/Region'] == country)]
    yCountryData[country] = filterZeros([_countryData[d].sum() for d in _countryData.columns[filterOutDays:]]) + exts

x = list(map(lambda x: x[:-3], data.columns[filterOutDays:])) + xexts
print('US deaths: {}'.format(yCountryData['US']))
    
fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 34])
ax.set_ylim([0, 100000])
ax.minorticks_on()
ax.grid(color='gray')

for country in countries:
    ax.plot(x, yCountryData[country], marker='o', label=country)

# line = ax.plot(x, yCountryData['US'], lw=3, marker='o', label='US')
realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [yCountryData['US'][-6]] + yUSPredicts, marker='o', linestyle=':', label='US Predicted')

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of deaths')
plt.title('COVID-19 Deaths (based on JHU data)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

plt.show()
