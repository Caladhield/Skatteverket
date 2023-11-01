import requests


def fetch_and_filter_data(url, target_years, target_communities):
 
    filtered_data = []
    for community in target_communities:
        try:
            for year in target_years:
                år_url = f"{url}?år={year}"
                response = requests.get(år_url)

                if response.status_code == 200:
                    data = response.json()

                    for entry in data['results']:
                        if entry['år'] == str(year) and entry['kommun'].upper() == community:
                            kommunal_skatt = entry["kommunal-skatt"]
                            kommun = entry['kommun']
                            entry_data = {
                                "Year": entry["år"],
                                "Kommun": kommun,
                                "Kommunal Skatt": kommunal_skatt
                            }
                            if entry_data not in filtered_data:
                                filtered_data.append(entry_data)
                else:
                    print(f"Failed to retrieve data for year {year} and community {community}. Status code:", response.status_code)

        except Exception as error:
            print(f"An error occurred for year {year} and community {community}:", str(error))

    return filtered_data

from openpyxl import Workbook

def save_to_excel(data, file_name):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Kommunal Skatt Data"
    header = ["Year", "Kommun", "Kommunal Skatt"]
    sheet.append(header)

    for entry in data:
        sheet.append([entry['Year'], entry['Kommun'], entry['Kommunal Skatt']])

    workbook.save(file_name)


if __name__ == "__main__":
    url = "https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99"
    target_years = range(2014, 2024)
    target_communities = ["JÄRFÄLLA", "LIDINGÖ", "NACKA", "NORRTÄLJE", "NYKVARN", "ÖSTERÅKER"]
    data = []

data = fetch_and_filter_data(url=url, target_years=target_years, target_communities=target_communities)
print("Data fetched and filtered successfully.")
if 'data' in locals() and data:
    save_to_excel(data=data, file_name='kommunal_skatt_data1.xlsx')
else:
     print("No data to save. Please fetch data first (Option 1).")
    
