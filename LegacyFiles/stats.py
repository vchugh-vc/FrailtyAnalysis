from scipy import stats
import pandas as pd

# Example data (replace with your actual data)
# data1 = [62.33,65,58.33,60.05,64,61,61,57.67,54.67,58.67]
# data2 = [53.00,63,53.3,48.33,63,48.67,50,45.67,53,54]
#
# # Calculate differences
# differences = [x - y for x, y in zip(data1, data2)]
#
# # Calculate t-statistic and p-value
# t_statistic, p_value = stats.ttest_rel(data1, data2)
#
# print("t-statistic:", t_statistic)
# print("p-value:", p_value)

df = pd.read_csv('../LongData.csv')
df['change'] = df['Control'].diff()

# Calculate average change
average_change = df['change'].mean()


print("Average change:", average_change * 100)
