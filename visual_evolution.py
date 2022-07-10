import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv('output_file.csv')
data = data.transpose()
sns.heatmap(data, linewidths = 1)
plt.title('Cost evolution TSP problem')
plt.xlabel('Generations')
plt.ylabel('Population')
plt.savefig('evolution.svg', bbox_inches='tight')