import pandas as pd
import numpy as np

rollingmean = pd.DataFrame([2,4,2,6,8,645,6])
print rollingmean
rollingmean = rollingmean.drop(len(rollingmean)-1,axis=0)
rollingmean.loc[-1] = np.nan
rollingmean = rollingmean.sort_index()
print rollingmean
