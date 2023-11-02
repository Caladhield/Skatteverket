import requests
import pandas as pd

def fetch_and_filter_data(url, years, kommuner):
    filtered_data = []

    for year in years:
        year_url = f"{url}?år={year}"

        try:
            response = requests.get(year_url)

            if response.status_code == 200:
                data = response.json()
                results = data["results"]

                for result in results:
                    kommun = result["kommun"].upper()
                    if kommun in kommuner:
                        kommunal_skatt = result["kommunal-skatt"]
                        excel_data = {"Year": year, "Kommun": kommun, "Kommunal Skatt": kommunal_skatt}
                        filtered_data.append(excel_data)
                        
            else:
                print(f"Failed to retrieve data for year {year}. Status code:", response.status_code)

        except Exception as error:
            print(f"An error occurred for year {year}:", str(error))

    return filtered_data

if __name__ == "__main__":
    url = "https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99"
    years = list(range(2014, 2024))
    kommuner = ["BOTKYRKA","DANDERYD","EKERÖ","HANINGE","HUDDINGE",
                "JÄRFÄLLA","LIDINGÖ","NACKA","NORRTÄLJE","NYKVARN",
                "NYNÄSHAMN","SALEM","SIGTUNA","SOLLENTUNA","SOLNA",
                "STOCKHOLM","SUNDBYBERG","SÖDERTÄLJE","TYRESÖ","TÄBY",
                "UPPLANDS VÄSBY","UPPLANDS-BRO","VALLENTUNA","VAXHOLM","VÄRMDÖ",
                "ÖSTERÅKER"]

    data = fetch_and_filter_data(url, years, kommuner)

    if data:
        df = pd.DataFrame(data)
        df.drop_duplicates(subset=["Year", "Kommun"], keep="first", inplace=True)
        df = df.pivot(index="Kommun", columns="Year", values="Kommunal Skatt")
        df.columns = [f"{year}" for year in df.columns]
        df.to_excel("all_kommunal_skatt.xlsx", index=False)
        print("Data saved to all_kommunal_skatt.xlsx")
    else:
        print("No data to save.")
