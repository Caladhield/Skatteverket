#%%
import pandas as pd
#%%
df = pd.read_excel("all_kommunal_skatt.xlsx")

df_diff = df.copy()

for year in range(2014, 2024):
    df_diff[str(year)] = df[str(year)] - df["2014"]
    df_diff.to_excel("kommunal_skatt_diff.xlsx", index=False)
    
print("Skillnaden har sparats i kommunal_skatt_diff.xlsx")
# %%
