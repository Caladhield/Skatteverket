#%%
import requests
import pandas as pd
url = "https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99"

#%%
start_year = 2014
end_year = 2024
selected_kommuner = ["UPPLANDS VÄSBY", "UPPLANDS-BRO", "VALLENTUNA", "VAXHOLM", "VÄRMDÖ"]
df = pd.DataFrame()# empty dataframe

for year in range(start_year, end_year):
    #This line modifies the url by appending the value of the year variable as a query parameter (år) to the URL. to new_url
    new_url = f"{url}?år={year}"
    
    try:
        response = requests.get(new_url)

        if response.status_code == 200:
            data = response.json()["results"]
            new_df = pd.DataFrame(data) 
            new_df = new_df[['kommunal-skatt','kommun', 'år']]
            filtered_df = new_df[new_df["kommun"].isin(selected_kommuner)] # check and take only isin "kommun" in selected_kommuner
            filtered_df.reset_index(inplace=True)
            df = pd.concat([df, filtered_df], ignore_index=True) # concatenate "df" with "filtered_df" and save it in my empty DataFrame
            print(f"Data for year {year}:")

        else:
            print(f"Failed to retrieve data for year {year}. Status code:", response.status_code)
    except Exception as error:
        print(f"An error occurred for year {year}:", str(error))

# drop_duplicats - method used to remove duplicate rows from the DataFrame
# subset= ["kommun"]specifies the column to consider when identifying duplicates/delete
df.drop_duplicates(subset=['kommunal-skatt','kommun', 'år'], inplace=True, ignore_index=True)

df.to_excel("skatteverket.xlsx")# load to excel file
print('Saved file to excel')

# %%
