
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
