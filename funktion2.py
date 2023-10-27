

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