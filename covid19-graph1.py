import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
import numpy as np
import pandas as pd

data = pd.read_csv('COVID-19-Cases.csv')
tmp = data[['Date', 'Country_Region', 'Case_Type', 'Cases']]
confirmed = tmp[(tmp['Country_Region'] == 'US') & ((tmp['Case_Type'] == 'Confirmed') | (tmp['Case_Type'] == 'Active')) & (tmp['Cases'] > 0)]
x = confirmed[confirmed['Date'] == '3/18/2020']
print('confirmed cases: {}'.format(x['Cases'].sum())

#  df = pd.DataFrame(confirmed)
# df.sort_values(by='Date')
# df.groupby('Date').agg()

# print('{}'.format(data.r))
