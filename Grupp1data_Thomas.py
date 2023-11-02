import requests
import json
import pandas as pd

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

            if "results" in data:
                results = data["results"]

                kommunal_skatt_data = []

                for result in results:
                        kommunal_skatt = result["kommunal-skatt"]
                        kommun = result["kommun"].upper()
                        
                        if kommun in group_ett_kommuner:
                            exceldata = {"Year": year, 
                                         "Kommun": kommun, 
                                         "Kommunal-skatt": kommunal_skatt}
                            kommunal_skatt_data.append(exceldata)

                return kommunal_skatt_data

        else:
            print(f"Error for year: {year}. Status code:", response.status_code)
            return []

    except Exception as error:
        print(f"An error occurred for year {year}:", str(error))
        return []

def get_data_group_ett():
    years = list(range(2014, 2024))

    all_data = []

    for year in years:
        kommunal_skatt_data = fetch_data(year)
        all_data.extend(kommunal_skatt_data)

    if all_data:
        df = pd.DataFrame(all_data)
        
        #remove duplicates
        df.drop_duplicates(subset=["Year", "Kommun"], keep="first", inplace=True)
        #sort the excel
        df.sort_values(by=["Kommun", "Year"], inplace=True)

        #create an excel with 
        df.to_excel("kommunal_skatt_data.xlsx", index=False)
        print("Combined data saved to kommunal_skatt_data.xlsx")
    else:
        print("No data to save.")

if __name__ == "__main__":
    get_data_group_ett()
