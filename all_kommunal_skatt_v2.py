#%%
import requests
import pandas as pd
#%%
def fetch_data(year):
    url = f"https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99?år={year}"
    
    group_ett_kommuner = ["BOTKYRKA","DANDERYD","EKERÖ","HANINGE","HUDDINGE",
                        "JÄRFÄLLA","LIDINGÖ","NACKA","NORRTÄLJE","NYKVARN",
                        "NYNÄSHAMN","SALEM","SIGTUNA","SOLLENTUNA","SOLNA",
                        "STOCKHOLM","SUNDBYBERG","SÖDERTÄLJE","TYRESÖ","TÄBY",
                        "UPPLANDS VÄSBY","UPPLANDS-BRO","VALLENTUNA","VAXHOLM","VÄRMDÖ",
                        "ÖSTERÅKER"]

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            results = data["results"]

            filtered_data = []

            for result in results:
                kommun = result["kommun"].upper()
                if kommun in group_ett_kommuner:
                    kommunal_skatt = result["kommunal-skatt"]
                    excel_data = {"Year": year, "Kommun": kommun, "Kommunal Skatt": kommunal_skatt}
                    filtered_data.append(excel_data)
                    
            return filtered_data

        else:
            print(f"Failed to retrieve data for year {year}. Status code:", response.status_code)
            return []

    except Exception as error:
        print(f"An error occurred for year {year}:", str(error))
        return []

years = list(range(2014, 2024))
all_data = []

for year in years:
    data = fetch_data(year)
    all_data.extend(data)

if all_data:
    df = pd.DataFrame(all_data)
    df.drop_duplicates(subset=["Year", "Kommun"], keep="first", inplace=True)
    df = df.pivot(index="Kommun", columns="Year", values="Kommunal Skatt")
    df.columns = years#
    
    alla_kommuner = df.index.tolist()
    df["Kommun"] = alla_kommuner
    
    df = df[["Kommun"] + [col for col in df.columns if col != "Kommun"]]

    df[years] = df[years].astype(float) # convert to float

    df['Skilnad'] = (df[2023] - df[2014]) / 10 #Genomsnittlig ökning perår

    df.to_excel("all_kommunal_skatt.xlsx", index=False)
    print("Data saved to all_kommunal_skatt.xlsx")
else:
    print("No data to save.")
#%%
 