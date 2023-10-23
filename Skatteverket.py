import requests

url = "https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99"

start_year = 2014
end_year = 2024

for year in range(start_year, end_year):
    url = f"{url}?år={year}"
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"Data for year {year}:")
            print(data)
        else:
            print(f"Failed to retrieve data for year {year}. Status code:", response.status_code)
    except Exception as error:
        print(f"An error occurred for year {year}:", str(error))

