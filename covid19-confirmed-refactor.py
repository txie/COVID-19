from typing import List
import matplotlib.pyplot as plt
plt.style.use('bmh')
import numpy as np
import pandas as pd
import mplcursors

plt.rcParams["figure.figsize"] = (16, 8)


def filterZeros(nums: List[int]):
    return [x if x > 0 else float('nan') for x in nums]


data = pd.read_csv('../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

country2DataMap = {}
country2DataMap['IT'] = data[(data['Country/Region'] == 'Italy')]
country2DataMap['FR'] = data[(data['Country/Region'] == 'France')]
country2DataMap['US'] = data[(data['Country/Region'] == 'US')]
country2DataMap['DE'] = data[(data['Country/Region'] == 'Germany')]
country2DataMap['ES'] = data[(data['Country/Region'] == 'Spain')]
country2DataMap['UK'] = data[(data['Country/Region'] == 'United Kingdom')]

country2DataMap['BR'] = data[(data['Country/Region'] == 'Brazil')]
country2DataMap['AR'] = data[(data['Country/Region'] == 'Argentina')]

country2DataMap['ID'] = data[(data['Country/Region'] == 'Indonesia')]
country2DataMap['MY'] = data[(data['Country/Region'] == 'Malaysia')]

exts = [float('nan')] * 5
xexts = [str(x) for x in range(5)]
yUSPredicts = [27000, 34000, 42000, 50000, 56000]

# x = country2DataMap['US']
# b = [x.sum() for d in d.columns[20:]]

for country in country2DataMap.keys():
    countryData = country2DataMap[country]
    country2DataMap[country] = filterZeros([countryData[d].sum() for d in countryData.columns[20:]]) + exts

# yFr = filterZeros([frData[d].sum() for d in frData.columns[20:]]) + exts

x = list(map(lambda x: x[:-3], country2DataMap['US'].columns[20:])) + xexts

print('confirmed cases: {}'.format(country2DataMap['US']))

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlim([0, 50])
ax.set_ylim([0, 100000])
ax.minorticks_on()
ax.grid(color='gray')

for c in country2DataMap.keys():
    ax.plot(x, country2DataMap[c], marker='o', label=c)

realNumDays = len(x) - len(xexts)
ax.plot([ realNumDays - 1 + i for i in range(6)], [country2DataMap['US'][-6]] + yUSPredicts, marker='o', linestyle=':', label='Predict')

plt.legend()
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.title('Confirmed COVID-19 Cases (based on JHU data)')
plt.xticks(rotation=20)
plt.xticks(x[::2])

plt.show()
