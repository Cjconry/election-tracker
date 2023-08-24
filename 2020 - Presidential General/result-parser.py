from result_ETL import build_results
import pandas as pd
import matplotlib.pyplot as plt
from plot import build_plot

#build_results()
data = pd.read_csv('out.csv')  
#data= data.drop_duplicates(subset=['Progress'], keep='last')
build_plot(data)
plt.show() 