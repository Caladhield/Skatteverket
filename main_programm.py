

import funktion1, funktion2


if __name__ == "__main__":
    url = "https://skatteverket.entryscape.net/rowstore/dataset/c67b320b-ffee-4876-b073-dd9236cd2a99"
    target_years = range(2014, 2024)
    target_communities = ["JÄRFÄLLA", "LIDINGÖ", "NACKA", "NORRTÄLJE", "NYKVARN", "ÖSTERÅKER"]
    data = []
    
    
    while True: 
     print('-------Vi ska ha en MENY-------')  # Display a menu for the user.
     print('\n1) Hämta data') 
     print('\n2) Lagra data i excel')
     print('\n9) Avsluta') 

     val = input("\n\tVälj en alternativ (1/2/9): ")  # Ask the user to choose an option (1, 2, or 9).
 
     if val == "1":
        # If the user selects option 1, call the 'fetch_and_filter_data' function and store the result in 'data'.
        data = funktion1.fetch_and_filter_data(url=url, target_years=target_years, target_communities=target_communities)
        print("Data fetched and filtered successfully.")

       
     elif val == "2":
        if 'data' in locals() and data:
            funktion2.save_to_excel(data=data, file_name='kommunal_skatt_data1.xlsx')
        else:
            print("No data to save. Please fetch data first (Option 1).")
        
    
     elif val == "9":  # If the user selects option 9, exit the loop, ending the program.
       break
     
     else:
        print("Ogiltigt alternativ. Vänligen välj 1, 2 eller 9.")

