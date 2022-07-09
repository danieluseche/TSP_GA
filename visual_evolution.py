import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv('output_file.csv')
sns.heatmap(data)
plt.savefig('evolution.svg', bbox_inches='tight')