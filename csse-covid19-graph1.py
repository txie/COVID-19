import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
# plt.style.use('tableau-colorblind10')
# plt.style.use('ggplot')
import numpy as np
import pandas as pd

data = pd.read_csv('../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
usData = data[(data['Country/Region'] == 'US')]

plt.xlim([0, 70])
# plt.ylim([0, 100000])
# plt.axis([0, 70, 0, 100000])
confirmed = [usData[d].sum() for d in usData.columns[4:]]

# fig, ax = plt.subplots()

plt.plot(confirmed)
plt.xlabel('Days')
plt.ylabel('# of confirmed cases')
plt.yscale('log')
plt.title('US Confirmed COVID-19 Cases (based on JHU)')
plt.grid()
plt.show()
# for d in usData.columns[4:]:
#     print('{} - {}'.format(d, usData[d].sum()))