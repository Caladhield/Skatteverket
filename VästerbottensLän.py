import requests
import pandas as pd

def fetch_data(year):
    url = f"https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99?%C3%A5r={year}&_limit=500&_offset=900"
    
    group_två_kommuner = ["BJURHOLM", "DOROTEA", "LYCKSELE", "MALÅ", "NORDMALINGS",
                        "NORSJÖ", "ROBERTSFORS", "SKELLEFTEÅ", "SORSELE", "STORUMAN",
                        "UMEÅ", "VILHELMINA", "VINDELN", "VÄNNÄS", "ÅSELE",]

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            results = data["results"]

            filtered_data = []

            for result in results:
                kommun = result["kommun"].upper()
                if kommun in group_två_kommuner:
                    kommunal_skatt = float(result["kommunal-skatt"].replace(",", "."))  # Convert to float
                    excel_data = {"Year": year, 
                                  "Kommun": kommun, 
                                  "Kommunal Skatt": kommunal_skatt}
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
    df.columns = [f"{year}" for year in df.columns]
    
    alla_kommuner = df.index.tolist()
    df["Kommun"] = alla_kommuner
    
    df = df[["Kommun"] + [col for col in df.columns if col != "Kommun"]]
    
    # Calculate the difference between 2014 and 2023 for each municipality
    df["Diff_2014-2023"] = df["2023"] - df["2014"]
    
    average_change = df["Diff_2014-2023"].mean()
    
    df.loc["Snittet Län"] = ["Snitt Ökning/sänkning", average_change] + [""] * (len(df.columns) - 2)
    
    df.to_excel("Västerbottens.xlsx", index=False)
    print("Data saved to Västerbottens.xlsx")
else:
    print("No data to save.")
